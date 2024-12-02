# flight_search.py
import requests

def search_flight_offers(destination_code, origin_code, departure_date, budget_per_person, token):
    """Busca ofertas de vuelos dentro del presupuesto del usuario."""
    api_url = "https://test.api.amadeus.com/v2/shopping/flight-offers"
    params = {
        "originLocationCode": origin_code,
        "destinationLocationCode": destination_code,
        "departureDate": departure_date,
        "adults": 1,
        "maxPrice": int(budget_per_person),
        "currencyCode": "EUR"
    }

    headers = {"Authorization": f"Bearer {token}"}

    try:
        response = requests.get(api_url, params=params, headers=headers)
        response.raise_for_status()
        response_data = response.json()

        flight_options = response_data.get('data', [])
        if not flight_options:
            return "No hay vuelos disponibles dentro de tu presupuesto."

        # Limitar a 5 vuelos
        unique_flights = {
            f"Vuelo {idx + 1}": f"{flight['price']['total']} €"
            for idx, flight in enumerate(flight_options[:5])
        }

        return unique_flights

    except Exception as e:
        print(f"Error al buscar vuelos: {e}")
        return "No se pudo obtener las ofertas de vuelos."
