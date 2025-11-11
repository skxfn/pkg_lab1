import streamlit as st
from functools import partial
from color_models import (
	rgb_to_xyz,
	xyz_to_rgb,
	rgb_to_cmyk,
	cmyk_to_rgb,
	to_hex,
	from_hex,
	constrain_xyz,
)

st.set_page_config(page_title="RGB ↔ XYZ ↔ CMYK", page_icon="🎨", layout="wide")


def header():
	st.title("Интерактивные цветовые модели: RGB ↔ XYZ ↔ CMYK")
	st.caption(
		"sRGB, белая точка D65. XYZ нормированы к Yn=100. CMYK — K = 1 − max(R,G,B)."
	)


# Инициализация базового состояния цвета
if "color_rgb" not in st.session_state:
	st.session_state.color_rgb = (255, 0, 0)
	X, Y, Z, _ = rgb_to_xyz(*st.session_state.color_rgb)
	st.session_state.color_xyz = (X, Y, Z)
	C, M, Yc, K = rgb_to_cmyk(*st.session_state.color_rgb)
	st.session_state.color_cmyk = (C, M, Yc, K)


# Вспомогательные функции для синхронизации значений виджетов с текущими моделями

def _set_rgb_widget_values(r: int, g: int, b: int):
	st.session_state["rgb_r"] = int(r)
	st.session_state["rgb_g"] = int(g)
	st.session_state["rgb_b"] = int(b)
	st.session_state["rgb_r_s"] = int(r)
	st.session_state["rgb_g_s"] = int(g)
	st.session_state["rgb_b_s"] = int(b)
	st.session_state["hex_pick"] = to_hex(int(r), int(g), int(b))


def _set_xyz_widget_values(X: float, Y: float, Z: float):
	st.session_state["xyz_x"] = float(X)
	st.session_state["xyz_y"] = float(Y)
	st.session_state["xyz_z"] = float(Z)
	st.session_state["xyz_x_s"] = float(X)
	st.session_state["xyz_y_s"] = float(Y)
	st.session_state["xyz_z_s"] = float(Z)


def _set_cmyk_widget_values(C: float, M: float, Yc: float, K: float):
	st.session_state["cmyk_c"] = float(C)
	st.session_state["cmyk_m"] = float(M)
	st.session_state["cmyk_y"] = float(Yc)
	st.session_state["cmyk_k"] = float(K)
	st.session_state["cmyk_c_s"] = float(C)
	st.session_state["cmyk_m_s"] = float(M)
	st.session_state["cmyk_y_s"] = float(Yc)
	st.session_state["cmyk_k_s"] = float(K)


# Обеспечиваем наличие исходных значений для всех виджетов при первом рендере
r0, g0, b0 = st.session_state.color_rgb
x0, y0, z0 = st.session_state.color_xyz
c0, m0, yk0, k0 = st.session_state.color_cmyk
for key, val in (
	("rgb_r", int(r0)), ("rgb_g", int(g0)), ("rgb_b", int(b0)),
	("rgb_r_s", int(r0)), ("rgb_g_s", int(g0)), ("rgb_b_s", int(b0)),
	("xyz_x", float(x0)), ("xyz_y", float(y0)), ("xyz_z", float(z0)),
	("xyz_x_s", float(x0)), ("xyz_y_s", float(y0)), ("xyz_z_s", float(z0)),
	("cmyk_c", float(c0)), ("cmyk_m", float(m0)), ("cmyk_y", float(yk0)), ("cmyk_k", float(k0)),
	("cmyk_c_s", float(c0)), ("cmyk_m_s", float(m0)), ("cmyk_y_s", float(yk0)), ("cmyk_k_s", float(k0)),
	("hex_pick", to_hex(int(r0), int(g0), int(b0))),
):
	if key not in st.session_state:
		st.session_state[key] = val


# Функции обновления модели с синхронизацией виджетов

def update_from_rgb(r: int, g: int, b: int):
	st.session_state.color_rgb = (int(r), int(g), int(b))
	X, Y, Z, _ = rgb_to_xyz(int(r), int(g), int(b))
	st.session_state.color_xyz = (X, Y, Z)
	C, M, Yc, K = rgb_to_cmyk(int(r), int(g), int(b))
	st.session_state.color_cmyk = (C, M, Yc, K)
	_set_rgb_widget_values(int(r), int(g), int(b))
	_set_xyz_widget_values(X, Y, Z)
	_set_cmyk_widget_values(C, M, Yc, K)


def update_from_xyz(X: float, Y: float, Z: float):
	X, Y, Z = constrain_xyz(X, Y, Z)
	r, g, b, clip = xyz_to_rgb(X, Y, Z)
	st.session_state.color_xyz = (X, Y, Z)
	st.session_state.color_rgb = (r, g, b)
	C, M, Yc, K = rgb_to_cmyk(r, g, b)
	st.session_state.color_cmyk = (C, M, Yc, K)
	_set_xyz_widget_values(X, Y, Z)
	_set_rgb_widget_values(r, g, b)
	_set_cmyk_widget_values(C, M, Yc, K)
	if clip.clipped:
		st.warning(
			"Некоторые компоненты вне гаммы sRGB — значения обрезаны перед гаммой.",
			icon="⚠️",
		)


def update_from_cmyk(C: float, M: float, Yc: float, K: float):
	r, g, b = cmyk_to_rgb(C, M, Yc, K)
	update_from_rgb(r, g, b)


