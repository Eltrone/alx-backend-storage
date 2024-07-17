#!/usr/bin/env python3
"""This module implements an expiring web cache and tracker using Redis."""

import requests
import redis
from functools import wraps

# Establish a connection to the Redis server
redis_client = redis.Redis()

def cache_and_track(url_function):
    """
    A decorator that caches web pages and tracks the number of times a URL
    has been accessed. It sets the cache to expire in 10 seconds.
    """
    @wraps(url_function)
    def wrapper(url):
        """Retrieve web content from cache or make a new request."""
        # Increment the access count each time the URL is requested
        count_key = f"count:{url}"
        redis_client.incr(count_key)
        
        # Check if the URL's content is already cached
        cached_key = f"cache:{url}"
        cached_content = redis_client.get(cached_key)
        if cached_content:
            return cached_content.decode('utf-8')
        
        # Fetch new content if not cached and cache it
        response = url_function(url)
        redis_client.setex(cached_key, 10, response)
        return response
    return wrapper

@cache_and_track
def get_page(url: str) -> str:
    """
    Fetch the HTML content of the specified URL and return it as a string.
    Uses the requests library to perform the HTTP request.
    """
    response = requests.get(url)
    return response.text

# Test example with a slow response URL
if __name__ == "__main__":
    test_url = "http://slowwly.robertomurray.co.uk/delay/3000/url/http://www.google.com"
    print(get_page(test_url))  # This request should fetch and cache
    print(get_page(test_url))  # This request should retrieve from cache
