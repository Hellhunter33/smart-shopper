
# Smart Shopper

A Django-based smart shopping assistant API that fetches real-time product information using Google Custom Search and caches results in Redis for faster performance.

## Features

- Search for products by name.
- Returns structured product data: `name`, `brand`, `price`, `weight`, `link`.
- Redis caching for faster repeated queries.
- Fallback mock data if Google API fails.
- Configurable via `.env` for API keys and Redis URL.

## Setup

1. Clone the repo:

```bash
git clone https://github.com/Hellhunter33/smart-shopper.git
cd smart-shopper
````

2. Create a virtual environment and install dependencies:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. Create a `.env` file in the root:

```
SECRET_KEY=your_django_secret_key
GOOGLE_API_KEY=your_google_api_key
GOOGLE_CX=your_google_search_engine_id
REDIS_URL=redis://127.0.0.1:6379/0
```

4. Run migrations:

```bash
python manage.py migrate
```

5. Start the development server:

```bash
python manage.py runserver
```

6. Test the API:

```
GET http://127.0.0.1:8000/api/search/?q=Peanut+Butter
```

## Notes

* Ensure Redis is running locally or adjust `REDIS_URL`.
* Google API limits may restrict the number of searches per day.
* Use `.env` to keep sensitive information secure.
