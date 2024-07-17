#!/usr/bin/env python3
"""
Test script for web caching and tracking functionality.
"""

import redis
import requests
from web import get_page  # Assurez-vous que cette importation est correcte

# Initialisation du client Redis
cache = redis.Redis()

if __name__ == "__main__":
    url_base = "http://slowwly.robertomurray.co.uk/delay/5000/url/"
    url_test = url_base + "http://www.google.com"

    # Tester la récupération de la page (devrait être lent la première fois)
    first_response = get_page(url_test)
    print("Première réponse récupérée.")

    # Tester si le cache fonctionne (devrait être rapide)
    second_response = get_page(url_test)
    print("Seconde réponse récupérée.")

    # Vérifier que les deux réponses sont identiques
    assert first_response == second_response, "Le cache ne fonctionne pas correctement."

    # Vérifier que le compteur d'accès indique 2
    access_count = int(cache.get(f"count:{url_test}").decode())
    assert access_count == 2, f"Le compteur d'accès devrait être 2, mais est {access_count}."

    print("Tests passés avec succès!")
