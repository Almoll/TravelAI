def search_flight_offers(destination, origin, departure_date, max_budget, token):
    """Simula la búsqueda de ofertas de vuelo."""
    return [
        {'origin': origin, 'destination': destination, 'price': max_budget * 0.9, 'date': departure_date}
    ]
