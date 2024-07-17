#!/usr/bin/env python3
"""Module for implementing an expiring web cache and access tracker."""

import redis
import requests
from typing import Callable
from functools import wraps

# Create a Redis client
redis_client = redis.Redis()

def cache_response(func: Callable) -> Callable:
    """
    Decorator to cache the responses of web requests and track access frequency.
    """
    @wraps(func)
    def cache_wrapper(url: str) -> str:
        """Check cache or fetch web content, and track the access."""
        # Track access count for the given URL
        access_key = f"count:{url}"
        redis_client.incr(access_key)
        
        # Attempt to retrieve the cached content
        cache_key = f"cached:{url}"
        cached_content = redis_client.get(cache_key)
        if cached_content:
            return cached_content.decode('utf-8')
        
        # Fetch new content if not cached
        content = func(url)
        # Cache the new content with an expiration time (10 seconds)
        redis_client.setex(cache_key, 10, content)
        return content

    return cache_wrapper

@cache_response
def get_page(url: str) -> str:
    """
    Fetch and return the HTML content of the specified URL.
    Uses the requests library to perform the web request.
    """
    response = requests.get(url)
    return response.text

# Example usage
if __name__ == "__main__":
    test_url = "http://slowwly.robertomurray.co.uk/delay/3000/url/http://www.google.com"
    print(get_page(test_url))  # Should fetch and cache
    print(get_page(test_url))  # Should load from cache
    print(redis_client.get(f"count:{test_url}"))  # Displays the access count
