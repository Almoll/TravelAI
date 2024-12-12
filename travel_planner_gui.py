import tkinter as tk
from tkinter import messagebox
from authentication import get_amadeus_token, get_coordinates
from budget_allocation import allocate_budget
from flight_search import search_flight_offers
from accommodation_search import search_accommodation_options
from restaurants import search_bars_and_restaurants
from activities import search_activities_by_square
import sqlite3

# --- Database Setup ---
def setup_database():
    conn = sqlite3.connect("travel_planner.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS trips (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        trip_name TEXT NOT NULL,
        details TEXT NOT NULL,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)
    conn.commit()
    conn.close()

setup_database()

# --- Helper Functions ---
def register_user(username, email, password):
    conn = sqlite3.connect("travel_planner.db")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", (username, email, password))
        conn.commit()
        messagebox.showinfo("Registro exitoso", "Usuario registrado correctamente.")
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "El usuario o el correo ya existen.")
    conn.close()

def login_user(email, password):
    conn = sqlite3.connect("travel_planner.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, username FROM users WHERE email = ? AND password = ?", (email, password))
    user = cursor.fetchone()
    conn.close()
    return user

def save_trip(user_id, trip_name, details):
    conn = sqlite3.connect("travel_planner.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO trips (user_id, trip_name, details) VALUES (?, ?, ?)", (user_id, trip_name, details))
    conn.commit()
    conn.close()

def get_user_trips(user_id):
    conn = sqlite3.connect("travel_planner.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, trip_name, details FROM trips WHERE user_id = ?", (user_id,))
    trips = cursor.fetchall()
    conn.close()
    return trips

# --- GUI Functions ---
def show_main_screen():
    root = tk.Tk()
    root.title("Travel Planner")

    def guest_mode():
        root.destroy()
        show_trip_planner(None)

    def login_mode():
        root.destroy()
        show_login_screen()

    tk.Label(root, text="Bienvenido a Travel Planner", font=("Arial", 16)).pack(pady=20)
    tk.Button(root, text="Entrar como Invitado", command=guest_mode).pack(pady=10)
    tk.Button(root, text="Iniciar Sesión / Registrarse", command=login_mode).pack(pady=10)

    root.mainloop()

def show_login_screen():
    login_screen = tk.Tk()
    login_screen.title("Iniciar Sesión / Registrarse")

    tk.Label(login_screen, text="Email:").grid(row=0, column=0)
    email_entry = tk.Entry(login_screen)
    email_entry.grid(row=0, column=1)

    tk.Label(login_screen, text="Contraseña:").grid(row=1, column=0)
    password_entry = tk.Entry(login_screen, show="*")
    password_entry.grid(row=1, column=1)

    def login():
        email = email_entry.get()
        password = password_entry.get()
        user = login_user(email, password)
        if user:
            login_screen.destroy()
            show_user_dashboard(user)
        else:
            messagebox.showerror("Error", "Credenciales incorrectas.")

    def show_register_screen():
        login_screen.destroy()
        show_registration_screen()

    tk.Button(login_screen, text="Iniciar Sesión", command=login).grid(row=2, column=0, columnspan=2, pady=10)
    tk.Button(login_screen, text="Registrarse", command=show_register_screen).grid(row=3, column=0, columnspan=2)

    login_screen.mainloop()

def show_registration_screen():
    register_screen = tk.Tk()
    register_screen.title("Registrarse")

    tk.Label(register_screen, text="Nombre de Usuario:").grid(row=0, column=0)
    username_entry = tk.Entry(register_screen)
    username_entry.grid(row=0, column=1)

    tk.Label(register_screen, text="Email:").grid(row=1, column=0)
    email_entry = tk.Entry(register_screen)
    email_entry.grid(row=1, column=1)

    tk.Label(register_screen, text="Contraseña:").grid(row=2, column=0)
    password_entry = tk.Entry(register_screen, show="*")
    password_entry.grid(row=2, column=1)

    def register():
        username = username_entry.get()
        email = email_entry.get()
        password = password_entry.get()
        register_user(username, email, password)
        register_screen.destroy()
        show_login_screen()

    tk.Button(register_screen, text="Registrar", command=register).grid(row=3, column=0, columnspan=2, pady=10)

    register_screen.mainloop()

