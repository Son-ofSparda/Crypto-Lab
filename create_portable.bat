@echo off
echo Создание портативной версии CryptoLab...
echo.

REM Установка зависимостей
pip install -r requirements.txt

REM Создание папки для портативной версии
if exist Portable_CryptoLab rmdir /s /q Portable_CryptoLab
mkdir Portable_CryptoLab

REM Копирование файлов
copy main.py Portable_CryptoLab\
copy README.txt Portable_CryptoLab\
copy icon.ico Portable_CryptoLab\

REM Создание bat-файла для запуска
echo @echo off > Portable_CryptoLab\run.bat
echo echo Запуск CryptoLab... >> Portable_CryptoLab\run.bat
echo python main.py >> Portable_CryptoLab\run.bat
echo pause >> Portable_CryptoLab\run.bat

REM Создание портативного Python
echo Создание портативного Python (это может занять несколько минут)...
if not exist python_portable (
    mkdir python_portable
    echo Скачайте портативный Python с https://www.python.org/downloads/windows/ > python_portable\readme.txt
    echo и распакуйте в эту папку >> python_portable\readme.txt
)

echo.
echo ================================================
echo ГОТОВО!
echo ================================================
echo.
echo Варианты запуска программы:
echo.
echo 1. ПРОСТОЙ .EXE ФАЙЛ:
echo    Запустите: pyinstaller --onefile --windowed main.py
echo    .exe файл появится в папке dist
echo.
echo 2. ПОРТАТИВНАЯ ВЕРСИЯ:
echo    Папка Portable_CryptoLab готова к копированию на флешку
echo.
echo 3. УСТАНОВЩИК:
echo    Установите Inno Setup и скомпилируйте setup.iss
echo.
pause