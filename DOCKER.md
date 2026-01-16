# OpenAI Mock Server - Docker Setup

## Quick Start with Docker

### Development Environment

1. **Build and run the application:**
   ```bash
   # Linux/Mac
   chmod +x docker-start.sh
   ./docker-start.sh
   
   # Windows
   docker-start.bat
   ```

2. **Or manually with Docker Compose:**
   ```bash
   docker-compose up -d --build
   docker-compose exec web python manage.py migrate
   docker-compose exec web python create_user.py
   ```

3. **Access the application:**
   - Dashboard: http://localhost:8000/dashboard/
   - API Documentation: http://localhost:8000/v1/
   - Admin: http://localhost:8000/admin/

### Production Environment

```bash
docker-compose -f docker-compose.prod.yml up -d --build
```

## Services

- **web**: Django application server
- **db**: PostgreSQL database

## Environment Variables

- `DEBUG`: Enable Django debug mode
- `DATABASE_URL`: PostgreSQL connection string
- `DJANGO_SETTINGS_MODULE`: Settings module to use

## Useful Commands

```bash
# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Stop and remove volumes
docker-compose down -v

# Execute commands in container
docker-compose exec web python manage.py shell

# Database backup
docker-compose exec db pg_dump -U postgres openai_mock > backup.sql

# Database restore
docker-compose exec -T db psql -U postgres openai_mock < backup.sql
```

## Scaling

```bash
# Scale web workers
docker-compose up -d --scale web=3
```

## Development

Mount your code as a volume for live reloading:
```yaml
volumes:
  - .:/app
```

The container will automatically reload when you make changes to the code.