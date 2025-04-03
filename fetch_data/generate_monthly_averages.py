import os
import json
from collections import defaultdict

# === CONFIGURATION ===
"""PARAMETERS = [
    "ALLSKY_SFC_SW_DWN", "CLRSKY_SFC_SW_DWN", "T2M", "T2M_MAX", "T2M_MIN",
    "RH2M", "WS2M", "WS10M", "WS50M", "PRECTOTCORR"
]"""
PARAMETERS = ["WS2M", "WS2M_MAX", "WS2M_MIN"]
INPUT_DIR = "../data/departments"
OUTPUT_DIR = "../data/averages"

# Mapping numeric months to Spanish names
MONTH_MAP = {
    "01": "Enero", "02": "Febrero", "03": "Marzo", "04": "Abril",
    "05": "Mayo", "06": "Junio", "07": "Julio", "08": "Agosto",
    "09": "Septiembre", "10": "Octubre", "11": "Noviembre", "12": "Diciembre"
}

# === MAIN SCRIPT ===
def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for param in PARAMETERS:
        output_data = []

        for dept_folder in os.listdir(INPUT_DIR):
            dept_path = os.path.join(INPUT_DIR, dept_folder)
            if not os.path.isdir(dept_path) or dept_folder == "averages":
                continue

            file_path = os.path.join(dept_path, f"{param.lower()}.json")
            if not os.path.exists(file_path):
                print(f"⚠️ No se encontró: {file_path}")
                continue

            with open(file_path, "r", encoding="utf-8") as f:
                monthly_data_by_year = json.load(f)

            monthly_sums = defaultdict(float)
            monthly_counts = defaultdict(int)

            for key, value in monthly_data_by_year.items():
                if len(key) != 6:
                    continue  # skip unexpected formats

                month_num = key[4:]
                if month_num == "13":
                    continue  # skip annual average

                # Skip invalid data
                if value == -999.0:
                    continue

                month_name = MONTH_MAP.get(month_num)
                if not month_name:
                    continue

                monthly_sums[month_name] += value
                monthly_counts[month_name] += 1

            monthly_avg = {
                month: round(monthly_sums[month] / monthly_counts[month], 2)
                for month in MONTH_MAP.values()
                if monthly_counts[month] > 0
            }

            output_data.append({
                "departamento": dept_folder,
                "datos": monthly_avg
            })

        output_filename = os.path.join(OUTPUT_DIR, f"avg_{param.lower()}.json")
        with open(output_filename, "w", encoding="utf-8") as f_out:
            json.dump(output_data, f_out, indent=2, ensure_ascii=False)

        print(f"✅ Guardado: {output_filename}")

if __name__ == "__main__":
    main()
