## Приложение «Цветовые модели (RGB ↔ XYZ ↔ CMYK)»

Веб‑приложение на Streamlit для интерактивного выбора и редактирования цвета с одновременным отображением значений в RGB, XYZ (D65, Yn=100) и CMYK. Все модели синхронизированы: изменение любой координаты автоматически пересчитывает остальные. При выходе XYZ→RGB за гамму показывается ненавязчивое предупреждение.

[Документация на русском (теория и инструкции)](docs/Документация.md)

### Возможности
- Точные числовые поля и плавные ползунки для RGB, XYZ, CMYK.
- Палитра (color picker), синхронизированная с RGB/HEX.
- Двунаправленные преобразования: RGB ↔ XYZ (sRGB, D65) и RGB ↔ CMYK (аппроксимация).
- Предупреждение о клиппинге при XYZ→RGB.
- Отображение HEX и предпросмотр цвета.

### Запуск локально
```bash
pip install -r requirements.txt
streamlit run app.py
```
Откройте адрес из лога (обычно `http://localhost:8501`).

### Сборка Windows (EXE)
Вариант A — с помощью скрипта:
```bat
build_windows.bat
```
Готовый файл: `dist/ColorModelsApp.exe`.

Вариант B — вручную:
```bat
pip install -r requirements.txt
pip install pyinstaller
pyinstaller --onefile --windowed --name ColorModelsApp run_app.py
```

### Сборка на macOS (локальный бинарник)
Вариант A — скрипт:
```bash
./build_macos.sh
```
Результат: `dist/ColorModelsApp.app` (двойной клик или `open dist/ColorModelsApp.app`).

Вариант B — вручную:
```bash
pip install -r requirements.txt
pip install pyinstaller
pyinstaller --onefile --windowed --name ColorModelsApp run_app.py
```

### Деплой в веб (по желанию вместо EXE)
- Streamlit Community Cloud:
  - Подключите репозиторий, укажите `app.py`.
  - Python 3.11 (в проекте есть `runtime.txt`).
  - Нажмите Deploy — получите публичный URL.
- Либо Hugging Face Spaces (шаблон Streamlit).

### Что сдавать
- Либо Windows‑исполняемый файл `dist/ColorModelsApp.exe`, либо публичный URL веб‑приложения.
- Ссылка на репозиторий GitHub с исходниками (включая `app.py`, `color_models.py`, `requirements.txt`, `run_app.py`, скрипты сборки, документацию).
- Краткая документация/скриншоты (у нас: `docs/Документация.md`).

### Примечания
- XYZ использует sRGB‑матрицы и белую точку D65, нормировку к Yn=100.
- CMYK — девайс‑независимая учебная аппроксимация: K = 1 − max(R,G,B); C/M/Y нормируются по (1−K), выводятся в процентах 0–100.
- Диапазоны: RGB 0..255; XYZ около 0..100 (Yn=100); CMYK 0..100%.
