# main.py

from amadeus_api import get_amadeus_token, search_flight_offers
from activities import search_activities_by_square
from restaurants import search_bars_and_restaurants
from itinerary import create_itinerary

def run_travel_planner():
    # Datos del usuario (puedes mejorarlo con inputs)
    user_data = {
        'budget': 1000,
        'origin': "MAD",
        'destination': "CDG",
        'departure_date': "2024-12-01",
        'people': 2,
        'days': 3,
        'preferences': 'cultura'
    }
    token = get_amadeus_token()
    latitude, longitude = 48.8566, 2.3522  # Coordenadas de París (como ejemplo)

    budget_allocation = {'transport_per_person': 400, 'hotel_per_night': 100, 'daily_expenses': 50}
    transport_options = search_flight_offers(user_data['destination'], user_data['origin'], user_data['departure_date'], budget_allocation['transport_per_person'], token)
    itinerary = create_itinerary(latitude, longitude, user_data['preferences'], user_data['days'], budget_allocation['daily_expenses'], token)

    print("\n--- Opciones de Transporte ---")
    print(transport_options)
    print("\n--- Itinerario Sugerido ---")
    for day_plan in itinerary:
        print(day_plan)

if __name__ == "__main__":
    run_travel_planner()
