# products/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests, re, json
import redis
from decouple import config

# --- Load from .env ---
GOOGLE_API_KEY = config("GOOGLE_API_KEY")
SEARCH_ENGINE_ID = config("GOOGLE_CX")
REDIS_URL = config("REDIS_URL", default="redis://127.0.0.1:6379/0")

# --- Redis setup ---
redis_client = redis.Redis.from_url(REDIS_URL)

def clean_query(q):
    return re.sub(r'\s+', ' ', q.strip()).lower()

# Mock data (used if API fails)
mock_products = [
    {"name": "365 WholeFoods Peanut Butter", "brand": "WholeFoods", "price_usd": "$5.99", "price_inr": "₹527", "weight": "500g", "link": "https://example.com/product1"},
    {"name": "Organic Peanut Butter", "brand": "Organic Co", "price_usd": "$6.49", "price_inr": "₹571", "weight": "400g", "link": "https://example.com/product2"},
]

@api_view(["GET"])
def search_products(request):
    query = request.GET.get("q", "")
    if not query:
        return Response({"error": "Please provide a search term"}, status=400)

    query = clean_query(query)

    # --------------------------
    # 1. Check Redis cache first
    # --------------------------
    cached = redis_client.get(query)
    if cached:
        print(f"Cache hit for query: {query}")
        return Response({"query": query, "results": json.loads(cached)})

    print(f"Cache miss for query: {query}")

    # --------------------------
    # 2. Call Google API
    # --------------------------
    url = "https://www.googleapis.com/customsearch/v1"
    params = {"key": GOOGLE_API_KEY, "cx": SEARCH_ENGINE_ID, "q": query}
    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        items = data.get("items", [])

        # Structure the output: name, brand, price, weight, link
        results = []
        for item in items:
            # If available, parse from item['pagemap'] for Google Shopping data
            results.append({
                "name": item.get("title"),
                "brand": item.get("pagemap", {}).get("brand", ["Unknown"])[0] if item.get("pagemap") else "Unknown",
                "price_usd": item.get("pagemap", {}).get("offer", [{}])[0].get("price", "Unknown") if item.get("pagemap") else "Unknown",
                "price_inr": "Unknown",  # You can convert using a currency API
                "weight": item.get("pagemap", {}).get("product", [{}])[0].get("weight", "Unknown") if item.get("pagemap") else "Unknown",
                "link": item.get("link")
            })
    except Exception as e:
        print(f"Google API error: {e}")
        results = mock_products

    # --------------------------
    # 3. Cache results in Redis
    # --------------------------
    redis_client.set(query, json.dumps(results), ex=3600)  # expires in 1 hour
    print(f"Cache set for query: {query}")

    return Response({"query": query, "results": results})
