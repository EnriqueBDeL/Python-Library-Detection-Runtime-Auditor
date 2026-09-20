@echo off
chcp 65001 > nul
title Compilación de DLP (Python Library Detection) - EnriqueBDL

echo ======================================================================
echo    PYTHON LIBRARY DETECTION - COMPILACIÓN A EJECUTABLE OFICIAL (DLP.exe)
echo    Desarrollado por: EnriqueBDL
echo ======================================================================
echo.

cd /d "%~dp0\.."

echo [1/3] Verificando dependencias necesarias...
python -m pip install --upgrade pyinstaller pillow

echo.
echo [2/3] Compilando con PyInstaller (DLP.spec)...
pyinstaller --clean --noconsole --onefile --icon="Media/app_icon.ico" --add-data "Media;Media" --name="DLP" main.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] Ocurrió un error durante la compilación.
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo [3/3] Compilación exitosa. El ejecutable oficial se encuentra en:
echo       dist\DLP.exe
echo.
echo ======================================================================
echo    ¡PROCESO COMPLETADO SATISFACTORIAMENTE!
echo ======================================================================
pause
