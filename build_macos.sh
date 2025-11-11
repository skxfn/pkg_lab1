#!/usr/bin/env bash
set -euo pipefail

# Сборка однокомпонентного бинарника для приложения на Streamlit (macOS)
python3 -m pip install --upgrade pip
pip3 install -r requirements.txt
pip3 install pyinstaller

pyinstaller --onefile --windowed --name ColorModelsApp run_app.py

echo
echo "Сборка завершена. Бинарник: dist/ColorModelsApp"
