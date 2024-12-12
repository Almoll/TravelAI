import requests

def search_activities_by_square(latitude, longitude, preferences, token):
    """Busca actividades culturales, de aventura o relajación en el área."""
    
    # Mapeo de categorías de actividades para las preferencias
    activity_categories = {
        'aventura': ['outdoor', 'adventure', 'extreme-sports', 'hiking'],
        'cultura': ['sightseeing', 'cultural', 'museums', 'history', 'art', 'landmark'],
        'relax': ['wellness', 'spas', 'meditation', 'yoga']
    }
    
    selected_category = activity_categories.get(preferences, [])

    if not selected_category:
        return {}

    api_url = "https://test.api.amadeus.com/v1/shopping/activities/by-square"
    params = {
        "north": latitude + 0.1,
        "south": latitude - 0.1,
        "east": longitude + 0.1,
        "west": longitude - 0.1,
        "category": ','.join(selected_category)
    }
    headers = {"Authorization": f"Bearer {token}"}

    try:
        response = requests.get(api_url, params=params, headers=headers)
        response.raise_for_status()
        response_data = response.json()

        activities = response_data.get('data', [])
        if not activities:
            return {}

        # Filtrar actividades no deseadas (por ejemplo, relacionadas con comida)
        filtered_activities = {}
        for activity in activities:
            name = activity.get('name', 'Actividad sin nombre')
            description = activity.get('shortDescription', 'Descripción no disponible')
            price = activity.get('price', {}).get('total', 'Precio no disponible')
            
            # Filtramos lugares relacionados con comida
            if "food" in name.lower() or "restaurant" in name.lower():
                continue  # Ignoramos los lugares relacionados con comida

            filtered_activities[name] = {
                'description': description,
                'price': price
            }

        return filtered_activities
    except Exception as e:
        print(f"Error al buscar actividades: {e}")
        return {}
