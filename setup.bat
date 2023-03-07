@echo off
echo Checking python version...
for /f "tokens=*" %%a in ('python --version') do set version=%%a
if %version:~0,3% GEQ 3.9 (
    echo Python 3.9 or higher is installed...
) else (
    echo Python 3.9 or higher is not installed...
    echo Please install Python 3.9 or higher from the official website
    exit /b
)
if exist env (
    echo Virtual Environment already exists!
    echo Attempting to install Python Dependencies...
    call env\Scripts\Activate.bat
    pip install -r requirements.txt
) else (
    echo Starting Virtual Environment...
    python -m venv env
    call env\Scripts\Activate.bat
    echo Installing Python Dependencies...
    pip install -r requirements.txt
)

echo Installation successful, this setup script will now exit...