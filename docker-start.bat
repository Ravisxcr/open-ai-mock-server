@echo off
REM Build and run the application with Docker Compose

echo Building OpenAI Mock Server...
docker-compose build

echo Starting services...
docker-compose up -d

echo Waiting for services to start...
timeout /t 10 /nobreak > nul

echo Running migrations...
docker-compose exec web python manage.py migrate

echo Collecting static files...
docker-compose exec web python manage.py collectstatic --noinput

echo Creating superuser...
docker-compose exec web python create_user.py

echo OpenAI Mock Server is running at http://localhost:8000
echo Dashboard: http://localhost:8000/dashboard/
echo API: http://localhost:8000/v1/

echo To view logs: docker-compose logs -f
echo To stop: docker-compose down

pause