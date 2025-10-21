# Submission Checklist

Use this checklist to submit strictly per the task requirements.

## 1) Executable or public web app
- [ ] Windows EXE built with PyInstaller using `build_windows.bat`
  - Output path: `dist/ColorModelsApp.exe`
  - Test on a clean Windows PC (no dev tools): double‑click opens the app in browser.
- OR
- [ ] Public web app deployed (e.g., Streamlit Community Cloud)
  - Provide public URL in the README under "Submission".

## 2) Source code on GitHub
- [ ] Push all files (include `app.py`, `color_models.py`, `requirements.txt`, `run_app.py`, `build_windows.bat`, `README.md`, and this checklist)
- [ ] Add tags/release if required; ensure repository is public or shared with the instructor.

## 3) Accompanying documentation
- [ ] `README.md` includes:
  - Project description and features
  - Run locally instructions
  - Windows EXE build steps and where to find the `.exe`
  - Optional: deployment instructions and public URL
- [ ] Screenshots or short GIF of the app (optional but recommended)

## QA before submission
- [ ] Changing any field (RGB/XYZ/CMYK) updates other models
- [ ] Warning appears for out‑of‑gamut XYZ→RGB cases
- [ ] RGB↔XYZ and RGB↔CMYK round‑trip sanity check
- [ ] Lint passes; app launches without errors

