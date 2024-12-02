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
    response.raise_for_status()  # Asegurarse de que la solicitud fue exitosa
    return response.json()['access_token']