# Общий колбэк синхронизации пары «число ↔ слайдер» и пересчёт моделей

def _on_pair_change(prefix: str, comp: str, is_slider: bool):
	if is_slider:
		st.session_state[f"{prefix}_{comp}"] = st.session_state[f"{prefix}_{comp}_s"]
	else:
		st.session_state[f"{prefix}_{comp}_s"] = st.session_state[f"{prefix}_{comp}"]
	if prefix == "rgb":
		update_from_rgb(
			int(st.session_state["rgb_r"]),
			int(st.session_state["rgb_g"]),
			int(st.session_state["rgb_b"]),
		)
	elif prefix == "xyz":
		update_from_xyz(
			float(st.session_state["xyz_x"]),
			float(st.session_state["xyz_y"]),
			float(st.session_state["xyz_z"]),
		)
	elif prefix == "cmyk":
		update_from_cmyk(
			float(st.session_state["cmyk_c"]),
			float(st.session_state["cmyk_m"]),
			float(st.session_state["cmyk_y"]),
			float(st.session_state["cmyk_k"]),
		)


def _on_hex_change():
	try:
		rr, gg, bb = from_hex(st.session_state["hex_pick"])
		_set_rgb_widget_values(rr, gg, bb)
		update_from_rgb(rr, gg, bb)
	except Exception:
		pass


header()

left, mid, right = st.columns([1.0, 1.0, 1.0])

with left:
	st.subheader("RGB")
	c1, c2, c3 = st.columns(3)
	c1.number_input("R", 0, 255, key="rgb_r", on_change=partial(_on_pair_change, "rgb", "r", False))
	c2.number_input("G", 0, 255, key="rgb_g", on_change=partial(_on_pair_change, "rgb", "g", False))
	c3.number_input("B", 0, 255, key="rgb_b", on_change=partial(_on_pair_change, "rgb", "b", False))
	st.slider("R", 0, 255, key="rgb_r_s", on_change=partial(_on_pair_change, "rgb", "r", True))
	st.slider("G", 0, 255, key="rgb_g_s", on_change=partial(_on_pair_change, "rgb", "g", True))
	st.slider("B", 0, 255, key="rgb_b_s", on_change=partial(_on_pair_change, "rgb", "b", True))
	st.color_picker("Палитра", key="hex_pick", on_change=_on_hex_change)

with mid:
	st.subheader("XYZ (D65, Yn=100)")
	c1, c2, c3 = st.columns(3)
	c1.number_input("X", 0.0, 120.0, step=0.1, key="xyz_x", on_change=partial(_on_pair_change, "xyz", "x", False))
	c2.number_input("Y", 0.0, 120.0, step=0.1, key="xyz_y", on_change=partial(_on_pair_change, "xyz", "y", False))
	c3.number_input("Z", 0.0, 120.0, step=0.1, key="xyz_z", on_change=partial(_on_pair_change, "xyz", "z", False))
	st.slider("X", 0.0, 120.0, step=0.1, key="xyz_x_s", on_change=partial(_on_pair_change, "xyz", "x", True))
	st.slider("Y", 0.0, 120.0, step=0.1, key="xyz_y_s", on_change=partial(_on_pair_change, "xyz", "y", True))
	st.slider("Z", 0.0, 120.0, step=0.1, key="xyz_z_s", on_change=partial(_on_pair_change, "xyz", "z", True))

with right:
	st.subheader("CMYK (%)")
	c1, c2 = st.columns(2)
	c1.number_input("C", 0.0, 100.0, step=0.1, key="cmyk_c", on_change=partial(_on_pair_change, "cmyk", "c", False))
	c2.number_input("M", 0.0, 100.0, step=0.1, key="cmyk_m", on_change=partial(_on_pair_change, "cmyk", "m", False))
	c1.number_input("Y", 0.0, 100.0, step=0.1, key="cmyk_y", on_change=partial(_on_pair_change, "cmyk", "y", False))
	c2.number_input("K", 0.0, 100.0, step=0.1, key="cmyk_k", on_change=partial(_on_pair_change, "cmyk", "k", False))
	st.slider("C", 0.0, 100.0, step=0.1, key="cmyk_c_s", on_change=partial(_on_pair_change, "cmyk", "c", True))
	st.slider("M", 0.0, 100.0, step=0.1, key="cmyk_m_s", on_change=partial(_on_pair_change, "cmyk", "m", True))
	st.slider("Y", 0.0, 100.0, step=0.1, key="cmyk_y_s", on_change=partial(_on_pair_change, "cmyk", "y", True))
	st.slider("K", 0.0, 100.0, step=0.1, key="cmyk_k_s", on_change=partial(_on_pair_change, "cmyk", "k", True))

st.divider()

r, g, b = st.session_state.color_rgb
X, Y, Z = st.session_state.color_xyz
C, M, Yc, K = st.session_state.color_cmyk

st.markdown(
	f"Текущий цвет: RGB {r},{g},{b} | XYZ {X:.2f},{Y:.2f},{Z:.2f} | CMYK {C:.1f},{M:.1f},{Yc:.1f},{K:.1f} | HEX {to_hex(r,g,b)}"
)

st.markdown(
	f"""
<div style=\"width:100%;height:120px;border-radius:8px;border:1px solid #ddd;background: {to_hex(r,g,b)}\"></div>
""",
	unsafe_allow_html=True,
)

st.caption(
	"При изменении любой координаты обновление происходит автоматически; при XYZ→RGB вне гаммы будет предупреждение."
)

