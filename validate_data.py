#!/usr/bin/env python3
"""CI gate: python3 scripts/validate_data.py  (exit 1 on any error)"""
import csv, re, sys, datetime
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from catalog import DISC, VERIF, STATUS
from geo import MUNI_SLUGS
ROOT = Path(__file__).resolve().parent.parent
rows = list(csv.DictReader(open(ROOT/"data/locations.csv", encoding="utf-8-sig")))
src = {s["id"] for s in csv.DictReader(open(ROOT/"data/sources.csv", encoding="utf-8-sig"))}
errs, warns, seen = [], [], set()
for r in rows:
    i = r["id"]
    if not re.fullmatch(r"[a-z0-9-]+", i): errs.append(f"{i}: bad id")
    if i in seen: errs.append(f"{i}: duplicate id")
    seen.add(i)
    if not r["name_en"] or not r["name_ja"] and not r["name_en"]: errs.append(f"{i}: missing name")
    for d in r["disciplines"].split(";"):
        if d not in DISC: errs.append(f"{i}: unknown discipline {d!r}")
    if r["municipality"] and r["municipality"] not in MUNI_SLUGS: errs.append(f"{i}: unknown municipality {r['municipality']!r}")
    if r["verification"] not in VERIF: errs.append(f"{i}: bad verification")
    if r["status"] not in STATUS: errs.append(f"{i}: bad status")
    for s in filter(None, r["sources"].split(";")):
        if s not in src: errs.append(f"{i}: unknown source {s!r}")
    if r["last_verified"]:
        try: datetime.date.fromisoformat(r["last_verified"])
        except ValueError: errs.append(f"{i}: last_verified must be YYYY-MM-DD")
    if r["verification"] == "A" and not r["last_verified"]: errs.append(f"{i}: verification A needs last_verified")
    if r.get("lat") or r.get("lon"):
        try:
            la, lo = float(r["lat"]), float(r["lon"])
            if not (23.5 < la < 28.6 and 122.5 < lo < 131.5): errs.append(f"{i}: coordinates outside Okinawa")
        except ValueError: errs.append(f"{i}: bad lat/lon")
    if r["phone"] and not re.search(r"\d", r["phone"]): warns.append(f"{i}: phone has no digits")
    if r["website"] and not re.match(r"(https?://|[\w.-]+\.\w+)", r["website"]): warns.append(f"{i}: odd website")
print(f"{len(rows)} rows, {len(errs)} errors, {len(warns)} warnings")
for e in errs: print("ERROR", e)
for w in warns[:30]: print("warn", w)
sys.exit(1 if errs else 0)
