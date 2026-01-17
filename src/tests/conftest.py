import os
import pytest
import requests

@pytest.fixture(scope="session")
def base_url():
    """
    Base URL for the OpenAI Mock Server
    """
    return os.getenv("OPENAI_MOCK_BASE_URL", "http://localhost:8000/v1")


@pytest.fixture(scope="session")
def api_key():
    """
    API key used for authentication.
    Set via env variable for security:
        export OPENAI_MOCK_API_KEY=sk-xxxx
    """
    return os.getenv("OPENAI_MOCK_API_KEY", "sk-0ZE6DQEogW6TUutF87fhKSUgVTgarn67yymzomwBkY4jfrqb")


@pytest.fixture(scope="session")
def headers(api_key):
    """
    Common headers for all API requests
    """
    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }


@pytest.fixture(scope="session")
def session():
    """
    Shared requests session for all tests
    """
    s = requests.Session()
    yield s
    s.close()


@pytest.fixture
def api_client(session, base_url, headers):
    """
    Generic API client fixture
    """

    class APIClient:
        def post(self, endpoint, json=None):
            return session.post(
                f"{base_url}{endpoint}",
                headers=headers,
                json=json,
                timeout=10,
            )

        def get(self, endpoint):
            return session.get(
                f"{base_url}{endpoint}",
                headers=headers,
                timeout=10,
            )

    return APIClient()
