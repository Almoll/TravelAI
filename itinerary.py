# itinerary.py
import random
from retry_helper import make_amadeus_request_with_retry

def create_itinerary(latitude, longitude, preferences, days, daily_meal_budget, token):
    """Crea un itinerario diario con actividades y lugares para comer."""
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

    response_data = make_amadeus_request_with_retry(api_url, params, headers)
    activities = response_data.get('data', []) if response_data else []
    itinerary = []

    for day in range(1, days + 1):
        if activities:
            selected = random.choice(activities)
            itinerary.append(f"Día {day}: {selected['name']} - {selected.get('shortDescription', 'Sin descripción')}")
        else:
            itinerary.append(f"Día {day}: Día libre.")

    return itinerary
