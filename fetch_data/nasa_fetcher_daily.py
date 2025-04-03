import os
import json
import requests
from datetime import datetime

# === Configuration ===
OUTPUT_DIR = "../data/departments"
PARAMETERS = ["WS2M", "WS2M_MAX", "WS2M_MIN"]
START_DATE = "2024-01-01"
END_DATE = "2024-12-31"

# Departamento list (nombre, lat, lon)
DEPARTMENTS = [
    {"nombre": "guatemala", "lat": 14.6349, "lon": -90.5069},
    {"nombre": "sacatepequez", "lat": 14.5667, "lon": -90.7333},
    {"nombre": "escuintla", "lat": 14.3050, "lon": -90.7850},
    {"nombre": "peten", "lat": 16.9167, "lon": -89.8833},
    {"nombre": "quiche", "lat": 15.0300, "lon": -91.1500},
    {"nombre": "izabal", "lat": 15.7167, "lon": -88.5833},
    {"nombre": "jalapa", "lat": 14.6328, "lon": -89.9889},
    {"nombre": "jutiapa", "lat": 14.2911, "lon": -89.8933},
    {"nombre": "alta_verapaz", "lat": 15.5833, "lon": -90.3333},
    {"nombre": "baja_verapaz", "lat": 15.1000, "lon": -90.5833},
    {"nombre": "chimaltenango", "lat": 14.6614, "lon": -90.8194},
    {"nombre": "chiquimula", "lat": 14.8000, "lon": -89.5450},
    {"nombre": "el_progreso", "lat": 14.8500, "lon": -90.0167},
    {"nombre": "quetzaltenango", "lat": 14.8333, "lon": -91.5167},
    {"nombre": "retalhuleu", "lat": 14.5333, "lon": -91.6833},
    {"nombre": "san_marcos", "lat": 14.9667, "lon": -91.8000},
    {"nombre": "santa_rosa", "lat": 14.2833, "lon": -90.2833},
    {"nombre": "solola", "lat": 14.7667, "lon": -91.1833},
    {"nombre": "suchitepequez", "lat": 14.5333, "lon": -91.5000},
    {"nombre": "totonicapan", "lat": 14.9139, "lon": -91.3611},
    {"nombre": "zacapa", "lat": 14.9667, "lon": -89.5333}
]

def fetch_daily_data(dept_name, lat, lon, parameter):
    url = (
        f"https://power.larc.nasa.gov/api/temporal/daily/point?"
        f"start={START_DATE.replace('-', '')}&end={END_DATE.replace('-', '')}"
        f"&latitude={lat}&longitude={lon}&community=RE"
        f"&parameters={parameter}&format=JSON"
    )

    try:
        print(f"⬇️ Fetching {parameter} for {dept_name}...")
        response = requests.get(url)
        response.raise_for_status()

        data = response.json()
        return data["properties"]["parameter"][parameter]
    except Exception as e:
        print(f"❌ Error fetching {parameter} for {dept_name}: {e}")
        return None

def main():
    for dept in DEPARTMENTS:
        nombre = dept["nombre"]
        lat = dept["lat"]
        lon = dept["lon"]
        dept_path = os.path.join(OUTPUT_DIR, nombre)
        os.makedirs(dept_path, exist_ok=True)

        for param in PARAMETERS:
            result = fetch_daily_data(nombre, lat, lon, param)
            if result:
                filename = f"{param.lower()}_daily.json"
                file_path = os.path.join(dept_path, filename)
                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump(result, f, indent=2, ensure_ascii=False)
                print(f"✅ Saved {filename} in {nombre}")
            else:
                print(f"⚠️ Skipped {param} for {nombre}")

if __name__ == "__main__":
    main()
