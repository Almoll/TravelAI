import sqlite3

def initialize_database():
    conn = sqlite3.connect("travel_planner.db")
    cursor = conn.cursor()

    # Crear tabla para usuarios
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    """)

    # Crear tabla para viajes
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS trips (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            trip_details TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    conn.commit()
    conn.close()

def register_user(username, email, password):
    conn = sqlite3.connect("travel_planner.db")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", (username, email, password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def login_user(email, password):
    conn = sqlite3.connect("travel_planner.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, username FROM users WHERE email = ? AND password = ?", (email, password))
    user = cursor.fetchone()
    conn.close()
    return user  # Devuelve (id, username) si existe, de lo contrario None

def save_trip(user_id, trip_details):
    conn = sqlite3.connect("travel_planner.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO trips (user_id, trip_details) VALUES (?, ?)", (user_id, trip_details))
    conn.commit()
    conn.close()

def get_user_trips(user_id):
    conn = sqlite3.connect("travel_planner.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, trip_details FROM trips WHERE user_id = ?", (user_id,))
    trips = cursor.fetchall()
    conn.close()
    return trips

def delete_trip(trip_id):
    conn = sqlite3.connect("travel_planner.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM trips WHERE id = ?", (trip_id,))
    conn.commit()
    conn.close()