def show_user_dashboard(user):
    dashboard = tk.Tk()
    dashboard.title("Panel de Usuario")

    user_id, username = user
    tk.Label(dashboard, text=f"Bienvenido, {username}", font=("Arial", 16)).pack(pady=10)

    def plan_trip():
        dashboard.destroy()
        show_trip_planner(user_id)

    def view_trips():
        trips = get_user_trips(user_id)
        if trips:
            trip_screen = tk.Toplevel(dashboard)
            trip_screen.title("Tus Viajes")
            for trip_id, trip_name, details in trips:
                tk.Label(trip_screen, text=f"{trip_name}: {details}").pack()
        else:
            messagebox.showinfo("Sin viajes", "No tienes viajes guardados.")

    tk.Button(dashboard, text="Planificar un Viaje", command=plan_trip).pack(pady=10)
    tk.Button(dashboard, text="Ver Mis Viajes", command=view_trips).pack(pady=10)

    dashboard.mainloop()

def show_trip_planner(user_id):
    planner = tk.Tk()
    planner.title("Planificador de Viajes")

    tk.Label(planner, text="Presupuesto (EUR):").grid(row=0, column=0)
    budget_entry = tk.Entry(planner)
    budget_entry.grid(row=0, column=1)

    tk.Label(planner, text="Origen (Código IATA):").grid(row=1, column=0)
    origin_entry = tk.Entry(planner)
    origin_entry.grid(row=1, column=1)

    tk.Label(planner, text="Destino (Código IATA):").grid(row=2, column=0)
    destination_entry = tk.Entry(planner)
    destination_entry.grid(row=2, column=1)

    tk.Label(planner, text="Fecha de Salida (YYYY-MM-DD):").grid(row=3, column=0)
    departure_date_entry = tk.Entry(planner)
    departure_date_entry.grid(row=3, column=1)

    tk.Label(planner, text="Número de Personas:").grid(row=4, column=0)
    people_entry = tk.Entry(planner)
    people_entry.grid(row=4, column=1)

    tk.Label(planner, text="Días de Viaje:").grid(row=5, column=0)
    days_entry = tk.Entry(planner)
    days_entry.grid(row=5, column=1)

    tk.Label(planner, text="Preferencias (aventura, cultura, relax):").grid(row=6, column=0)
    preferences_entry = tk.Entry(planner)
    preferences_entry.grid(row=6, column=1)

    def plan_trip():
       try:
           budget = int(budget_entry.get())
           origin = origin_entry.get().upper()
           destination = destination_entry.get().upper()
           departure_date = departure_date_entry.get()
           people = int(people_entry.get())
           days = int(days_entry.get())
           preferences = preferences_entry.get()
    
           # Token y asignación de presupuesto
           token = get_amadeus_token()
           budget_allocation = allocate_budget(budget, days, people)
    
           # Opciones de transporte
           transport_options = search_flight_offers(destination, origin, departure_date, budget_allocation['transport_per_person'], token)
           if not transport_options:
               transport_options = ["No se encontraron opciones de vuelo."]
    
           # Opciones de alojamiento
           accommodation_options = search_accommodation_options(budget_allocation['hotel_per_night'])
           if not accommodation_options:
               accommodation_options = ["No se encontraron opciones de alojamiento."]
    
           # Coordenadas e itinerario
           latitude, longitude = get_coordinates(destination, token)
           itinerary = create_itinerary(
               latitude, longitude, preferences, days,
               budget_allocation['daily_expenses'], token
           )
           if not itinerary:
               itinerary = ["No se pudo generar el itinerario."]
    
           # Mostrar resultados en una nueva ventana
           result_screen = tk.Toplevel(planner)
           result_screen.title("Resultados del Viaje")
    
           tk.Label(result_screen, text="Resultados del Viaje", font=("Arial", 16)).pack(pady=10)
    
           # Mostrar vuelos
           tk.Label(result_screen, text="Opciones de Vuelo:", font=("Arial", 12, "bold")).pack(anchor="w", padx=10)
           flights_text = tk.Text(result_screen, wrap=tk.WORD, height=8, width=80)
           flights_text.pack(pady=5)
           flights_text.insert(tk.END, "\n".join(transport_options))
           flights_text.config(state=tk.DISABLED)
    
           # Mostrar hoteles
           tk.Label(result_screen, text="Opciones de Alojamiento:", font=("Arial", 12, "bold")).pack(anchor="w", padx=10)
           hotels_text = tk.Text(result_screen, wrap=tk.WORD, height=8, width=80)
           hotels_text.pack(pady=5)
           hotels_text.insert(tk.END, "\n".join(accommodation_options))
           hotels_text.config(state=tk.DISABLED)
    
           # Mostrar itinerario
           tk.Label(result_screen, text="Itinerario Generado:", font=("Arial", 12, "bold")).pack(anchor="w", padx=10)
           itinerary_text = tk.Text(result_screen, wrap=tk.WORD, height=15, width=80)
           itinerary_text.pack(pady=5)
           itinerary_text.insert(tk.END, "\n".join(itinerary))
           itinerary_text.config(state=tk.DISABLED)
    
           # Botón para regresar
           def go_back():
               result_screen.destroy()
    
           tk.Button(result_screen, text="Atrás", command=go_back).pack(pady=10)
    
           # Guardar viaje si hay usuario
           if user_id:
               trip_name = f"Viaje a {destination} ({departure_date})"
               save_trip(user_id, trip_name, "\n".join(itinerary))
               messagebox.showinfo("Viaje Guardado", "Tu viaje ha sido guardado exitosamente.")
    
       except Exception as e:
           messagebox.showerror("Error", f"Ha ocurrido un error: {str(e)}")
    
    
       def go_back():
           planner.destroy()
           if user_id:
               show_user_dashboard((user_id, "Usuario"))
           else:
               show_main_screen()
    
       tk.Button(planner, text="Planificar", command=plan_trip).grid(row=7, column=0, columnspan=2, pady=10)
       tk.Button(planner, text="Atrás", command=go_back).grid(row=8, column=0, columnspan=2)
    
       planner.mainloop()
    def go_back():
        planner.destroy()
        if user_id:
            show_user_dashboard((user_id, "Usuario"))
        else:
            show_main_screen()

    tk.Button(planner, text="Planificar", command=plan_trip).grid(row=7, column=0, columnspan=2, pady=10)
    tk.Button(planner, text="Atrás", command=go_back).grid(row=8, column=0, columnspan=2)

    planner.mainloop()


