# main.py

from user_input import get_user_input
from authentication import get_amadeus_token
from budget_allocation import allocate_budget
from flight_search import search_flight_offers
from accommodation_search import search_accommodation_options
from itinerary import create_itinerary
from recommendations import add_recommendations_to_itinerary
from route_planner import generate_routes
from itinerary_format import format_itinerary_chronologically

def run_travel_planner():
    user_data = get_user_input()
    token = get_amadeus_token()

    # Asignación del presupuesto
    budget_allocation = allocate_budget(user_data['budget'], user_data['days'], user_data['people'])

    # Búsqueda de transporte
    transport_options = search_flight_offers(
        user_data['destination'], user_data['origin'], user_data['departure_date'],
        budget_allocation['transport_per_person'], token
    )

    # Búsqueda de alojamiento
    accommodation_options = search_accommodation_options(budget_allocation['hotel_per_night'])

    # Generar itinerario
    itinerary = create_itinerary(48.8566, 2.3522, user_data['preferences'], user_data['days'], budget_allocation['daily_expenses'], token)

    # Añadir recomendaciones
    food_options = {'Le Marais': 'Restaurante gourmet', 'Chez Nous': 'Cocina local'}
    enriched_itinerary = add_recommendations_to_itinerary(itinerary, transport_options, food_options)

    # Generar rutas y optimización
    routes = generate_routes(itinerary, starting_point="Hotel")
    formatted_itinerary = format_itinerary_chronologically(enriched_itinerary)

    # Mostrar resultados
    print("\n--- Resultados ---")
    print("Distribución del Presupuesto:", budget_allocation)
    print("Vuelos:", transport_options)
    print("Alojamiento:", accommodation_options)
    print("Rutas optimizadas:\n", routes)
    print("\nItinerario final:\n", formatted_itinerary)

if __name__ == "__main__":
    run_travel_planner()
