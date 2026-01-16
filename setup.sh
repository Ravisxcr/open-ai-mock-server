#!/bin/bash

# Setup script for OpenAI Mock Server

echo "🚀 Setting up OpenAI Mock Server..."

# Create virtual environment
echo "📦 Creating virtual environment..."
python -m venv venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Run migrations
echo "🗃️ Setting up database..."
python manage.py makemigrations
python manage.py migrate

# Create superuser prompt
echo "👤 Create a superuser account for admin access..."
python manage.py createsuperuser

echo "✅ Setup complete! You can now run the server with:"
echo "   python manage.py runserver"
echo ""
echo "🌐 Access the dashboard at: http://localhost:8000/dashboard/"
echo "🔧 Access the admin at: http://localhost:8000/admin/"