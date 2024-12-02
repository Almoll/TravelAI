import requests

def search_activities_by_square(latitude, longitude, preferences, token):
    """Busca actividades dentro de un área geográfica basada en preferencias del usuario."""
    
    # Mapeo de categorías de actividades para las preferencias
    activity_categories = {
        'aventura': ['outdoor', 'adventure', 'extreme-sports', 'hiking'],
        'cultura': ['sightseeing', 'cultural', 'museums', 'history', 'art'],
        'relax': ['wellness', 'spas', 'meditation', 'yoga']
    }
    
    selected_category = activity_categories.get(preferences, [])

    # Si no se encuentra una categoría, retornamos un mensaje de error
    if not selected_category:
        return "No se encontraron actividades que coincidan con tus preferencias."

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
            return "No se encontraron actividades según tus preferencias."

        # Filtrar las actividades y mostrar un máximo de 4 actividades
        viable_activities = {}
        for activity in activities[:4]:  # Mostrar hasta 4 actividades
            name = activity.get('name', 'Actividad sin nombre')
            description = activity.get('shortDescription', 'Descripción no disponible')
            price = activity.get('price', {}).get('total', 'Precio no disponible')

            # Mostrar el nombre de la actividad con la descripción y el precio
            viable_activities[name] = {
                'description': description,
                'price': price
            }

        return viable_activities
    except Exception as e:
        print(f"Error al buscar actividades: {e}")
        return "No se pudo obtener las actividades."
