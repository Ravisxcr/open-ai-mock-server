# OpenAI Mock Server

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Django](https://img.shields.io/badge/django-4.0+-green.svg)](https://djangoproject.com/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)]()

A comprehensive Django-based mock server that provides OpenAI API compatibility for development, testing, and prototyping environments. This= solution includes a sophisticated dashboard for API key management, usage analytics, and comprehensive monitoring capabilities.

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Configuration](#configuration)
- [API Documentation](#api-documentation)
- [Dashboard Features](#dashboard-features)
- [Development](#development)
- [Deployment](#deployment)
- [Security Considerations](#security-considerations)
- [Performance](#performance)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)
- [Support](#support)

## Overview

The OpenAI Mock Server is designed to provide a complete OpenAI API simulation environment without the need for external API calls or costs. It's particularly useful for:

- **Development environments** where consistent, predictable responses are needed
- **Testing workflows** that require OpenAI API integration
- **Offline development** scenarios
- **Cost-effective prototyping** of AI-powered applications
- **Educational purposes** for understanding OpenAI API patterns

## Key Features

### 🔐 Advanced API Key Management
- **Secure Key Generation**: OpenAI-compatible format (`sk-proj-...`) with cryptographically secure random generation
- **Granular Permissions**: Fine-grained access control for individual API endpoints
- **Flexible Rate Limiting**: Customizable rate limits per API key with burst handling
- **Key Lifecycle Management**: Active, suspended, expired, and revoked key states
- **Audit Trail**: Comprehensive logging of key creation, modification, and usage

### 📊 Enterprise Dashboard & Analytics
- **Real-time Monitoring**: Live usage statistics and API performance metrics
- **Advanced Analytics**: Historical trends, usage patterns, and predictive insights
- **Visual Reporting**: Interactive charts and graphs for data visualization
- **Custom Dashboards**: Configurable views for different user roles
- **Export Capabilities**: Data export in multiple formats (CSV, JSON, PDF)

### 🚀 Complete OpenAI API Compatibility
- **Chat Completions** (`/v1/chat/completions`) - Multi-turn conversations with context
- **Text Embeddings** (`/v1/embeddings`) - Vector representations for semantic search
- **Content Moderation** (`/v1/moderations`) - Content safety and policy compliance
- **Image Generation** (`/v1/images/generations`) - AI-powered image creation
- **Model Management** (`/v1/models`) - Available models and capabilities listing
- **Streaming Support**: Real-time response streaming for enhanced user experience

### 🛡️ Enterprise Security & Authentication
- **Multi-layer Authentication**: User authentication with API key validation
- **Role-based Access Control**: Administrative and user-level permissions
- **Request Validation**: Input sanitization and schema validation
- **Audit Logging**: Comprehensive request and response logging
- **Rate Limiting**: DDoS protection and fair usage enforcement

### 📈 Comprehensive Usage Tracking
- **Detailed Metrics**: Request volume, token consumption, and response times
- **Performance Monitoring**: API endpoint performance and error tracking
- **Usage Forecasting**: Predictive analytics for capacity planning
- **Alert System**: Configurable alerts for usage thresholds and errors
- **Billing Simulation**: Mock billing calculations for cost estimation

## Prerequisites

Before installing the OpenAI Mock Server, ensure your system meets the following requirements:

### System Requirements
- **Operating System**: Windows 10/11, macOS 10.15+, or Linux (Ubuntu 18.04+ recommended)
- **Python**: Version 3.8 or higher (Python 3.9+ recommended)
- **Memory**: Minimum 2GB RAM (4GB+ recommended for production)
- **Storage**: At least 1GB free disk space
- **Network**: Internet connection for initial package installation

### Required Software
- **Python Package Manager**: pip (included with Python 3.4+)
- **Database**: SQLite (included) or PostgreSQL/MySQL for production
- **Web Browser**: Modern browser for dashboard access (Chrome, Firefox, Safari, Edge)

### Optional Components
- **Docker**: For containerized deployment
- **Reverse Proxy**: Nginx or Apache for production deployments
- **Process Manager**: systemd, supervisor, or PM2 for production process management

## Installation

### Option 1: Automated Setup (Recommended)

The fastest way to get started is using our automated setup scripts:

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/openai-mock-server.git
   cd openai-mock-server
   ```

2. **Run Automated Setup**

   ```bash
   # Windows
   .\setup.bat
   
   # Linux/macOS
   chmod +x setup.sh
   ./setup.sh
   ```

### Option 2: Docker Setup

For containerized deployment using Docker:

1. **Prerequisites**
   - Install [Docker](https://docs.docker.com/get-docker/)
   - Install [Docker Compose](https://docs.docker.com/compose/install/)

2. **Build and Run with Docker Compose**
   ```bash
   # For development
   docker-compose up --build
   
   # For production
   docker-compose -f docker-compose.prod.yml up --build -d
   ```

3. **Using the Convenience Scripts**
   ```bash
   # Windows
   .\docker-start.bat
   
   # Linux/macOS
   chmod +x docker-start.sh
   ./docker-start.sh
   ```

4. **Access the Application**
   - **Dashboard**: [http://localhost:8000/dashboard/](http://localhost:8000/dashboard/)
   - **Admin Panel**: [http://localhost:8000/admin/](http://localhost:8000/admin/)
   - **API Base URL**: [http://localhost:8000/v1/](http://localhost:8000/v1/)

5. **Stop the Server**
   ```bash
   docker-compose down
   ```

### Option 3: Manual Installation

For more control over the installation process:

1. **Create Virtual Environment**
   ```bash
   # Create virtual environment
   python -m venv venv
   
   # Activate virtual environment
   # Windows
   venv\Scripts\activate
   # Linux/macOS
   source venv/bin/activate
   ```

2. **Install Dependencies**
   ```bash
   # Upgrade pip to latest version
   python -m pip install --upgrade pip
   
   # Install project dependencies
   pip install -r requirements.txt
   ```

3. **Configure Database**
   ```bash
   # Create database migrations
   python src/manage.py makemigrations
   
   # Apply database migrations
   python src/manage.py migrate
   ```

4. **Create Administrative User**
   ```bash
   # Create superuser account (optional but recommended)
   python src/manage.py createsuperuser
   ```

5. **Initialize Default Data**
   ```bash
   # Create default API key plans and settings
   python src/manage.py loaddata initial_data.json  # If available
   ```

## Quick Start

### Starting the Server

1. **Make a copy of .env** edit the variable.

2. **Development Server**
   ```bash
   # Using convenience script
   .\start.bat  # Windows
   ./start.sh   # Linux/macOS
   
   # Or directly with Django
   cd src
   python manage.py runserver 0.0.0.0:8000
   ```

3. **Access the Application**
   - **Dashboard**: [http://localhost:8000/dashboard/](http://localhost:8000/dashboard/)
   - **Admin Panel**: [http://localhost:8000/admin/](http://localhost:8000/admin/)
   - **API Base URL**: [http://localhost:8000/v1/](http://localhost:8000/v1/)

4. **Create Your First API Key**
   - Navigate to the dashboard
   - Register a new user account
   - Create an API key with desired permissions
   - Note the generated key (starts with `sk-proj-`)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


### Frequently Asked Questions

**Q: Can this replace OpenAI's API completely?**
A: This is a mock server for development and testing. It simulates responses but doesn't provide actual AI capabilities.

**Q: How accurate are the simulated responses?**
A: The server focuses on API compatibility rather than response accuracy. Responses are generated for testing purposes.

**Q: Can I use this in production?**
A: While technically possible, this is designed for development environments. Production use requires careful consideration of your specific needs.

---

**Project Status**: Active Development
**Latest Version**: v1.0.0
**Last Updated**: January 2026