def create_itinerary(latitude, longitude, preferences, days, daily_budget, token):
    activities = search_activities_by_square(latitude, longitude, preferences, token)
    restaurants = search_bars_and_restaurants(latitude, longitude, daily_budget, token)

    full_itinerary = []
    for day in range(1, days + 1):
        daily_plan = generate_daily_itinerary(day, activities, restaurants)
        full_itinerary.extend(daily_plan)

    return full_itinerary

def generate_daily_itinerary(day, activities, restaurants):
    itinerary = []
    time_slots = ["9:00 AM", "12:00 PM", "3:00 PM", "6:00 PM", "8:00 PM"]
    activities_list = list(activities.items())[:2]
    restaurants_list = list(restaurants.items())[:6]

    itinerary.append(f"Día {day}:")
    for i, time in enumerate(time_slots):
        if i % 2 == 0 and activities_list:
            activity = activities_list.pop(0)
            itinerary.append(f"   {time} - Actividad: {activity[0]} - {activity[1]}")
        elif restaurants_list:
            itinerary.append(f"   {time} - Restaurantes recomendados:")
            for _ in range(3):
                if restaurants_list:
                    restaurant = restaurants_list.pop(0)
                    itinerary.append(f"      - {restaurant[0]} ({restaurant[1]})")
    return itinerary

# Inicializar la aplicación principal
if __name__ == "__main__":
    show_main_screen()

