# itinerary.py

import random
from restaurants import search_bars_and_restaurants
from activities import search_activities_by_square

def create_itinerary(latitude, longitude, preferences, days, daily_meal_budget, token):
    print("Generando itinerario detallado...")
    activities = search_activities_by_square(latitude, longitude, preferences, token)

    if isinstance(activities, str):
        print(activities)
        return []

    itinerary = []
    available_activities = list(activities.items())

    def get_activity_duration():
        return random.randint(1, 4)

    for day in range(1, days + 1):
        daily_schedule = f"Día {day}:\n"
        current_time = 9

        while current_time < 18:
            if available_activities:
                activity_name, description = random.choice(available_activities)
                duration = get_activity_duration()

                start_time = f"{current_time}:00"
                end_time = f"{current_time + duration}:00"
                daily_schedule += f"  {start_time} - {end_time}: {activity_name}\n"

                current_time += duration
                if current_time < 18:
                    daily_schedule += f"  {current_time}:00 - {current_time + 2}:00: Tiempo para comer\n"
                    places = search_bars_and_restaurants(latitude, longitude, daily_meal_budget, token)
                    if isinstance(places, dict):
                        for place, price in places.items():
                            daily_schedule += f"    Opción: {place} - {price}\n"
                    else:
                        daily_schedule += f"    {places}\n"
                    current_time += 2
                available_activities.remove((activity_name, description))
            else:
                daily_schedule += f"  {current_time}:00 - 18:00: Día libre\n"
                break

        itinerary.append(daily_schedule)

    return itinerary
