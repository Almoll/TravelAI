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
        viable_places = []
        for place in places:
            price = random.randint(10, 50)  # Simulación de precios
            if price <= budget:
                viable_places.append({"name": place['name'], "price": price})

        # Limitar a 4 opciones y ordenar por precio ascendente
        viable_places = sorted(viable_places, key=lambda x: x['price'])[:4]

        if not viable_places:
            return "No hay lugares dentro del presupuesto."

        return {
            place["name"]: f"{place['price']} EUR"
            for place in viable_places
        }
    except Exception as e:
        print(f"Error al buscar restaurantes: {e}")
        return "Error al buscar bares/restaurantes."
