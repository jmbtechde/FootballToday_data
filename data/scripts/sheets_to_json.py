#!/usr/bin/env python3
# scripts/sheets_to_json.py
# Wandelt Google‑Sheets CSVs in JSON-Dateien unter /data um.

import csv, json, os, sys
from urllib.request import urlopen
from urllib.error import URLError, HTTPError

SHEETS = {
    "data/playerdata.json":
        "https://docs.google.com/spreadsheets/d/e/2PACX-1vQQpmPsya_7om0r3NU89tEuaGdTcrq0mXwDF78dQAV6RIXiDybEiQVHh052Oq97Qvoq_V-IpPwqe2vM/pub?gid=0&single=true&output=csv",
    "data/playernumbers.json":
        "https://docs.google.com/spreadsheets/d/e/2PACX-1vQR2rAyG3r1IeWapXwzomjMlaYs-xeQbXno7kKE_wsg8a7r5H209Wa99QIz4dKYkpWRZXAnCknTAaaO/pub?gid=0&single=true&output=csv",
    "data/gameday_analysis.json":
        "https://docs.google.com/spreadsheets/d/e/2PACX-1vQb5gHazVA0ocBRh8s1YB0UwZDoMfyoJA25XufRBVn8S23XyLNv73KqGeQMjopSQ-q3BpN2KJ7OENU5/pub?gid=0&single=true&output=csv"
}

OUT_INDEX = "data/index.json"

def fetch_csv(url: str):
    with urlopen(url) as resp:
        if resp.status != 200:
            raise HTTPError(url, resp.status, "Bad status", hdrs=None, fp=None)
        data = resp.read().decode("utf-8", errors="replace")
        return list(csv.reader(data.splitlines()))

def rows_to_dicts(rows):
    if not rows:
        return []
    header = [h.strip() for h in rows[0]]
    out = []
    for r in rows[1:]:
        if len(r) < len(header):
            r = r + [""] * (len(header) - len(r))
        elif len(r) > len(header):
            r = r[:len(header)]
        out.append({header[i]: r[i].strip() for i in range(len(header))})
    return out

def ensure_dir(path: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)

def main():
    ensure_dir(OUT_INDEX)
    index = {}
    for out_path, url in SHEETS.items():
        try:
            print(f"→ Hole CSV: {url}")
            rows = fetch_csv(url)
            objs = rows_to_dicts(rows)
            ensure_dir(out_path)
            with open(out_path, "w", encoding="utf-8") as f:
                json.dump(objs, f, ensure_ascii=False, indent=2)
            print(f"✓ Geschrieben: {out_path} ({len(objs)} Objekte)")
            index[os.path.basename(out_path)] = {
                "url": f"./{out_path}",
                "count": len(objs)
            }
        except Exception as e:
            print(f"✗ Fehler bei {url}: {e}", file=sys.stderr)
            index[os.path.basename(out_path)] = {"error": str(e)}

    with open(OUT_INDEX, "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)
    print(f"✓ Index aktualisiert: {OUT_INDEX}")

if __name__ == "__main__":
    main()
