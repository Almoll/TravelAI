# user_input.py

def get_user_input():
    """Recopila la información inicial del usuario para planificar el viaje."""
    user_data = {}
    user_data['budget'] = int(input("¿Cuál es tu presupuesto total? "))
    user_data['origin'] = input("¿Desde qué ciudad deseas viajar? Ejemplo: Madrid=MAD ").upper()
    user_data['destination'] = input("¿A qué ciudad quieres viajar? Ejemplo: Paris=CDG ").upper()
    user_data['departure_date'] = input("¿En qué fecha deseas viajar? (YYYY-MM-DD) ")
    user_data['people'] = int(input("¿Cuántas personas van? "))
    user_data['days'] = int(input("¿Cuántos días durará el viaje? "))
    user_data['preferences'] = input("¿Qué tipo de actividades prefieres? (aventura, cultura, relax) ")
    return user_data
