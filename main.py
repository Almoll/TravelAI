from user_input import get_user_input
from authentication import get_amadeus_token, get_coordinates
from budget_allocation import allocate_budget
from flight_search import search_flight_offers
from accommodation_search import search_accommodation_options
from restaurants import search_bars_and_restaurants
from activities import search_activities_by_square

#las actividades dan restaurantes y tambien dan los restaurantes restaurantes preguntar chatgpt que solucione eso
def generate_daily_itinerary(day, activities, restaurants):
    """Genera un itinerario detallado para un día específico con múltiples restaurantes."""
    itinerary = []
    time_slots = ["9:00 AM", "12:00 PM", "3:00 PM", "6:00 PM", "8:00 PM"]
    
    # Asegurar que las actividades y los restaurantes sean diccionarios
    if not isinstance(activities, dict):
        activities = {}
    if not isinstance(restaurants, dict):
        restaurants = {}

    activities_list = list(activities.items())[:2]  # Máximo 2 actividades por día
    restaurants_list = list(restaurants.items())[:6]  # Máximo 6 restaurantes por día

    itinerary.append(f"Día {day}:")
    for i, time in enumerate(time_slots):
        if i % 2 == 0 and activities_list:  # Actividad en horario par
            activity = activities_list.pop(0)
            itinerary.append(f"   {time} - Actividad: {activity[0]} - {activity[1]['description']} ({activity[1]['price']})")
        elif restaurants_list:  # Restaurantes en horario impar
            itinerary.append(f"   {time} - Restaurantes recomendados:")
            for _ in range(3):  # Mostrar hasta 3 restaurantes por franja
                if restaurants_list:
                    restaurant = restaurants_list.pop(0)
                    itinerary.append(f"      - {restaurant[0]} ({restaurant[1]})")
    return itinerary




def create_itinerary(latitude, longitude, preferences, days, daily_budget, token):
    """Crea un itinerario completo con actividades y restaurantes."""
    activities = search_activities_by_square(latitude, longitude, preferences, token)
    restaurants = search_bars_and_restaurants(latitude, longitude, daily_budget, token)

    # Validar respuestas antes de pasar a generar el itinerario
    if not isinstance(activities, dict):
        print("No se encontraron actividades válidas.")
        activities = {}
    if not isinstance(restaurants, dict):
        print("No se encontraron restaurantes válidos.")
        restaurants = {}

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
    latitude, longitude = get_coordinates(user_data['destination'], token)
    if latitude is None or longitude is None:
        print("No se pudo determinar la ubicación del destino.")
        return

    itinerary = create_itinerary(
        latitude, longitude, user_data['preferences'], user_data['days'], 
        budget_allocation['daily_expenses'], token
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
