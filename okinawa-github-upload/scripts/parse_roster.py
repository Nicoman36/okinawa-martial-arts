#!/usr/bin/env python3
"""Parse the Okinawa Karate Information Center dojo roster (FY2019) text into records.

Input : data/raw/okic_roster_2019.txt  (text as extracted from the official PDF)
Output: data/work/roster_parsed.json

The PDF uses ruby (furigana), so one dojo spans several text lines:
    <association> <dojo> <surname>
    <surname kana>
    <given-name kanji>
    <given kana> <address>
Record boundaries are found from the address line; address continuation lines are
only accepted when they match explicit building/venue patterns, so one record can
never swallow the next. Anything the parser is unsure about is written to `flags`.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data/raw/okic_roster_2019.txt"
OUT = ROOT / "data/work/roster_parsed.json"

MUNI = (
    "那覇市|豊見城市|南城市|糸満市|浦添市|宜野湾市|沖縄市|うるま市|名護市|石垣市|宮古島市|"
    "南風原町|八重瀬町|与那原町|西原町|北谷町|読谷村|北中城村|中城村|宜野座村|金武町|"
    "本部町|今帰仁村|恩納村|久米島町|宮古郡|宮古市内|中頭郡"
)
FACILITY_ONLY = ("沖縄県立武道館", "沖縄空手会館", "市内の体育館", "屋我地　体育館", "勝山公民館、安和小学校")
FAC = "|".join(map(re.escape, FACILITY_ONLY))
# optional 沖縄県 before a municipality; facility-only addresses must END the line
ADDR_RE = re.compile(rf"(?:沖縄県)?(?:{MUNI})|(?:^|(?<=\s)|(?<=\u3000))(?:{FAC})$")

KATAKANA_ONLY = re.compile(r"^[゠-ヿー・\s　]+$")
CONT_RE = re.compile(
    r"^(?:[（(].*[）)]|号|ANA SPORTS PARK.*|[^ ]*(?:ビル|マンション|アパート|団地|市営住宅|自治会|公民館|保育園)[^ ]*)$"
)

# Records whose association/dojo wrap across lines in the PDF. Keyed by the record's first
# text line; values replace the automatic association/dojo split.
OVERRIDES = {
    "上地流系沖縄孝武流空手道": {"association": "上地流系沖縄孝武流空手道古武道孝武会", "dojo": "本部道場"},
    "沖縄小林流空手道無拳会": {"association": "沖縄小林流空手道無拳会／琉球古武道信武舘", "dojo": "信武舘"},
    "沖縄船越少林流空手・琉球古武道協会": {"association": "沖縄船越少林流空手・琉球古武道協会清流館", "dojo": "船越少林流 清流館"},
    "（一社）沖縄伝統志道館空手古武術": {"association": "（一社）沖縄伝統志道館空手古武術国際連盟", "dojo": "中村道場"},
    "上地流空手道硬軟会": {"association": "上地流空手道硬軟会／沖縄古武道周和会", "dojo": "阿波根道場"},
    "沖縄空手道小林流竜球館": {"association": "沖縄空手道小林流竜球館空手古武道連盟", "dojo": "竜球館 総本部道場"},
    "剛柔流沖縄館空手道協会": {"association": "剛柔流沖縄館空手道協会／琉球古武術保存武道協会", "dojo": "沖縄館 本部道場"},
    "琉球伝統古武術保存武道協会 古武道徳身流総本部": {"association": "琉球伝統古武術保存武道協会", "dojo": "古武道徳身流総本部 徳身館"},
    "沖縄小林流空手道究道館連合会 究道館　緑川道場": {"association": "沖縄小林流空手道究道館連合会", "dojo": "究道館 緑川道場（沖縄空手会館教室）"},
    "沖縄小林流空手道古武道連盟": {"association": "沖縄小林流空手道古武道連盟", "dojo": "ワールド王修会 沖縄道場"},
}


def is_address(line: str):
    m = ADDR_RE.search(line)
    return m


def split_prefix_addr(line: str):
    m = ADDR_RE.search(line)
    prefix, addr = line[: m.start()].strip(), line[m.start():].strip()
    if prefix.endswith("沖") and addr.startswith("那覇市"):   # source typo: 沖那覇市
        prefix = prefix[:-1].strip()
    return prefix, addr


def norm_ws(s: str) -> str:
    return re.sub(r"[\s　]+", " ", s).strip()


def parse(lines):
    records, buf, cur = [], [], None
    for raw in lines:
        line = raw.strip()
        if not line:
            continue
        if ADDR_RE.search(line) and not CONT_RE.match(line):
            prefix, addr = split_prefix_addr(line)
            blob = buf + ([prefix] if prefix else [])
            if blob:
                cur = {"blob": blob, "addresses": [addr], "continuations": []}
                records.append(cur)
                buf = []
            elif cur is not None:
                cur["addresses"].append(addr)  # a second address for the same dojo
            continue
        if cur is not None and not buf and CONT_RE.match(line):
            cur["continuations"].append(line)
            continue
        buf.append(line)
    if buf:  # trailing lines without an address -> record with no address
        records.append({"blob": buf, "addresses": [], "continuations": []})
    return records


def split_missing_address(records):
    """A record with no address line (礼邦館) is glued to the next record; split it."""
    out = []
    for r in records:
        blob = r["blob"]
        starts = [i for i, l in enumerate(blob) if i > 0 and " " in l and not KATAKANA_ONLY.match(l)
                  and not re.match(r"^[ぁ-ん]", l)
                  and (re.search(r"(協会|連盟|保存会|拳士会|流)", l.split(" ")[0]))
                  and any(KATAKANA_ONLY.match(x) for x in blob[:i])]
        if starts:
            i = starts[0]
            out.append({"blob": blob[:i], "addresses": [], "continuations": []})
            out.append({"blob": blob[i:], "addresses": r["addresses"], "continuations": r["continuations"]})
        else:
            out.append(r)
    return out


def build(rec, idx):
    blob = rec["blob"]
    flags = []
    # head = lines before the first katakana-only line (the surname furigana)
    k = next((i for i, l in enumerate(blob) if KATAKANA_ONLY.match(l)), None)
    if k is None:
        flags.append("no_furigana_line")
        k = len(blob)
    head_lines, rest = blob[:k], blob[k:]
    head_key = head_lines[0] if head_lines else ""
    head = " ".join(head_lines)
    tokens = [t for t in head.split(" ") if t]
    surname_tok = tokens[-1] if tokens else ""
    name_tokens = tokens[:-1]
    pieces = [p for p in re.split(r"　", surname_tok) if p.strip()]
    kana_tokens, given_pieces = [], []
    for l in rest:
        if KATAKANA_ONLY.match(l):
            kana_tokens += [t for t in re.split(r"[\s　]+", l) if t]
        else:
            given_pieces += [t for t in re.split(r"　", l.strip()) if t.strip()]
    pieces += [p.strip() for p in given_pieces]
    # surname/given boundary
    boundary = None
    if len(re.split(r"　", surname_tok)) > 1 or any("　" in x for x in rest):
        boundary = 1
    # full-width-space inside a later piece ("城　守") marks the boundary after the surname part
    # pieces were already split on it, so locate it via the raw text instead
    raw_given = [l for l in rest if not KATAKANA_ONLY.match(l)]
    surname, given = "", ""
    if len(re.split(r"　", surname_tok)) > 1:       # "新城　安勇" on the head line
        parts = re.split(r"　", surname_tok)
        surname, given = parts[0], "".join(parts[1:] + [x.strip() for x in raw_given])
        ns = 1
    elif any("　" in x.strip() and not x.strip().startswith("　") and len(x.strip()) > 1 for x in raw_given):
        # e.g. 眞 / 栄 / 城　守 / 信  -> surname = 眞栄城, given = 守信
        acc, hit, after = surname_tok, False, []
        for x in raw_given:
            x = x.strip()
            if not hit and "　" in x:
                a, b = x.split("　", 1)
                acc += a
                after.append(b)
                hit = True
            elif not hit:
                acc += x
            else:
                after.append(x)
        surname, given = acc, "".join(after)
        ns = None
    else:
        flat = [surname_tok] + [x.strip() for x in raw_given]
        if len(flat) >= 3 and len(flat[0]) == 1:
            ns = 2                                          # 松/門/正, 池/宮城/政明, 我/謝/孟/弘 ...
        else:
            ns = 1
        surname, given = "".join(flat[:ns]), "".join(flat[ns:])
        if not given:
            flags.append("no_given_name")
    rep_ja = (surname + " " + given).strip()
    # association / dojo
    if len(name_tokens) >= 2:
        association, dojo = name_tokens[0], " ".join(name_tokens[1:])
    elif len(name_tokens) == 1:
        association, dojo = "", name_tokens[0]
    else:
        association, dojo = "", ""
        flags.append("no_name_tokens")
    ov = OVERRIDES.get(head_key) or OVERRIDES.get(" ".join(head.split(" ")[:2]))
    if ov:
        association, dojo = ov["association"], ov["dojo"]
        flags.append("assoc_override")
    addresses = [a for a in rec["addresses"]]
    addr = addresses[0] if addresses else ""
    if rec["continuations"]:
        addr = (addr + " " + " ".join(rec["continuations"])).strip()
    if addr.startswith("沖那覇市"):
        addr = addr[1:]
        flags.append("source_typo_fixed")
    if not addresses:
        flags.append("no_address_in_roster")
    # kana reading for the instructor (only when pieces and kana line up)
    reading = None
    if kana_tokens:
        if ns is not None and len(kana_tokens) >= 2:
            reading = {"surname": "".join(kana_tokens[:ns]) if len(kana_tokens) >= ns else "",
                       "given": "".join(kana_tokens[ns:])}
        elif len(kana_tokens) == 2:
            reading = {"surname": kana_tokens[0], "given": kana_tokens[1]}
    if reading and (not reading["surname"] or not reading["given"]):
        reading = None
    if re.search(r"[ぁ-ん]", given):
        flags.append("hiragana_in_name")
        reading = None
    if not re.search(r"[一-鿿]", surname) and not re.search(r"[A-Za-z]", surname):
        flags.append("odd_surname")
    return {
        "idx": idx,
        "association_ja": norm_ws(association),
        "dojo_ja": norm_ws(dojo),
        "rep_ja": rep_ja,
        "rep_kana": reading,
        "address_ja": norm_ws(addr),
        "extra_addresses_ja": [norm_ws(a) for a in addresses[1:]],
        "flags": flags,
        "raw": " | ".join(blob),
    }


# Hand-checked corrections, keyed by dojo name as parsed (each verified against the raw text)
POST = {
    "志道館 無聲塾": {"rep_ja": "眞栄城 守信", "rep_kana": {"surname": "マエシロ", "given": "モリノブ"}},
    "長浜山会 清山": {"dojo_ja": "長浜山会", "rep_ja": "清山", "rep_en": "Gordon Breyette",
                  "rep_kana": None, "flags_drop": ["no_furigana_line", "no_given_name"]},
}


def apply_post(rec):
    fix = POST.get(rec["dojo_ja"]) or POST.get(rec["dojo_ja"] + " " + rec["rep_ja"].split(" ")[0])
    if not fix:
        return rec
    for k, v in fix.items():
        if k == "flags_drop":
            rec["flags"] = [f for f in rec["flags"] if f not in v]
        else:
            rec[k] = v
    rec["flags"].append("hand_corrected")
    return rec


def main():
    text = RAW.read_text(encoding="utf-8").splitlines()
    lines = [l for l in text[2:]]  # drop the two header lines
    recs = split_missing_address(parse(lines))
    out = [apply_post(build(r, i + 1)) for i, r in enumerate(recs)]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"records: {len(out)}")
    from collections import Counter
    c = Counter(f for r in out for f in r["flags"])
    print("flags:", dict(c))
    return out


if __name__ == "__main__":
    sys.exit(0 if main() else 1)
