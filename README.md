## Color Models App (RGB ↔ XYZ ↔ CMYK)

A Streamlit web app that lets you select and edit a color using synchronized inputs across RGB, XYZ, and CMYK. All models update automatically; out-of-gamut conversions show non-intrusive warnings.

[Документация на русском](docs/Документация.md)

### Features
- Interactive color picker, sliders, and precise numeric inputs.
- Bidirectional conversion: RGB ↔ XYZ (D65, sRGB) and RGB ↔ CMYK.
- Gamut clipping warnings with details on which channels were clipped.
- Copyable HEX and decimal values.

### Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

### Build Windows EXE
Option A — run the helper script on Windows:
```bat
build_windows.bat
```
This creates `dist/ColorModelsApp.exe`.

Option B — manual commands:
```bat
pip install -r requirements.txt
pip install pyinstaller
pyinstaller --onefile --windowed --name ColorModelsApp run_app.py
```

### Build on macOS (local binary)
Option A — run the helper script:
```bash
./build_macos.sh
```
Output: `dist/ColorModelsApp`

Option B — manual commands:
```bash
pip install -r requirements.txt
pip install pyinstaller
pyinstaller --onefile --windowed --name ColorModelsApp run_app.py
```
Run the binary by double-clicking `dist/ColorModelsApp` or from terminal.

### Deploy to Streamlit Cloud (optional instead of EXE)
- Push repo to GitHub
- On Streamlit Community Cloud, create a new app pointing to `app.py`
- Add repository secrets if needed (none for this app)
- Share the public URL

### Submission
Provide:
- Windows executable at `dist/ColorModelsApp.exe` OR a public deployment URL
- GitHub repository link (with all sources)
- Any additional docs/screenshots. See `docs/SubmissionChecklist.md`.

### Notes
- XYZ conversions use sRGB primaries and D65 white with IEC 61966-2-1 companding.
- CMYK is device-independent approximation: K = 1 − max(R,G,B); C/M/Y normalized over (1−K), then scaled to 0–100%.
- R,G,B are 0..255; X,Y,Z use Yn=100 with D65; C,M,Y,K are in %.
