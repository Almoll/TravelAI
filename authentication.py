# authentication.py
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
    response.raise_for_status()
    return response.json()['access_token']


def get_coordinates(city_code, token):
    """Convierte un código de ciudad en coordenadas (latitud y longitud)."""
    api_url = "https://test.api.amadeus.com/v1/reference-data/locations"
    params = {
        "keyword": city_code,
        "subType": "CITY"
    }
    headers = {"Authorization": f"Bearer {token}"}

    try:
        response = requests.get(api_url, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()
        if 'data' in data and len(data['data']) > 0:
            location = data['data'][0]['geoCode']
            return location['latitude'], location['longitude']
        else:
            print("No se encontraron coordenadas para el código de ciudad.")
            return None, None
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener coordenadas: {e}")
        return None, None
