import os
import json
from collections import defaultdict
from datetime import datetime

INPUT_DIR = "../data/departments"
OUTPUT_DIR = "../data/averages"
PARAM_MAP = {
    "ws2m.json": "avg_ws2m.json",
    "ws2m_max.json": "avg_ws2m_max.json",
    "ws2m_min.json": "avg_ws2m_min.json"
}

MONTH_NAMES = {
    "01": "Enero", "02": "Febrero", "03": "Marzo", "04": "Abril",
    "05": "Mayo", "06": "Junio", "07": "Julio", "08": "Agosto",
    "09": "Septiembre", "10": "Octubre", "11": "Noviembre", "12": "Diciembre"
}

def parse_month(key):
    try:
        return datetime.strptime(key, "%Y%m%d").strftime("%m")
    except:
        return None

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for input_file, output_file in PARAM_MAP.items():
        final_data = []

        for dept in os.listdir(INPUT_DIR):
            dept_path = os.path.join(INPUT_DIR, dept)
            full_path = os.path.join(dept_path, input_file)

            if not os.path.exists(full_path):
                continue

            with open(full_path, "r", encoding="utf-8") as f:
                daily_data = json.load(f)

            monthly_values = defaultdict(list)

            for date_str, val in daily_data.items():
                if val == -999.0:
                    continue
                month = parse_month(date_str)
                if month:
                    monthly_values[month].append(val)

            monthly_avg = {
                MONTH_NAMES[m]: round(sum(vs) / len(vs), 2)
                for m, vs in monthly_values.items() if vs
            }

            final_data.append({
                "departamento": dept,
                "datos": monthly_avg
            })

        with open(os.path.join(OUTPUT_DIR, output_file), "w", encoding="utf-8") as f_out:
            json.dump(final_data, f_out, indent=2, ensure_ascii=False)

        print(f"✅ Archivo guardado: {output_file}")

if __name__ == "__main__":
    main()
