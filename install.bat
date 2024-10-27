@echo off
chcp 65001
echo Checking for installed Python...

REM Checking for Python installation and its version
python --version > nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Python is not installed. Installing the latest version...
    REM Downloading the Python installer
    set PYTHON_INSTALLER=python-installer.exe
    curl -Lo %PYTHON_INSTALLER% https://www.python.org/ftp/python/3.12.0/python-3.12.0-amd64.exe

    REM Running the installer
    start /wait %PYTHON_INSTALLER% /quiet InstallAllUsers=1 PrependPath=1

    REM Deleting the installer
    del %PYTHON_INSTALLER%
) ELSE (
    echo Python is already installed. Skipping installation.
)

echo Installing required libraries...
pip install pandas requests openpyxl
echo All required libraries have been installed.
pause


