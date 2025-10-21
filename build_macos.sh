#!/usr/bin/env bash
set -euo pipefail

# Build one-file macOS binary for the Streamlit app
python3 -m pip install --upgrade pip
pip3 install -r requirements.txt
pip3 install pyinstaller

pyinstaller --onefile --windowed --name ColorModelsApp run_app.py

echo
echo "Build finished. Binary: dist/ColorModelsApp"
