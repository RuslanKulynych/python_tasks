import math
import sqlite3
from pathlib import Path

DB_FILE = Path("cities.db")


class CityDatabase:
    """Handles city coordinates storage and retrieval using SQLite."""

    def __init__(self, db_path=DB_FILE):
        self.conn = sqlite3.connect(db_path)
        self.create_table()

    def create_table(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS cities (
                    name TEXT PRIMARY KEY,
                    latitude REAL NOT NULL,
                    longitude REAL NOT NULL
                )
            """)

    def get_city(self, name: str):
        cur = self.conn.cursor()
        cur.execute("SELECT latitude, longitude FROM cities WHERE name=?", (name.lower(),))
        return cur.fetchone()

    def add_city(self, name: str, latitude: float, longitude: float):
        with self.conn:
            self.conn.execute(
                "INSERT OR REPLACE INTO cities (name, latitude, longitude) VALUES (?, ?, ?)",
                (name.lower(), latitude, longitude)
            )


def haversine_distance(lat1, lon1, lat2, lon2):
    """Calculate great-circle distance between two points on Earth in kilometers."""
    R = 6371.0  # Earth's radius in km

    # Convert degrees → radians
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c


def get_city_coordinates(db: CityDatabase, city_name: str):
    """Retrieve or ask user for city coordinates, then return them."""
    record = db.get_city(city_name)
    if record:
        return record

    print(f"Coordinates for '{city_name}' not found.")
    while True:
        try:
            lat = float(input(f"Enter latitude for {city_name} (degrees): "))
            lon = float(input(f"Enter longitude for {city_name} (degrees): "))
            db.add_city(city_name, lat, lon)
            print(f"✅ Saved {city_name} ({lat}, {lon}) in database.")
            return lat, lon
        except ValueError:
            print("❌ Invalid input. Please enter numeric values.")


def main():
    db = CityDatabase()

    print("\n=== City Distance Calculator ===")
    city1 = input("Enter first city: ").strip()
    city2 = input("Enter second city: ").strip()

    lat1, lon1 = get_city_coordinates(db, city1)
    lat2, lon2 = get_city_coordinates(db, city2)

    distance = haversine_distance(lat1, lon1, lat2, lon2)
    print(f"\n📏 Straight-line distance between {city1.title()} and {city2.title()}: {distance:.2f} km")


if __name__ == "__main__":
    main()
