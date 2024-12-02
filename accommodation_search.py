# accommodation_search.py
import random

def search_accommodation_options(budget_per_night):
    """Simula opciones de alojamiento basadas en el presupuesto."""
    accommodations = [
        {'name': 'Hotel A', 'price': random.randint(100, 400)},
        {'name': 'Hostal B', 'price': random.randint(30, 100)},
        {'name': 'Airbnb C', 'price': random.randint(50, 200)}
    ]

    viable_accommodations = {
        acc['name']: f"{acc['price']} € por noche"
        for acc in accommodations if acc['price'] <= budget_per_night
    }

    return viable_accommodations if viable_accommodations else "No hay alojamientos dentro de tu presupuesto."
