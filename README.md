# Translation API 
Django API for text translation, handling both HTML and plain text inputs. It uses Django Rest Framework (DRF) for API functionality and BeautifulSoup for HTML parsing. The API integrates with a third-party chatGPT translation service and associates translations with specific users.

## Features
- Django 3.2+
- Environment variable management with `python-decouple`
- PostgreSQL database support
- Docker and Docker Compose setup for development
- Basic project structure with  `translation_api` app for the api for functionalities

## Getting Started

### Prerequisites

- Python 3.8+
- `pip` and `virtualenv`
- Docker (optional, for containerized development)

### Setup

1. **Clone the repository**

    ```bash
    git clone git@github.com:Marlinekhavele/SUMM-AI-Backend-Coding-Challenge.git
    cd translation
    ```

2. **Create and activate a virtual environment**

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install dependencies**

    ```bash
    pip install -r requirements.txt
    ```

4. **Create a `.env` file**

    ```bash
    cp .env.example
    ```

    Edit the `.env` file with your configuration settings.

5. **Run migrations**

    ```bash
    python manage.py makemigration
    python manage.py migrate
    ```

6. **Create a superuser**

    ```bash
    python manage.py createsuperuser
    ```

7. **Run the development server**

    ```bash
    python manage.py runserver
    ```
    
8. **Run tests**
  ```bash
    python manage.py test translation_api
    ```

### Docker Setup

1. **Build and run the Docker containers**

    ```bash
    docker-compose up --build
    ```

2. **Run migrations inside the Docker container**

    ```bash
    docker-compose exec web python manage.py migrate
    ```

- biggest challenge translation api everything requires billing so stressful
- worked with chatgpt it is better when an API key is given 