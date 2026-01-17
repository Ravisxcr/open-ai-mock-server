#!/usr/bin/env python
import os
import django
from decouple import config

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "openai_mock_server.settings")
django.setup()

from django.contrib.auth.models import User


def create_user():
    try:
        admin_user = config("ADMIN_USER", default="admin")
        admin_password = config("ADMIN_PASSWORD", default="admin123")

        # Check if user already exists
        if User.objects.filter(username=admin_user).exists():
            print(f'⚠️ User "{admin_user}" already exists!')
            print("You can login with:")
            print(f"Username: {admin_user}")
            print(f"Password: {admin_password}")
            return

        # Create superuser
        user = User.objects.create_superuser(
            username=admin_user, email="admin@example.com", password=admin_password
        )

        print("Superuser created successfully!")
        print(f"Username: {admin_user}")
        print("Email: admin@example.com")
        print(f"Password: {admin_password}")
        print("")
        print("You can now login to:")
        print("Dashboard: http://localhost:8000/dashboard/")
        print("Admin: http://localhost:8000/admin/")

    except Exception as e:
        print(f"❌ Error creating user: {e}")


if __name__ == "__main__":
    create_user()
