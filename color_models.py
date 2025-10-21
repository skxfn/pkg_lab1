"""
High-accuracy color space conversions for RGB ↔ XYZ ↔ CMYK using sRGB primaries,
D65 white point and standard IEC 61966-2-1 transfer functions.

All channel orders are:
- RGB: 0..255 integers in UI, 0..1 floats in conversion
- XYZ: referenced to D65 white with Yn = 100.0 (Xn=95.047, Yn=100.0, Zn=108.883)
- CMYK: 0..100 percent in UI, 0..1 floats in conversion

The module also reports clipping when converting out of gamut.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple, Dict

# D65 white point (2°) with Yn=100
D65_XN = 95.047
D65_YN = 100.0
D65_ZN = 108.883


@dataclass
class ClipReport:
	"""Stores which channels were clipped and to what values."""
	clipped: bool
	details: Dict[str, Tuple[float, float]]  # name -> (original, clipped)

	@staticmethod
	def empty() -> "ClipReport":
		return ClipReport(False, {})

	def merge(self, other: "ClipReport") -> "ClipReport":
		if not other.clipped:
			return self
		merged = dict(self.details)
		merged.update(other.details)
		return ClipReport(True, merged)


def _srgb_compand_forward(c: float) -> float:
	"""Linear RGB (0..1) -> sRGB companded (0..1)."""
	if c <= 0.0031308:
		return 12.92 * c
	return 1.055 * (c ** (1 / 2.4)) - 0.055


def _srgb_compand_inverse(c: float) -> float:
	"""sRGB companded (0..1) -> linear RGB (0..1)."""
	if c <= 0.04045:
		return c / 12.92
	return ((c + 0.055) / 1.055) ** 2.4


def _clip01(x: float) -> Tuple[float, ClipReport]:
	if x < 0.0:
		return 0.0, ClipReport(True, {"clip": (x, 0.0)})
	if x > 1.0:
		return 1.0, ClipReport(True, {"clip": (x, 1.0)})
	return x, ClipReport.empty()


def rgb8_to_rgb1(r: int, g: int, b: int) -> Tuple[float, float, float]:
	return r / 255.0, g / 255.0, b / 255.0


def rgb1_to_rgb8(r: float, g: float, b: float) -> Tuple[int, int, int]:
	return int(round(max(0.0, min(1.0, r)) * 255)), int(round(max(0.0, min(1.0, g)) * 255)), int(round(max(0.0, min(1.0, b)) * 255))


# sRGB to XYZ matrix, from IEC 61966-2-1:1999 / Wikipedia (assuming D65)
# Uses linear RGB (not gamma encoded)
M_RGB_TO_XYZ = (
	(0.4124564, 0.3575761, 0.1804375),
	(0.2126729, 0.7151522, 0.0721750),
	(0.0193339, 0.1191920, 0.9503041),
)

M_XYZ_TO_RGB = (
	(3.2404542, -1.5371385, -0.4985314),
	(-0.9692660, 1.8760108, 0.0415560),
	(0.0556434, -0.2040259, 1.0572252),
)


def rgb_to_xyz(r8: int, g8: int, b8: int) -> Tuple[float, float, float, ClipReport]:
	"""Convert 8-bit sRGB to XYZ (D65) with Yn=100. Returns (X, Y, Z, clip).

	The returned XYZ values are scaled such that Y of white equals 100.
	"""
	r, g, b = rgb8_to_rgb1(r8, g8, b8)
	r_lin = _srgb_compand_inverse(r)
	g_lin = _srgb_compand_inverse(g)
	b_lin = _srgb_compand_inverse(b)

	X = 100.0 * (M_RGB_TO_XYZ[0][0] * r_lin + M_RGB_TO_XYZ[0][1] * g_lin + M_RGB_TO_XYZ[0][2] * b_lin)
	Y = 100.0 * (M_RGB_TO_XYZ[1][0] * r_lin + M_RGB_TO_XYZ[1][1] * g_lin + M_RGB_TO_XYZ[1][2] * b_lin)
	Z = 100.0 * (M_RGB_TO_XYZ[2][0] * r_lin + M_RGB_TO_XYZ[2][1] * g_lin + M_RGB_TO_XYZ[2][2] * b_lin)

	return X, Y, Z, ClipReport.empty()


def xyz_to_rgb(X: float, Y: float, Z: float) -> Tuple[int, int, int, ClipReport]:
	"""Convert XYZ (D65, Yn=100) to 8-bit sRGB. Returns (R,G,B,clip)."""
	# Normalize to 0..1 domain for matrix multiply
	x = X / 100.0
	y = Y / 100.0
	z = Z / 100.0

	r_lin = M_XYZ_TO_RGB[0][0] * x + M_XYZ_TO_RGB[0][1] * y + M_XYZ_TO_RGB[0][2] * z
	g_lin = M_XYZ_TO_RGB[1][0] * x + M_XYZ_TO_RGB[1][1] * y + M_XYZ_TO_RGB[1][2] * z
	b_lin = M_XYZ_TO_RGB[2][0] * x + M_XYZ_TO_RGB[2][1] * y + M_XYZ_TO_RGB[2][2] * z

	clip = ClipReport.empty()
	r_lin, cr = _clip01(r_lin)
	clip = clip.merge(_rename_clip(cr, "R_lin"))
	g_lin, cg = _clip01(g_lin)
	clip = clip.merge(_rename_clip(cg, "G_lin"))
	b_lin, cb = _clip01(b_lin)
	clip = clip.merge(_rename_clip(cb, "B_lin"))

	r = _srgb_compand_forward(r_lin)
	g = _srgb_compand_forward(g_lin)
	b = _srgb_compand_forward(b_lin)

	r8, g8, b8 = rgb1_to_rgb8(r, g, b)
	return r8, g8, b8, clip


def _rename_clip(rep: ClipReport, prefix: str) -> ClipReport:
	if not rep.clipped:
		return rep
	details = {f"{prefix}": v for _, v in rep.details.items()}
	return ClipReport(True, details)


def rgb_to_cmyk(r8: int, g8: int, b8: int) -> Tuple[float, float, float, float]:
	"""sRGB 8-bit -> CMYK (device-independent approx), returns percentages (0..100)."""
	r = r8 / 255.0
	g = g8 / 255.0
	b = b8 / 255.0

	k = 1.0 - max(r, g, b)
	if k >= 0.999999:
		return 0.0, 0.0, 0.0, 100.0
	c = (1.0 - r - k) / (1.0 - k)
	m = (1.0 - g - k) / (1.0 - k)
	y = (1.0 - b - k) / (1.0 - k)
	return c * 100.0, m * 100.0, y * 100.0, k * 100.0


def cmyk_to_rgb(Cp: float, Mp: float, Yp: float, Kp: float) -> Tuple[int, int, int]:
	"""CMYK percentages (0..100) -> sRGB 8-bit."""
	C = max(0.0, min(100.0, Cp)) / 100.0
	M = max(0.0, min(100.0, Mp)) / 100.0
	Y = max(0.0, min(100.0, Yp)) / 100.0
	K = max(0.0, min(100.0, Kp)) / 100.0

	r = 1.0 - min(1.0, C * (1.0 - K) + K)
	g = 1.0 - min(1.0, M * (1.0 - K) + K)
	b = 1.0 - min(1.0, Y * (1.0 - K) + K)

	return rgb1_to_rgb8(r, g, b)


def constrain_xyz(X: float, Y: float, Z: float) -> Tuple[float, float, float]:
	# XYZ can be non-negative; practical ranges depend on illuminant. We constrain softly for UI.
	return max(0.0, X), max(0.0, Y), max(0.0, Z)


def to_hex(r8: int, g8: int, b8: int) -> str:
	return f"#{r8:02X}{g8:02X}{b8:02X}"


def from_hex(hex_str: str) -> Tuple[int, int, int]:
	s = hex_str.strip().lstrip('#')
	if len(s) == 3:
		s = ''.join([ch * 2 for ch in s])
	if len(s) != 6:
		raise ValueError("Invalid hex color")
	r = int(s[0:2], 16)
	g = int(s[2:4], 16)
	b = int(s[4:6], 16)
	return r, g, b
