import os
import json
import requests
from datetime import datetime

# === CONFIGURATION ===
"""
PARAMETERS = [
    "ALLSKY_SFC_SW_DWN", "CLRSKY_SFC_SW_DWN", "T2M", "T2M_MAX", "T2M_MIN",
    "RH2M", "WS2M", "WS10M", "WS50M", "PRECTOTCORR"
]
"""
PARAMETERS = ["WS2M", "WS2M_MAX", "WS2M_MIN"]
START_DATE = "2020-01-01"
END_DATE = "2024-12-31"
OUTPUT_DIR = "../data/departments"

# === LOCATION DATA ===
DEPARTMENTS = [
    {"nombre": "guatemala", "lat": 14.6349, "lon": -90.5069},
    {"nombre": "escuintla", "lat": 14.3000, "lon": -90.7833},
    {"nombre": "quetzaltenango", "lat": 14.8458, "lon": -91.5181},
    {"nombre": "alta_verapaz", "lat": 15.4694, "lon": -90.3790},
    {"nombre": "peten", "lat": 16.9226, "lon": -89.8924},
    {"nombre": "jalapa", "lat": 14.6347, "lon": -89.9892},
    {"nombre": "chiquimula", "lat": 14.8000, "lon": -89.5500},
    {"nombre": "santa_rosa", "lat": 14.2833, "lon": -90.2833},
    {"nombre": "sacatepequez", "lat": 14.5667, "lon": -90.7333},
    {"nombre": "totonicapan", "lat": 14.9167, "lon": -91.3667},
    {"nombre": "jalapa", "lat": 14.6333, "lon": -89.9833},
    {"nombre": "chimaltenango", "lat": 14.6617, "lon": -90.8194},
    {"nombre": "solola", "lat": 14.7717, "lon": -91.1833},
    {"nombre": "huehuetenango", "lat": 15.3, "lon": -91.4667},
    {"nombre": "san_marcos", "lat": 14.9667, "lon": -91.8000},
    {"nombre": "izabal", "lat": 15.7167, "lon": -88.5833},
    {"nombre": "zacapa", "lat": 14.9667, "lon": -89.5333},
    {"nombre": "el_progreso", "lat": 14.9333, "lon": -89.8667},
    {"nombre": "baja_verapaz", "lat": 15.1, "lon": -90.3},
    {"nombre": "retalhuleu", "lat": 14.5333, "lon": -91.6833},
    {"nombre": "suchitepequez", "lat": 14.5333, "lon": -91.5},
    {"nombre": "jutiapa", "lat": 14.3, "lon": -89.9}
]

# === FUNCTION TO FETCH DATA ===
def fetch_nasa_power_data(lat, lon, parameter):
    url = (
        f"https://power.larc.nasa.gov/api/temporal/monthly/point"
        f"?start={START_DATE[:4]}&end={END_DATE[:4]}"
        f"&latitude={lat}&longitude={lon}"
        f"&parameters={parameter}"
        f"&community=RE&format=JSON"
    )

    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"❌ Error fetching {parameter} for lat={lat}, lon={lon}: {e}")
        return None

# === MAIN SCRIPT ===
def main():
    for dept in DEPARTMENTS:
        nombre = dept["nombre"]
        lat = dept["lat"]
        lon = dept["lon"]

        folder_path = os.path.join(OUTPUT_DIR, nombre)
        os.makedirs(folder_path, exist_ok=True)
        print(f"\n📍 Procesando: {nombre.title()}")

        for param in PARAMETERS:
            print(f"  ⏳ Descargando: {param}...")

            data = fetch_nasa_power_data(lat, lon, param)
            if not data:
                continue

            try:
                # Extract monthly values (average over all years)
                monthly_data = data["properties"]["parameter"][param]
                filename = os.path.join(folder_path, f"{param.lower()}.json")

                with open(filename, "w", encoding="utf-8") as f:
                    json.dump(monthly_data, f, indent=2, ensure_ascii=False)

                print(f"  ✅ Guardado: {filename}")
            except KeyError:
                print(f"  ⚠️ Formato inesperado para {param} en {nombre}")

if __name__ == "__main__":
    main()
