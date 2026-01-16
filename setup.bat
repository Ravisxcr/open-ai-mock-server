@echo off
REM Setup script for OpenAI Mock Server on Windows

echo Setting up OpenAI Mock Server...

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

REM Remove existing virtual environment if it exists
if exist ".venv\" (
    echo Removing existing virtual environment...
    rmdir /s /q .venv
)

REM Create virtual environment
echo Creating virtual environment...
python -m venv .venv

REM Activate virtual environment  
echo 🔧 Activating virtual environment...
call .venv\Scripts\activate.bat
REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies one by one to handle errors better
echo Installing dependencies...
pip install -r requirements.txt

REM Run migrations
cd src
echo Setting up database...
python manage.py makemigrations
python manage.py migrate
python create_user.py

REM Create superuser prompt
echo.
echo Create a superuser account for admin access...
echo (You can skip this by pressing Ctrl+C if you want to create it later)
python manage.py createsuperuser

echo.
echo Setup complete! You can now run the server with:
echo    start.bat
echo    or
echo    python manage.py runserver
echo.
echo Dashboard: http://localhost:8000/dashboard/
echo Admin: http://localhost:8000/admin/
echo Test API: python test_api.py
echo.
echo See README.md for detailed usage instructions

pause