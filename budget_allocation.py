# budget_allocation.py

def allocate_budget(budget, days, people):
    """Distribuye el presupuesto del usuario en transporte, alojamiento y gastos diarios."""
    transport_budget = 0.4 * budget  # 40% para transporte
    hotel_budget = 0.35 * budget  # 35% para alojamiento
    daily_expenses_budget = 0.25 * budget  # 25% para gastos diarios

    transport_per_person = transport_budget / people
    hotel_per_night = hotel_budget / days
    daily_expenses = daily_expenses_budget / days

    return {
        'transport_per_person': transport_per_person,
        'hotel_per_night': hotel_per_night,
        'daily_expenses': daily_expenses
    }
