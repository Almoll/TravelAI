# retry_helper.py
import requests
import time

def make_amadeus_request_with_retry(api_url, params, headers, retries=3, backoff_factor=1):
    """Realiza solicitudes a Amadeus con reintentos en caso de error."""
    for attempt in range(retries):
        try:
            response = requests.get(api_url, params=params, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            if response.status_code == 429 and attempt < retries - 1:
                wait_time = backoff_factor * (2 ** attempt)
                print(f"Demasiadas solicitudes. Reintentando en {wait_time} segundos...")
                time.sleep(wait_time)
            else:
                print(f"Error HTTP: {http_err}")
                print(f"Contenido de respuesta: {response.text}")
                return None
        except Exception as e:
            print(f"Error: {e}")
            return None
