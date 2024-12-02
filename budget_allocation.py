def allocate_budget(total_budget, days, people):
    """Distribuye el presupuesto total."""
    per_person = total_budget // people
    daily_budget = per_person // days

    return {
        'transport_per_person': per_person * 0.3,
        'hotel_per_night': daily_budget * 0.5,
        'daily_expenses': daily_budget * 0.2
    }
