#!/usr/bin/env python3
"""Merge the parsed 2019 roster + curated listings -> data/locations.csv (the editable source of truth)
and data/sources.csv. Run: python3 scripts/build_data.py"""
import csv, json, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from geo import MUNI, muni_of, en_address, kana_to_romaji
import curated

ROOT = Path(__file__).resolve().parent.parent
FIELDS = ["id","name_ja","name_en","disciplines","style","kind","municipality","region","address_ja","address_en","phone","website","social",
          "email","hours","contact","notes","visitors","english","verification","status","last_verified","sources","source_date","aliases","privacy_note","lat","lon","geo_precision"]

STYLE_RULES = [  # (regex, English style label)  — first match wins
 (r"日本空手協会|松濤", "Shotokan (JKA)"), (r"糸東", "Shito-ryu"), (r"和道", "Wado-ryu"),
 (r"極真", "Kyokushin"), (r"御殿手", "Motobu Udun-di"), (r"劉衛流", "Ryuei-ryu"), (r"上地流|上地", "Uechi-ryu"),
 (r"剛柔", "Goju-ryu"), (r"松林流|松林", "Matsubayashi-ryu (Shorin-ryu)"), (r"船越|少林流|少林", "Shorin-ryu (Shobayashi)"),
 (r"小林", "Shorin-ryu (Kobayashi)"), (r"泊手", "Tomari-te"), (r"首里", "Shuri-te / Shorin-ryu"), (r"拳法", "Okinawa Kenpo"),
 (r"空手|唐手", "Karate (style not stated in roster)"),
]
KARATE_MARK = re.compile(r"空手|唐手|小林|少林|松林|剛柔|上地|劉衛|拳法|御殿手|松濤|糸東|和道|極真")
KOBUDO_MARK = re.compile(r"古武")

def style_of(text):
    for rx, lab in STYLE_RULES:
        if re.search(rx, text): return lab
    return ""

def trim_address(addr):
    """Privacy: drop apartment names and room numbers from roster addresses (keep block-level)."""
    a = addr
    a = re.sub(r"\s*[^\s]*(?:マンション|アパート|団地|市営住宅|コーポ|ハイツ|荘)[^\s]*(?:\s*\d+号?)?", "", a)
    a = re.sub(r"(\d+-\d+-\d+)-\d{3,4}$", r"\1", a)
    a = re.sub(r"\s*号$", "", a).strip()
    return a, (a != addr)

def region_of(muni_ja): return MUNI[muni_ja][2] if muni_ja in MUNI else ""

def roster_rows():
    data = json.loads((ROOT/"data/work/roster_parsed.json").read_text(encoding="utf-8"))
    out = []
    for r in data:
        assoc, dojo = r["association_ja"], r["dojo_ja"]
        txt = assoc + dojo
        addr, trimmed = trim_address(r["address_ja"])
        muni, rest = muni_of(addr)
        if not muni:
            fac = addr
            muni = {"宮古市内体育館":"宮古島市","沖縄県立武道館":"那覇市","沖縄空手会館":"豊見城市","屋我地　体育館":"名護市","屋我地 体育館":"名護市","勝山公民館、安和小学校":"名護市"}.get(fac)
            rest = fac
        style = style_of(txt)
        karate = bool(KARATE_MARK.search(txt)) or not KOBUDO_MARK.search(txt)
        discs = []
        if style == "Kyokushin": discs = ["kyokushin"]
        elif karate: discs = ["karate"]
        if KOBUDO_MARK.search(txt): discs.append("kobudo")
        if not discs: discs = ["karate"]
        kana = r.get("rep_kana")
        rep_en = r.get("rep_en") or ""
        if not rep_en and kana:
            rep_en = f"{kana_to_romaji(kana['given'])} {kana_to_romaji(kana['surname'])}"   # Given Surname
        surname_en = kana_to_romaji(kana["surname"]) if kana else ""
        base = re.sub(r"(道場|本部|総本部|\s)", "", dojo)
        rep_surname_ja = r["rep_ja"].split(" ")[0]
        if dojo.endswith("道場") and surname_en and rep_surname_ja and rep_surname_ja in dojo:
            name_en = f"{surname_en} Dojo"
        elif surname_en:
            name_en = f"{surname_en} Sensei's dojo"
        else:
            name_en = "Dojo (name not romanized)"
        if style and not style.startswith("Karate"): name_en += f" — {style}"
        elif style: name_en += " — karate"
        if KOBUDO_MARK.search(txt) and "kobudo" not in name_en.lower(): name_en += " + kobudo"
        place = en_address(muni, rest) if muni else ""
        if muni and "," not in place and addr:
            place = f"{place} · {addr}"
        notes = []
        if "no_address_in_roster" in r["flags"]: notes.append("The 2019 roster lists no address for this dojo.")
        if r.get("extra_addresses_ja"): notes.append("Roster lists a second address: " + " / ".join(r["extra_addresses_ja"]))
        out.append(dict(
            id=f"roster-{r['idx']:03d}", name_ja=(assoc + (" " if assoc and dojo else "") + dojo).strip(), name_en=name_en,
            disciplines=";".join(discs), style=style or "Karate / kobudo (style not stated)", kind="dojo",
            municipality=MUNI[muni][0] if muni else "", region=region_of(muni) if muni else "",
            address_ja=rest if (muni and rest in ("沖縄県立武道館","沖縄空手会館")) else addr, address_en=place,
            phone="", website="", social="", email="", hours="", contact=(f"{rep_en} ({r['rep_ja']})" if rep_en else r["rep_ja"]).strip(),
            notes=" ".join(notes), visitors="", english="unknown", verification="C", status="unverified", last_verified="",
            sources="okic-roster", source_date="2019", aliases="", privacy_note="address trimmed to block level" if trimmed else ""))
    return out

