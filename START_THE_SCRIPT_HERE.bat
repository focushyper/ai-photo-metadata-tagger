@echo off
setlocal

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed.
    echo Please download and install Python 3.8 or newer from https://www.python.org/downloads/
    pause
    exit /b
)

:: Get the Python version
for /f "tokens=2 delims= " %%a in ('python --version') do set PYTHON_VERSION=%%a

:: Check if Python version is 3.8 or newer
for /f "tokens=1,2 delims=." %%a in ("%PYTHON_VERSION%") do (
    if %%a LSS 3 (
        echo Python version is less than 3.8. Please install Python 3.8 or newer.
        pause
        exit /b
    )
    if %%a EQU 3 (
        if %%b LSS 8 (
            echo Python version is less than 3.8. Please install Python 3.8 or newer.
            pause
            exit /b
        )
    )
)

:: Check if pip is installed
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Pip is not installed.
    echo Please ensure that pip is installed correctly with Python.
    pause
    exit /b
)

:: Install required packages
echo Installing required packages...
pip install -r requirements.txt

:: Start the script
echo Starting the script...
python script.py

:: Pause to keep the command prompt open
pause
endlocal
