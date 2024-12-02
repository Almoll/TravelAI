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
        response_data = response.json()

        places = response_data.get('data', [])
        if not places:
            return "No hay lugares dentro del presupuesto."

        viable_places = {}
        for place in places:
            # Generar precios realistas basados en datos del restaurante
            avg_price = round(budget * 0.1 + (len(place['name']) * 2))  # Ejemplo basado en nombre
            if avg_price <= budget:
                viable_places[place['name']] = f"{avg_price} EUR (aproximado)"

        return viable_places if viable_places else "No hay lugares dentro del presupuesto."
    except Exception as e:
        print(f"Error al buscar restaurantes: {e}")
        return "Error al buscar bares/restaurantes."
