from user_input import get_user_input
from authentication import get_amadeus_token
from budget_allocation import allocate_budget
from flight_search import search_flight_offers
from accommodation_search import search_accommodation_options
from restaurants import search_bars_and_restaurants
from activities import search_activities_by_square
import requests

def get_city_coordinates(city_name, token):
    """Obtiene las coordenadas de una ciudad usando la API de OpenCage."""
    api_url = f"https://api.opencagedata.com/geocode/v1/json"
    api_key = "tu_api_key_aqui"  # Reemplaza con tu API Key
    params = {
        "q": city_name,
        "key": api_key
    }
    response = requests.get(api_url, params=params)
    data = response.json()
    
    if data['results']:
        lat = data['results'][0]['geometry']['lat']
        lng = data['results'][0]['geometry']['lng']
        return lat, lng
    else:
        print(f"No se pudieron obtener coordenadas para {city_name}")
        return None, None


def generate_daily_itinerary(day, activities, restaurants):
    """Genera un itinerario detallado para un día específico con múltiples restaurantes."""
    itinerary = []
    time_slots = ["9:00 AM", "12:00 PM", "3:00 PM", "6:00 PM", "8:00 PM"]
    activities_list = list(activities.items())[:2]  # Máximo 2 actividades por día
    restaurants_list = list(restaurants.items())[:6]  # Máximo 6 restaurantes por día

    itinerary.append(f"Día {day}:")
    for i, time in enumerate(time_slots):
        if i % 2 == 0 and activities_list:  # Actividad en horario par
            activity = activities_list.pop(0)
            itinerary.append(f"   {time} - Actividad: {activity[0]} - {activity[1]}")
        elif restaurants_list:  # Restaurantes en horario impar
            itinerary.append(f"   {time} - Restaurantes recomendados:")
            for _ in range(3):  # Mostrar hasta 3 restaurantes por franja
                if restaurants_list:
                    restaurant = restaurants_list.pop(0)
                    itinerary.append(f"      - {restaurant[0]} ({restaurant[1]})")
    return itinerary


def create_itinerary(city_name, preferences, days, daily_budget, token):
    """Crea un itinerario completo con actividades y restaurantes."""
    
    # Obtener coordenadas de la ciudad
    latitude, longitude = get_city_coordinates(city_name, token)
    if latitude is None or longitude is None:
        return []

    # Obtener actividades y restaurantes según las coordenadas y preferencias
    activities = search_activities_by_square(latitude, longitude, preferences, token)
    restaurants = search_bars_and_restaurants(latitude, longitude, daily_budget, token)

    full_itinerary = []
    for day in range(1, days + 1):
        daily_plan = generate_daily_itinerary(day, activities, restaurants)
        full_itinerary.extend(daily_plan)

    return full_itinerary


def run_travel_planner():
    user_data = get_user_input()
    token = get_amadeus_token()

    budget_allocation = allocate_budget(user_data['budget'], user_data['days'], user_data['people'])
    transport_options = search_flight_offers(
        user_data['destination'], user_data['origin'], user_data['departure_date'],
        budget_allocation['transport_per_person'], token
    )
    accommodation_options = search_accommodation_options(budget_allocation['hotel_per_night'])
    
    # Crear itinerario con ciudad dinámica
    itinerary = create_itinerary(
        user_data['destination'], user_data['preferences'], user_data['days'], budget_allocation['daily_expenses'], token
    )

    print("\n--- Resultados ---")
    print("\n1. Distribución del Presupuesto:")
    for key, value in budget_allocation.items():
        print(f"   {key.capitalize()}: {value:.2f} EUR")

    print("\n2. Vuelos Disponibles:")
    for flight, price in transport_options.items():
        print(f"   {flight}: {price}")

    print("\n3. Opciones de Alojamiento:")
    for hotel, price in accommodation_options.items():
        print(f"   {hotel}: {price}")

    print("\n4. Itinerario Detallado:")
    for line in itinerary:
        print(line)


if __name__ == "__main__":
    run_travel_planner()
