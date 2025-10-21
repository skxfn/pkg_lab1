@echo off
REM Build one-file Windows executable for the Streamlit app
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install pyinstaller
pyinstaller --onefile --windowed --name ColorModelsApp run_app.py

echo.
echo Build finished. EXE: dist\ColorModelsApp.exe

