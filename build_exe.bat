@echo off
echo Сборка CryptoLab в .exe файл...
echo.

REM Очистка предыдущих сборок
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build

REM Создание .exe файла
pyinstaller --onefile ^
            --windowed ^
            --name "CryptoLab" ^
            --icon=icon.ico ^
            --add-data "README.txt;." ^
            --hidden-import sympy ^
            main.py

echo.
echo Сборка завершена! .exe файл находится в папке dist
pause