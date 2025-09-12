
# **Smart Shopper Project Report**

## 1. **Problem Overview**

The goal was to build a **real-time product search API**. Users could type a product name (e.g., "Peanut Butter") and receive structured product information (name, brand, price, weight, link) instantly.

Key requirements included:

* Fast response time.
* Scalability using caching.
* Exposure as a Django API for any client.

---

## 2. **Approach**

1. **Backend Setup**:

   * Created a Django project with an app `products`.
   * Set up Django Rest Framework for API endpoints.
   * Installed and configured Redis for caching frequent queries.

2. **Google API Integration**:

   * Used **Google Custom Search API** to fetch real-time product data.
   * Stored API keys and Custom Search Engine ID in a `.env` file to keep credentials secure.

3. **Caching Strategy**:

   * Checked Redis first for cached queries.
   * If a query was not cached, fetched from Google API and then stored the results in Redis (TTL: 1 hour).
   * Ensured repeated queries returned instantly from cache.

4. **Fallback Data (Mock Data)**:

   * If Google API failed (rate limit or disabled), returned mock product data to ensure API always responded.

5. **API Endpoint**:

   * `GET /api/search/?q=<product_name>`
   * Returns JSON with `query` and `results` (list of products).

---

## 3. **Solution Details**

* **Caching**: Used Redis to store queries and results as JSON strings. This significantly improved response time for repeated queries.
* **Error Handling**: Added fallback to mock data and logs for cache hits/misses.
* **Environment Variables**: API keys, secret keys, and Redis URL stored in `.env` and loaded via `python-decouple`.
* **JSON Output Structure**:

```json
{
  "query": "Peanut Butter",
  "results": [
    {
      "name": "365 WholeFoods Peanut Butter",
      "brand": "WholeFoods",
      "price_usd": "$5.99",
      "price_inr": "₹527",
      "weight": "500g",
      "link": "https://example.com/product1"
    }
  ]
}
```

* **Development Tools**:

  * Django 5.x
  * Django Rest Framework
  * Redis
  * Google Custom Search API
  * Python 3.10

---

## 4. **Challenges Faced & Solutions**

| Challenge                                              | Solution                                                                                  |
| ------------------------------------------------------ | ----------------------------------------------------------------------------------------- |
| Google API often returned `403` or was disabled        | Implemented fallback mock data to ensure API response continuity                          |
| Redis cache returned strings not in proper JSON format | Used `json.dumps`/`json.loads` for proper serialization and deserialization               |
| Secure storage of API keys                             | Stored in `.env` file, loaded with `python-decouple` instead of hardcoding                |
| Git repo misalignment                                  | Moved `.git` folder to correct project folder and resolved merge conflicts                |
| Displaying product info in a structured format         | Created a transformation function to format API results into `name, brand, price, weight` |

---

## 5. **Improvements / Experiments for the Future**

1. **Enhanced Google API parsing**:

   * Automatically parse prices, weight, and brand from Google Shopping results using more advanced scraping techniques.
2. **Async Requests**:

   * Use `asyncio` or `aiohttp` to fetch multiple API calls concurrently for faster response.
3. **Pagination & Limit**:

   * Allow users to fetch more results with `page` and `limit` query parameters.
4. **Rate Limiting & Queueing**:

   * Implement throttling and queuing to handle multiple users without hitting Google API rate limits.
5. **UI Integration**:

   * Build a simple web UI to search and display results in product cards instead of raw JSON.
6. **Caching Optimization**:

   * Implement smarter cache eviction strategies or store partial results for similar queries.

---

## 6. **Conclusion**

The **Smart Shopper API** successfully:

* Provides **real-time product information**.
* Responds quickly thanks to **Redis caching**.
* Is scalable and secure with proper **API key management**.
* Handles failures gracefully using **mock data**.

With additional time, the project can be extended to support richer data, user interface, and more advanced optimizations.

---
