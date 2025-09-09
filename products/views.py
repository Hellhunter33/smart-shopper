import requests
import json
import redis
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Connect to Redis using URL from settings.py (.env -> REDIS_URL)
redis_client = redis.StrictRedis.from_url(settings.REDIS_URL)

@api_view(["GET"])
def search_products(request):
    query = request.GET.get("q", "")

    if not query:
        return Response({"error": "Missing query parameter"}, status=400)

    cache_key = f"search:{query.lower()}"
    cached = redis_client.get(cache_key)

    if cached:
        print(f"✅ Cache hit for query: {query}")
        return Response({"query": query, "results": json.loads(cached)})

    print(f"❌ Cache miss for query: {query}, calling Google API...")

    api_key = settings.GOOGLE_API_KEY
    cx = settings.GOOGLE_CX

    if not api_key or not cx:
        return Response({"error": "Google API key or CX is not set"}, status=500)

    url = "https://www.googleapis.com/customsearch/v1"
    params = {"key": api_key, "cx": cx, "q": query}

    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()

        results = []
        for item in data.get("items", []):
            results.append(
                {
                    "title": item.get("title"),
                    "link": item.get("link"),
                    "snippet": item.get("snippet"),
                }
            )

        # Cache results for 1 hour
        redis_client.setex(cache_key, 3600, json.dumps(results))

        return Response({"query": query, "results": results})

    except requests.exceptions.RequestException as e:
        return Response({"error": f"API request failed: {str(e)}"}, status=500)
    except Exception as e:
        return Response({"error": str(e)}, status=500)
