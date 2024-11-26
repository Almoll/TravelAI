# amadeus_api.py

import requests

def get_amadeus_token():
    """Obtiene el token de autenticación para las APIs de Amadeus."""
    api_url = "https://test.api.amadeus.com/v1/security/oauth2/token"
    api_key = "t3OJUBBGaHxeLdrjvvYGN9F09QhQWLmv"
    api_secret = "AOeAhyD3tGGBr2xv"

    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "client_credentials",
        "client_id": api_key,
        "client_secret": api_secret
    }

    response = requests.post(api_url, headers=headers, data=data)
    response.raise_for_status()  # Asegurarse de que la solicitud fue exitosa
    return response.json()['access_token']


def search_flight_offers(destination_code, origin_code, departure_date, budget_per_person, token):
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

        unique_flights = {}
        for idx, flight in enumerate(flight_options[:5]):
            airline_code = flight['validatingAirlineCodes'][0]
            price = flight['price']['total']
            unique_flights[f"Vuelo {idx + 1} ({airline_code})"] = f"{price} €"

        return unique_flights
    except Exception as e:
        print(f"Error al buscar vuelos: {e}")
        return "No se pudo obtener las ofertas de vuelos."
