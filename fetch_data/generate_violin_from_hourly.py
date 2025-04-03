import os
import json
from collections import defaultdict

PARAMETRO = "ws2m"
INPUT_DIR = "../data/departments"
OUTPUT_DIR = "../data/violin"
OUTPUT_FILENAME = f"wind_{PARAMETRO}_violin.json"

# Month name map
MONTH_MAP = {
    "01": "Enero", "02": "Febrero", "03": "Marzo", "04": "Abril",
    "05": "Mayo", "06": "Junio", "07": "Julio", "08": "Agosto",
    "09": "Septiembre", "10": "Octubre", "11": "Noviembre", "12": "Diciembre"
}

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    result = []

    for dept_name in os.listdir(INPUT_DIR):
        dept_path = os.path.join(INPUT_DIR, dept_name)
        file_path = os.path.join(dept_path, f"{PARAMETRO}_hourly.json")

        if not os.path.isdir(dept_path) or not os.path.exists(file_path):
            continue

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        month_data = defaultdict(list)

        for key, values in data.items():
            if len(key) != 6:
                continue
            month = key[4:]
            month_name = MONTH_MAP.get(month)
            if not month_name:
                continue
            filtered_values = [v for v in values if v != -999.0]
            month_data[month_name].extend(filtered_values)

        result.append({
            "departamento": dept_name,
            "datos": month_data
        })

    output_path = os.path.join(OUTPUT_DIR, OUTPUT_FILENAME)
    with open(output_path, "w", encoding="utf-8") as out_f:
        json.dump(result, out_f, indent=2, ensure_ascii=False)

    print(f"✅ Violin data saved to: {output_path}")

if __name__ == "__main__":
    main()