def curated_rows():
    out = []
    for c in curated.ALL:
        muni = c["muni"]; m = MUNI.get(muni)
        addr_ja = c["address_ja"]
        place = c["address_en"] or (en_address(muni, muni_of(addr_ja)[1]) if (muni and addr_ja and muni_of(addr_ja)[0]) else (f"{m[1].split(' (')[0]}" if m else ""))
        if not c["address_en"] and muni and addr_ja and not muni_of(addr_ja)[0]:
            place = f"{m[1]} — {addr_ja}"      # venue-only addresses keep the Japanese venue text
        elif not c["address_en"] and muni and addr_ja and "," not in place:
            place = f"{place} · {addr_ja}"
        out.append(dict(
            id=c["id"], name_ja=c["name_ja"], name_en=c["name_en"], disciplines=";".join(c["disciplines"]), style=c["style"], kind=c["kind"],
            municipality=m[0] if m else "", region=m[2] if m else "", address_ja=addr_ja, address_en=place, phone=c["phone"], website=c["website"],
            social=c["social"], email=c["email"], hours=c["hours"], contact=c["contact"], notes=c["notes"], visitors=c["visitors"], english=c["english"],
            verification=c["verification"], status=c["status"], last_verified=c["last_verified"], sources=";".join(c["sources"]),
            source_date=c["source_date"], aliases=c["aliases"], privacy_note=""))
    return out

