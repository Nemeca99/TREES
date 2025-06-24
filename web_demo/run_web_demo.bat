@echo off
echo Starting TREES Web Demo...

REM Check if Python is installed
where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Python is not installed or not in the PATH. Please install Python and try again.
    pause
    exit /b
)

REM Check if requirements are installed, install if missing
echo Checking dependencies...
pip show flask >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Installing Flask and other dependencies...
    pip install -r requirements.txt
)

REM Run the web server
echo Starting web server...
python app.py
