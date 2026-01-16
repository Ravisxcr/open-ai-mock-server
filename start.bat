@echo off
REM Quick start script for OpenAI Mock Server
echo 🚀 Starting OpenAI Mock Server...

REM Check if virtual environment exists
if not exist "venv\" (
    echo ❌ Virtual environment not found. Please run setup.bat first.
    pause
    exit /b 1
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Start the server
echo 🌐 Starting server at http://127.0.0.1:8000/
echo 📊 Dashboard: http://127.0.0.1:8000/dashboard/
echo 🔧 Admin: http://127.0.0.1:8000/admin/
echo.
echo Press Ctrl+C to stop the server
python manage.py runserver