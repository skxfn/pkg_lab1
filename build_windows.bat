@echo off
REM Сборка однокомпонентного EXE для приложения на Streamlit (Windows)
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install pyinstaller
pyinstaller --onefile --windowed --name ColorModelsApp run_app.py

echo.
echo Сборка завершена. EXE: dist\ColorModelsApp.exe

