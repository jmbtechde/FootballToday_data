import csv, json, os, urllib.request

# Ordner für Ausgaben
os.makedirs("data", exist_ok=True)

# --- deine Google Sheets Links ---
sheets = {
    "players.json": "https://docs.google.com/spreadsheets/d/e/2PACX-1vQQpmPsya_7om0r3NU89tEuaGdTcrq0mXwDF78dQAV6RIXiDybEiQVHh052Oq97Qvoq_V-IpPwqe2vM/pub?gid=0&single=true&output=csv",
    "player_numbers.json": "https://docs.google.com/spreadsheets/d/e/2PACX-1vQR2rAyG3r1IeWapXwzomjMlaYs-xeQbXno7kKE_wsg8a7r5H209Wa99QIz4dKYkpWRZXAnCknTAaaO/pub?gid=0&single=true&output=csv",
    "analysis.json": "https://docs.google.com/spreadsheets/d/e/2PACX-1vQb5gHazVA0ocBRh8s1YB0UwZDoMfyoJA25XufRBVn8S23XyLNv73KqGeQMjopSQ-q3BpN2KJ7OENU5/pub?gid=0&single=true&output=csv"
}

def download_csv(url):
    with urllib.request.urlopen(url) as resp:
        return resp.read().decode("utf-8").splitlines()

def convert_to_json(csv_lines):
    reader = csv.DictReader(csv_lines)
    return list(reader)

index = {}

for out_name, url in sheets.items():
    print(f"➡️ Hole {url}")
    csv_lines = download_csv(url)
    json_data = convert_to_json(csv_lines)

    # Datei speichern
    out_path = os.path.join("data", out_name)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)

    index[out_name] = out_path

# Übersicht index.json
with open("data/index.json", "w", encoding="utf-8") as f:
    json.dump(index, f, indent=2)

print("✅ Fertig: JSON-Dateien erzeugt in /data")
