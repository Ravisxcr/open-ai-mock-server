#!/usr/bin/env python3
"""
Test script for OpenAI Mock Server API endpoints
This script tests all the available endpoints to ensure they work correctly.
"""

import requests
import json

# Configuration
BASE_URL = "http://localhost:8000/v1"
API_KEY = "sk-test123456789"  # This will need to be created in the dashboard


def test_endpoint(endpoint, data=None, method="POST"):
    """Test a specific API endpoint"""
    url = f"{BASE_URL}{endpoint}"
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

    try:
        if method == "POST":
            response = requests.post(url, headers=headers, json=data)
        else:
            response = requests.get(url, headers=headers)

        print(f"📍 {method} {endpoint}")
        print(f"Status: {response.status_code}")

        if response.status_code == 200:
            print("✅ SUCCESS")
            result = response.json()
            print(f"Response: {json.dumps(result, indent=2)[:200]}...")
        elif response.status_code == 401:
            print(
                "🔑 AUTHENTICATION ERROR - Please create an API key in the dashboard first"
            )
        else:
            print(f"❌ ERROR: {response.text}")

        print("-" * 60)
        return response.status_code == 200

    except requests.exceptions.ConnectionError:
        print(f"❌ CONNECTION ERROR: Could not connect to {url}")
        print("Make sure the server is running with: python manage.py runserver")
        return False
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False


def main():
    """Test all API endpoints"""
    print("🤖 Testing OpenAI Mock Server API Endpoints")
    print("=" * 60)

    tests = [
        # Chat completions
        {
            "endpoint": "/chat/completions",
            "data": {
                "model": "gpt-3.5-turbo",
                "messages": [{"role": "user", "content": "Hello, how are you?"}],
                "max_tokens": 50,
            },
        },
        # Embeddings
        {
            "endpoint": "/embeddings",
            "data": {
                "model": "text-embedding-ada-002",
                "input": "The quick brown fox jumps over the lazy dog",
            },
        },
        # Moderations
        {
            "endpoint": "/moderations",
            "data": {"input": "I love programming and building cool applications!"},
        },
        # Image generation
        {
            "endpoint": "/images/generations",
            "data": {
                "prompt": "A beautiful sunset over mountains",
                "n": 1,
                "size": "1024x1024",
            },
        },
        # Models listing
        {"endpoint": "/models", "method": "GET"},
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        method = test.get("method", "POST")
        data = test.get("data")

        if test_endpoint(test["endpoint"], data, method):
            passed += 1

    print("\n" + "=" * 60)
    print(f"📊 Test Results: {passed}/{total} tests passed")

    if passed == 0:
        print("\n🔑 To run these tests successfully:")
        print("1. Make sure the server is running: python manage.py runserver")
        print("2. Go to http://localhost:8000/dashboard/")
        print("3. Register an account and create an API key")
        print("4. Update the API_KEY variable in this script with your key")
    elif passed < total:
        print("⚠️  Some tests failed - check the error messages above")
    else:
        print("🎉 All tests passed! Your OpenAI Mock Server is working perfectly!")


if __name__ == "__main__":
    main()
