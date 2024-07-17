#!/usr/bin/env python3
"""Implementing an expiring web cache and tracker."""

import requests
import redis
from functools import wraps

client = redis.Redis()

def cache(func):
    """Decorator to cache web pages with an expiration time."""
    @wraps(func)
    def wrapper(url):
        """Check the cache first before fetching the URL."""
        cached_page = client.get(url)
        if cached_page:
            return cached_page.decode('utf-8')
        html_content = func(url)
        client.setex(url, 10, html_content)  # Cache expiration set to 10 seconds
        return html_content
    return wrapper

def count_url_calls(func):
    """Decorator to track how many times a URL has been accessed."""
    @wraps(func)
    def wrapper(url):
        """Increment the count every time the URL is fetched."""
        count_key = f"count:{url}"
        client.incr(count_key)
        return func(url)
    return wrapper

@cache
@count_url_calls
def get_page(url: str) -> str:
    """Fetch HTML content of a URL."""
    response = requests.get(url)
    return response.text

# Example usage
if __name__ == "__main__":
    url = "http://slowwly.robertomurray.co.uk/delay/3000/url/http://www.google.com"
    print(get_page(url))
    print(get_page(url))  # This second call should fetch the result from the cache
    print(client.get(f"count:{url}"))  # Displays the count of how many times the URL was accessed
