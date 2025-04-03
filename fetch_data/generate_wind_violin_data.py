import os
import json
from collections import defaultdict

# === CONFIGURATION ===
PARAMETRO = "ws2m"
INPUT_DIR = "../data/departments"  # ✅ updated
OUTPUT_DIR = "../data/violin"
OUTPUT_FILENAME = f"wind_{PARAMETRO}_violin.json"

# Mapping month numbers to Spanish names
MONTH_MAP = {
    "01": "Enero", "02": "Febrero", "03": "Marzo", "04": "Abril",
    "05": "Mayo", "06": "Junio", "07": "Julio", "08": "Agosto",
    "09": "Septiembre", "10": "Octubre", "11": "Noviembre", "12": "Diciembre"
}

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    result = []

    for dept_folder in os.listdir(INPUT_DIR):
        dept_path = os.path.join(INPUT_DIR, dept_folder)
        file_path = os.path.join(dept_path, f"{PARAMETRO}.json")

        if not os.path.isdir(dept_path):
            continue
        if not os.path.exists(file_path):
            print(f"❌ No se encontró {PARAMETRO}.json en {dept_folder}")
            continue

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        monthly_values = defaultdict(list)

        for key, value in data.items():
            if len(key) != 6:
                continue
            month = key[4:]
            if month == "13":
                continue
            if value == -999.0:
                continue

            month_name = MONTH_MAP.get(month)
            if month_name:
                monthly_values[month_name].append(value)

        result.append({
            "departamento": dept_folder,
            "datos": monthly_values
        })

    output_path = os.path.join(OUTPUT_DIR, OUTPUT_FILENAME)
    with open(output_path, "w", encoding="utf-8") as out_f:
        json.dump(result, out_f, indent=2, ensure_ascii=False)

    print(f"✅ Datos guardados en: {output_path}")

if __name__ == "__main__":
    main()