SOURCES = [
 # id, title, url, type, use, policy
 ("okic-roster","沖縄県内道場名簿 (Okinawa dojo roster, FY2019) — Okinawa Karate Information Center / Karate Kaikan","https://okic.odks.jp/","Official roster (prefecture-run)","Dojo names, instructors and addresses for karate/kobudo. Facts only; addresses trimmed to block level.","Government-published list; not re-verified since 2019."),
 ("kyokushin-okinawa","極真会館 沖縄県支部 (Kyokushinkaikan Okinawa Branch)","https://www.kyokushinokinawa.com/","Official organisation site","Dojo addresses, phones, instructors.","Facts only; checked Oct 2026."),
 ("shinkyokushin-okinawa","新極真会 沖縄支部 (Shinkyokushinkai Okinawa Branch)","https://yoshidadojo.jp/","Official organisation site","Dojo addresses, phones, instructor.","Facts only."),
 ("kyokushinkan-org","極真館 (Kyokushinkan) — national dojo roster","https://kyokushinkan.org/","Official organisation site","Ginoza dojo listing.","Facts only."),
 ("okikenren","一般財団法人 沖縄県剣道連盟 (Okinawa Kendo Federation) — class and practice lists","https://www.okikenren.jp/","Governing body","Youth, adult, iaido and jodo practice lists with venues, days and phones.","Facts only; checked Oct 2026."),
 ("judo-dojo-navi","全日本柔道連盟 道場ナビ — 沖縄県 (AJJF Dojo Navi, Okinawa: 13 dojo)","https://www.judo.or.jp/dojo-navi/dojo/okinawa","Governing body directory","Judo dojo venues and days/times.","Facts only; checked Oct 2026. Phone numbers are on each dojo's detail page."),
 ("judo-fed","沖縄県柔道連盟 (Okinawa Judo Federation)","https://judo.spoyell.okinawa/","Governing body","Federation contact.","Facts only."),
 ("aikikai-dir","合気会 Okinawa dojo directory (aikido.ne.jp)","https://www.aikido.ne.jp/dojo/okinawa.html","Organisation directory","Aikido dojo venues and instructors.","Facts only."),
 ("federation-sites","Prefectural federation / association websites (boxing, sumo, shorinji kempo, kyudo, naginata, wrestling, etc.)","","Governing bodies","Organisation contacts.","Facts only."),
 ("mccs","MCCS Okinawa — Martial Arts program","https://www.okinawa.usmc-mccs.org/recreation-fitness/sports/martial-arts","Official programme page","Programme list, contacts, fees, joining process.","Facts only; checked Oct 2026."),
 ("karatekaikan","沖縄空手会館 (Okinawa Karate Kaikan) — official site","https://karatekaikan.jp/en","Official facility site","Facility information.","Facts only."),
 ("official-site","Each gym's or dojo's own website","","Operator site","Addresses, phone numbers, schedules, instructors.","Facts only; links go to the operator."),
 ("ageshio","Ageshio Japan — Kobukai dojo page","https://ageshiojapan.com/?p=4294","Operator site","Kobukai details.","Facts only; checked Oct 2026."),
 ("stripes","Stars and Stripes Okinawa — jiu-jitsu feature (Apr 2026)","https://okinawa.stripes.com/travel/jiu-jitsu-okinawa.html","News article","Lead only (Leos BJJ Academy).","Lead; no data copied."),
 ("bjjglobetrotters","BJJ Globetrotters — Okinawa gym write-ups (2018–2019)","https://www.bjjglobetrotters.com/","Travel blog","Leads and historical drop-in notes.","Dated; leads only."),
 ("directory","Third-party gym directories (THE GYMS Okinawa, Itoman Gym network pages, chain locators, etc.)","https://thegyms.jp/okinawa/","Commercial directory","Used only to discover gyms; facts then checked against operator sites where possible.","Leads only; no listing text or ratings copied. Sites that disallow automated access were not scraped."),
 ("visitor-reviews","Visitor reviews and travel write-ups","","Reviews","Leads for English-friendly dojo.","Leads only."),
 ("competition-results","Public competition results","","Results","Evidence that a group is active.","Leads only."),
 ("social-media","Operators' public social-media pages","","Operator social","Meeting times for small clubs.","Facts only; links go to the operator."),
 ("community-report","Reports from members, visitors and owners (via the suggest-an-edit form or the site maintainers)","","Community","Open/closed status and changes.","Treated as a lead until confirmed against an operator source."),
 ("facebook","Operators' public Facebook pages","","Operator social","Contact links.","Facts only."),
 ("judo-fed-note","(reserved)","","","",""),
]

def main():
    rows = roster_rows() + curated_rows()
    old = {}
    f = ROOT/"data/locations.csv"
    if f.exists():   # keep coordinates that scripts/geocode.py already filled in
        old = {r["id"]: r for r in csv.DictReader(open(f, encoding="utf-8-sig"))}
    for r in rows:
        o = old.get(r["id"], {})
        r["lat"], r["lon"], r["geo_precision"] = o.get("lat", ""), o.get("lon", ""), o.get("geo_precision", "")
    ids = [r["id"] for r in rows]; assert len(ids) == len(set(ids)), "duplicate ids"
    with open(ROOT/"data/locations.csv", "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, FIELDS); w.writeheader(); w.writerows(rows)
    with open(ROOT/"data/sources.csv", "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f); w.writerow(["id","title","url","type","how_used","policy"])
        for s in SOURCES:
            if s[0] != "judo-fed-note": w.writerow(s)
    from collections import Counter
    print("rows", len(rows), Counter(r["verification"] for r in rows), Counter(r["kind"] for r in rows))
    print("no municipality:", [r["id"] for r in rows if not r["municipality"]])

if __name__ == "__main__":
    main()
