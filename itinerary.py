import random
from activities import search_activities_by_square
from restaurants import search_bars_and_restaurants

def create_itinerary(latitude, longitude, preferences, days, daily_meal_budget, token):
    """Crea un itinerario diario con actividades y lugares para comer."""
    activities = search_activities_by_square(latitude, longitude, preferences, token)
    restaurants = search_bars_and_restaurants(latitude, longitude, daily_meal_budget, token)

    itinerary = []
    for day in range(1, days + 1):
        itinerary.append(f"Día {day}:")

        # Seleccionamos actividades
        if activities:
            activity_name, activity_info = activities.popitem()
            itinerary.append(f"   Actividad: {activity_name} - {activity_info['description']} (Precio: {activity_info['price']})")
        else:
            itinerary.append("   Actividad: Día libre.")

        # Seleccionamos restaurantes
        if restaurants:
            itinerary.append("   Restaurantes recomendados:")
            for _ in range(3):  # Mostrar hasta 3 restaurantes
                if restaurants:
                    restaurant_name, price = restaurants.popitem()
                    itinerary.append(f"      - {restaurant_name}: {price}")
        else:
            itinerary.append("   Restaurantes: No hay restaurantes disponibles.")

    return itinerary
