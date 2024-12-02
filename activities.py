# activities.py

import requests

def search_activities_by_square(latitude, longitude, preferences, token):
    api_url = "https://test.api.amadeus.com/v1/shopping/activities/by-square"
    activity_categories = {
        'aventura': ['outdoor', 'adventure'],
        'cultura': ['sightseeing', 'cultural'],
        'relax': ['relax', 'wellness']
    }
    selected_category = activity_categories.get(preferences, [])

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

        viable_activities = [
            {"name": activity['name'], "description": activity.get('shortDescription', 'Descripción no disponible')}
            for activity in activities
        ]

        # Limitar a 4 actividades y ordenar alfabéticamente por nombre
        viable_activities = sorted(viable_activities, key=lambda x: x['name'])[:4]

        return {
            activity["name"]: activity["description"]
            for activity in viable_activities
        }
    except Exception as e:
        print(f"Error al buscar actividades: {e}")
        return "No se pudo obtener las actividades."
