"""
ASGI config for openai_mock_server project.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "openai_mock_server.settings")

application = get_asgi_application()
