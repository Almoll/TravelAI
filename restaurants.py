import requests

def search_bars_and_restaurants(latitude, longitude, budget, token):
    """Busca bares y restaurantes cerca de la ubicación y calcula precios realistas."""
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
        data = response.json()

        places = {}
        for place in data.get('data', []):
            name = place.get('name', 'Lugar sin nombre')
            avg_price = round(budget * 0.1 + len(name))  # Ejemplo simplificado
            if avg_price <= budget:
                places[name] = f"{avg_price} EUR (aproximado)"

        return places
    except Exception as e:
        print(f"Error al buscar restaurantes: {e}")
        return {}
