# restaurants.py

import random
import requests

def search_bars_and_restaurants(latitude, longitude, budget, token):
    api_url = "https://test.api.amadeus.com/v1/shopping/activities/by-square"
    params = {
        "north": latitude + 0.02,
        "south": latitude - 0.02,
        "east": longitude + 0.02,
        "west": longitude - 0.02,
        "category": "food-and-drink"
    }
    headers = {"Authorization": f"Bearer {token}"}

    try:
        response = requests.get(api_url, params=params, headers=headers)
        response.raise_for_status()
        response_data = response.json()

        places = response_data.get('data', [])
        viable_places = {}
        for place in places[:5]:
            price = random.randint(10, 50)
            if price <= budget:
                viable_places[place['name']] = f"{price} EUR"

        return viable_places if viable_places else "No hay lugares dentro del presupuesto."
    except Exception as e:
        print(f"Error al buscar restaurantes: {e}")
        return "Error al buscar bares/restaurantes."
