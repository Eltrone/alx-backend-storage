#!/usr/bin/env python3
"""
Module pour la mise en cache expirante des pages web et le suivi des accès.
"""

import requests
import redis
from functools import wraps

# Initialisation du client Redis
cache = redis.Redis()


def cache_page(func):
    """
    Décorateur pour mettre en cache les résultats de la fonction get_page et
    compter les accès à chaque URL.
    """
    @wraps(func)
    def wrapper(url: str) -> str:
        # Incrémentation du compteur pour l'URL
        count_key = f"count:{url}"
        cache.incr(count_key)

        # Vérification si la page est déjà en cache
        cached_page = cache.get(url)
        if cached_page is not None:
            return cached_page.decode()

        # Appel de la fonction originale pour récupérer la page
        result = func(url)

        # Mise en cache du résultat avec une expiration de 10 secondes
        cache.setex(url, 10, result)
        return result
    return wrapper


@cache_page
def get_page(url: str) -> str:
    """
    Récupère le contenu HTML d'une URL spécifique.

    Args:
        url: L'URL de la page à récupérer.

    Returns:
        Le contenu HTML de la page.
    """
    response = requests.get(url)
    return response.text


# Pour tester le fonctionnement du cache et du compteur
if __name__ == "__main__":
    url_test = "http://slowwly.robertomurray.co.uk/delay/5000/url/http://www.google.com"
    print(get_page(url_test))  # Devrait charger lentement et être mis en cache
    print(get_page(url_test))  # Devrait être instantanément chargé du cache
    # Devrait indiquer que l'URL a été accédée deux fois
    print(cache.get(f"count:{url_test}").decode())
