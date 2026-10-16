#!/usr/bin/env python3
"""Static site generator (stdlib only).  python3 scripts/build_site.py  ->  dist/"""
import csv, html, json, os, re, shutil, sys, urllib.parse, datetime
from collections import Counter, defaultdict
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from catalog import DISC, DISCIPLINES, GROUPS, VERIF, STATUS, GROUPS_JA, REGIONS_JA, VERIF_JA, KIND_JA, STYLE_JA, DISC_JA
from geo import MUNI_SLUGS, REGIONS

ROOT = Path(__file__).resolve().parent.parent
DIST = Path(os.environ.get("DIST_DIR", ROOT / "dist"))
CFG = json.loads((ROOT/"config.json").read_text(encoding="utf-8"))
BASE = os.environ.get("BASE_PATH", CFG["base_path"]).rstrip("/")
TODAY = datetime.date.today().isoformat()
esc = lambda s: html.escape(str(s or ""), quote=True)

# ------------------------------------------------------------------ data
def load():
    rows = list(csv.DictReader(open(ROOT/"data/locations.csv", encoding="utf-8-sig")))
    for r in rows:
        r["disc"] = [d for d in r["disciplines"].split(";") if d]
        r["srcs"] = [s for s in r["sources"].split(";") if s]
        r["is_org"] = r["kind"] == "organization"
        _el = r["english"].lower()
        r["eng_level"] = 1 if _el.startswith(("yes", "reported")) else (2 if _el.startswith("likely") else 0)
        r["eng"] = r["eng_level"] > 0
        _m = re.search(r"(?:Google rating|rated) (\d\.\d) \((\d+)(?: reviews?)?\)", r["notes"])
        r["rating"] = (_m.group(1), _m.group(2)) if _m else None
        if r["municipality"] in MUNI_SLUGS:
            r["m_ja"], r["m_en"], r["region"] = MUNI_SLUGS[r["municipality"]]
        else:
            r["m_ja"], r["m_en"] = "", "Location not listed"
    srcs = {s["id"]: s for s in csv.DictReader(open(ROOT/"data/sources.csv", encoding="utf-8-sig"))}
    return rows, srcs

ROWS, SRC = load()
PLACES = [r for r in ROWS if not r["is_org"] and r["status"] != "closed"]
by_disc = defaultdict(list)
for r in ROWS:
    if r["status"] == "closed": continue
    for d in r["disc"]: by_disc[d].append(r)
def n_places(d): return sum(1 for r in by_disc[d] if not r["is_org"])

# ------------------------------------------------------------------ helpers
LANG = "en"
def T(en, ja): return ja if LANG == "ja" else en
LOCAL_PREFIXES = ("/arts", "/areas", "/find", "/start", "/about-data", "/sources", "/suggest-edit", "/for-dojos", "/privacy", "/l/", "/map")
def url(p):
    if LANG == "ja" and (p == "/" or p.startswith(LOCAL_PREFIXES)): p = "/ja" + (p if p != "/" else "/")
    return f"{BASE}{p}"
def vlabel(k): return (VERIF_JA if LANG == "ja" else VERIF)[k]
def dname(d): return DISC[d]["ja"] if LANG == "ja" else DISC[d]["en"]
def dtext(d, i):  # i: 0 blurb, 1 about, 2 beginner
    if LANG == "ja": return DISC_JA[d][i]
    return (DISC[d]["blurb"], DISC[d]["about"], DISC[d]["beginner"])[i]
def mname(slug): return MUNI_SLUGS[slug][0] if LANG == "ja" else MUNI_SLUGS[slug][1]
def write(path, content):
    f = DIST / path.lstrip("/"); f.parent.mkdir(parents=True, exist_ok=True); f.write_text(content, encoding="utf-8")

def issue_url(r, kind="report-listing.yml"):
    if not CFG.get("use_github", True): return mail_url(r)
    q = urllib.parse.urlencode({"template": kind, "title": f"[Edit] {r['name_en']}", "listing": r["id"]})
    return f"https://github.com/{CFG['github_repo']}/issues/new?{q}"
def mail_url(r):
    s = urllib.parse.quote(f"Correction: {r['name_en']} ({r['id']})")
    b = urllib.parse.quote(f"Listing: {CFG['base_url']}/l/{r['id']}/\n\nWhat is wrong / what changed:\n\nHow do you know (website, phone call, I run it):\n")
    return f"mailto:{CFG['contact_email']}?subject={s}&body={b}"

ANALYTICS = CFG.get("analytics_snippet", "")

def report_buttons(r):
    if CFG.get("use_github", True):
        return f'<a class="btn" href="{esc(issue_url(r))}" rel="noopener">{T("Report a problem","誤りを報告")}</a> <a class="btn secondary" href="{esc(mail_url(r))}">{T("Email instead","メールで連絡")}</a>'
    return f'<a class="btn" href="{esc(mail_url(r))}">{T("Report a problem","誤りを報告")}</a>'

def header(cur="", alt=None):
    groups = []
    for g in GROUPS:
        items = "".join(f'<a href="{url("/arts/"+d["slug"]+"/")}"><span>{esc(dname(d["slug"]))}</span><span class="n">{n_places(d["slug"])}</span></a>'
                        for d in DISC.values() if d["group"] == g)
        groups.append(f"<h3>{esc(T(g, GROUPS_JA[g]))}</h3>{items}")
    def a(href, label, key): return f'<a href="{url(href)}"{" aria-current=page" if cur==key else ""}>{label}</a>'
    langlink = f'<a href="{BASE}{alt}" hreflang="{"en" if LANG=="ja" else "ja"}" lang="{"en" if LANG=="ja" else "ja"}" style="border:1px solid var(--line)">{"English" if LANG=="ja" else "日本語"}</a>' if alt else ""
    return f'''<a class="skip" href="#main">{T("Skip to content","本文へスキップ")}</a>
<header class="site"><div class="wrap">
<a class="brand" href="{url("/")}"><span class="mark" aria-hidden="true">武</span><span>{esc(T(CFG["site_name"], CFG["site_name_ja"]))}<small lang="{T("ja","en")}">{esc(T(CFG["site_name_ja"], CFG["site_name"]))}</small></span></a>
<nav class="main" aria-label="{T("Main","メイン")}">
<details><summary>{T("Arts ▾","武道・種目 ▾")}</summary><div class="menu">{"".join(groups)}<a href="{url("/arts/")}" style="grid-column:1/-1;margin-top:6px;font-weight:600">{T("All arts →","すべての種目 →")}</a></div></details>
{a("/areas/",T("Areas","地域"),"areas")}{a("/map/",T("Map","地図"),"map")}{a("/find/",T("Search","検索"),"find")}{a("/start/",T("New to training?","初めての方へ"),"start")}{a("/about-data/",T("About the data","データについて"),"about")}{langlink}
</nav></div></header>'''

def footer():
    if LANG == "ja":
        return f'''<footer class="site"><div class="wrap"><div class="cols">
<div><h4>{esc(CFG["site_name_ja"])}</h4><p>沖縄の武道・格闘技を紹介する、独立した有志運営のガイドです。道場・連盟・行政機関とは関係ありません。最終ビルド {TODAY}。※営業時間・備考など掲載詳細の一部は原文（英語）のままです。</p></div>
<div><h4>探す</h4><ul><li><a href="{url("/find/")}">すべてを検索</a></li><li><a href="{url("/areas/")}">地域から探す</a></li><li><a href="{url("/map/")}">地図</a></li><li><a href="{url("/start/")}">初めての方へ</a></li></ul></div>
<div><h4>信頼性・お問い合わせ</h4><ul><li><a href="{url("/about-data/")}">データについて</a></li><li><a href="{url("/sources/")}">情報源と帰属</a></li><li><a href="{url("/suggest-edit/")}">修正・追加の提案</a></li><li><a href="{url("/for-dojos/")}">道場・ジムの運営者の方へ</a></li><li><a href="{url("/privacy/")}">プライバシーと削除依頼</a></li></ul></div>
</div></div></footer>'''
    return f'''<footer class="site"><div class="wrap"><div class="cols">
<div><h4>{esc(CFG["site_name"])}</h4><p>An independent, community-maintained guide to martial arts and combat sports in Okinawa. Not affiliated with any dojo, federation or government body. Last built {TODAY}.</p></div>
<div><h4>Explore</h4><ul><li><a href="{url("/find/")}">Search all places</a></li><li><a href="{url("/areas/")}">Browse by area</a></li><li><a href="{url("/map/")}">Map</a></li><li><a href="{url("/start/")}">Beginner guide</a></li><li><a href="{url("/arts/")}">All arts</a></li></ul></div>
<div><h4>Trust &amp; help</h4><ul><li><a href="{url("/about-data/")}">About this data</a></li><li><a href="{url("/sources/")}">Sources &amp; attribution</a></li><li><a href="{url("/suggest-edit/")}">Suggest an edit</a></li><li><a href="{url("/for-dojos/")}">For dojo &amp; gym owners</a></li><li><a href="{url("/privacy/")}">Privacy &amp; removal</a></li></ul></div>
</div></div></footer>'''

def page(path, title, desc, body, cur="", noindex=False, jsonld=None, extra_head="", scripts=""):
    pf = "/ja" if LANG == "ja" else ""
    full_path = pf + path
    canon = f'{CFG["base_url"]}{full_path}'
    en_p = path; ja_p = "/ja" + path
    alt = en_p if LANG == "ja" else ja_p
    hl = f'<link rel="alternate" hreflang="en" href="{CFG["base_url"]}{en_p}"><link rel="alternate" hreflang="ja" href="{CFG["base_url"]}{ja_p}"><link rel="alternate" hreflang="x-default" href="{CFG["base_url"]}{en_p}">'
    ld = f'<script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False)}</script>' if jsonld else ""
    robots = '<meta name="robots" content="noindex,follow">' if noindex else ""
    full = f'''<!doctype html><html lang="{LANG}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title><meta name="description" content="{esc(desc)}"><link rel="canonical" href="{esc(canon)}">{hl}{robots}
<meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:type" content="website"><meta property="og:locale" content="{"ja_JP" if LANG=="ja" else "en_US"}">
<meta name="color-scheme" content="light dark"><link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='7' fill='%231f2f5a'/%3E%3Ctext x='16' y='24' font-size='22' text-anchor='middle' fill='white'%3E武%3C/text%3E%3C/svg%3E">
<link rel="stylesheet" href="{url("/assets/style.css")}">{extra_head}{ld}{ANALYTICS}</head><body>{header(cur, alt)}<main id="main">{body}</main>{footer()}{scripts}<script src="{url("/assets/app.js")}" defer></script></body></html>'''
    write(full_path.rstrip("/") + "/index.html" if full_path != "/" else "index.html", full)

def badge(v): return f'<span class="badge {v}" title="{esc(vlabel(v)[1])}">{esc(vlabel(v)[0])}</span>'
def style_txt(r): return STYLE_JA.get(r["style"], r["style"]) if LANG == "ja" else r["style"]

def primary_name(r):
    if LANG == "ja": return r["name_ja"] or r["name_en"]
    return r["name_en"]
def secondary_name(r):
    if LANG == "ja": return r["name_en"] if (r["name_ja"] and r["verification"] != "C") else ""
    return r["name_ja"]
def loc_text(r):
    if LANG == "ja": return r["address_ja"] or r["address_en"] or r["m_ja"] or "所在地未掲載"
    return r["address_en"] or r["m_en"]

def eng_chips(r):
    out = ""
    if r["eng_level"] == 1: out += f"<span class='chip'>🗣 {T('English','英語OK')}</span>"
    elif r["eng_level"] == 2: out += f"<span class='chip'>🗣 {T('English (likely)','英語可の可能性')}</span>"
    if r["rating"]: out += f"<span class='chip' title='{T('Google rating (number of reviews)','Googleの評価（口コミ件数）')}'>★ {r['rating'][0]} ({r['rating'][1]})</span>"
    return out

def card(r):
    chips = "".join(f'<span class="chip">{esc(dname(d))}</span>' for d in r["disc"] if d in DISC)
    phone = f'<a href="tel:{esc("".join(c for c in r["phone"] if c.isdigit() or c=="+"))}">☎ {esc(r["phone"])}</a>' if r["phone"] and r["phone"][0].isdigit() else ""
    web = f'<a href="{esc(r["website"] if r["website"].startswith("http") else "https://"+r["website"])}" rel="noopener nofollow">{T("Website ↗","ウェブサイト ↗")}</a>' if r["website"] else ""
    sec = secondary_name(r)
    jl = ' lang="ja"' if LANG == "en" else ""
    sec_html = f'<div class="ja"{jl}>{esc(sec)}</div>' if sec else ""
    org = f"<span class='chip'>{T('Organization','団体')}</span>" if r["is_org"] else ""
    return f'''<article class="card"><div class="pill-row">{badge(r["verification"])}{org}{chips}{eng_chips(r)}</div>
<h3><a href="{url("/l/"+r["id"]+"/")}">{esc(primary_name(r))}</a></h3>{sec_html}
<div class="meta"><span>📍 {esc(loc_text(r))}</span>{phone}{web}</div></article>'''

def switcher(cur):
    opts = "".join(f'<option value="{url("/arts/"+d["slug"]+"/")}"{" selected" if d["slug"]==cur else ""}>{esc(d["en"] if LANG=="en" else d["ja"])}{" — "+esc(d["ja"]) if LANG=="en" else ""} ({n_places(d["slug"])})</option>' for d in DISC.values())
    links = " · ".join(f'<a href="{url("/arts/"+d["slug"]+"/")}">{esc(dname(d["slug"]))}</a>' for d in DISC.values())
    return f'''<div class="switcher"><label for="art-switch"><b>{T("Switch art","種目を切り替え")}</b></label>
<select id="art-switch" data-nav aria-label="{T("Switch to another martial art","別の武道・種目へ移動")}">{opts}</select>
<noscript><p>{links}</p></noscript></div>'''

def grouped_cards(rs):
    out = []
    rs = sorted(rs, key=lambda r: (r["verification"], r["name_en"].lower()))
    for key, label in REGIONS + [("", "Location not listed")]:
        sub = [r for r in rs if (r.get("region") or "") == key] if key else [r for r in rs if not r.get("region")]
        if not sub: continue
        lab = REGIONS_JA[key] if LANG == "ja" else label
        out.append(f'<h2 class="region">{esc(lab)} <small style="font-weight:400;color:var(--muted)">· {len(sub)}</small></h2>')
        bym = defaultdict(list)
        for r in sub: bym[r["m_ja"] if LANG == "ja" else r["m_en"]].append(r)
        for m in sorted(bym):
            out.append(f'<h3 class="muni-head">{esc(m or T("Location not listed","所在地未掲載"))} <small style="color:var(--muted)">({len(bym[m])})</small></h3><div class="cards">{"".join(card(r) for r in bym[m])}</div>')
    return "".join(out)

def short_ja(n): return n[:-1] if n[-1] in "市町村" and len(n) > 2 else n

def tilemap(counts, link_prefix="/areas/", caption=None):
    caption = caption or T("places listed", "件掲載")
    pos = {"kunigami":(7,1),"nakijin":(5,2),"motobu":(5,3),"nago":(6,3),"ginoza":(7,3),"onna":(6,4),"kin":(7,4),
           "yomitan":(5,5),"uruma":(7,5),"kadena":(5,6),"okinawa-city":(6,6),"chatan":(4,7),"kitanakagusuku":(5,7),"nakagusuku":(6,7),
           "ginowan":(4,8),"nishihara":(5,8),"yonabaru":(6,8),"urasoe":(3,9),"naha":(4,9),"haebaru":(5,9),"nanjo":(6,9),
           "tomigusuku":(4,10),"yaese":(5,10),"itoman":(4,11)}
    mx = max([counts.get(s, 0) for s in pos] + [1])
    def lvl(n): return 0 if n == 0 else 1 if n <= mx*0.2 else 2 if n <= mx*0.45 else 3 if n <= mx*0.7 else 4
    def tile(slug, style=""):
        n = counts.get(slug, 0); ja, en, _ = MUNI_SLUGS[slug]
        name = short_ja(ja) if LANG == "ja" else en.split(" (")[0]
        inner = f"<span>{esc(name)}</span><b>{n}</b>"
        cls = f"tile l{lvl(n)}" + (" zero" if n == 0 else "")
        lab = f'aria-label="{esc(name)}: {n} {esc(caption)}"'
        if n: return f'<a class="{cls}" style="{style}" href="{url(link_prefix+slug+"/")}" {lab}>{inner}</a>'
        return f'<div class="{cls}" style="{style}" {lab}>{inner}</div>'
    tiles = "".join(tile(s, f"grid-column:{x};grid-row:{y}") for s, (x, y) in pos.items())
    isl = "".join(tile(s) for s in ("kumejima","miyako","tarama","ishigaki"))
    return f'''<div class="tilemap-wrap"><div class="tilemap" role="group" aria-label="{T("Okinawa main island, municipalities as tiles. North is up.","沖縄本島の市町村をタイルで表示（上が北）")}">{tiles}<span class="north-arrow" aria-hidden="true">↑ {T("North","北")}</span></div>
<div class="islands"><span class="label">{T("Outer islands →","離島 →")}</span>{isl}</div>
<div class="legend"><span>{T("Fewer","少")}</span><i style="background:var(--tile1)"></i><i style="background:var(--tile2)"></i><i style="background:var(--tile3)"></i><i style="background:var(--tile4)"></i><span>{T("More","多")} ({esc(caption)})</span><span>· {T("dashed tile = none listed yet (not “none exist”)","破線のタイル＝未掲載（「存在しない」ではありません）")}</span></div></div>'''

def art_card(d):
    k = d["ja"].split("・")[0]
    sty = ' style="font-size:1.45rem"' if len(k) > 5 else ""
    return f'<a class="art-card" href="{url("/arts/"+d["slug"]+"/")}"><span class="cnt">{n_places(d["slug"])}</span><span class="kanji" lang="ja"{sty}>{esc(k)}</span><span class="name">{esc(d["en"] if LANG=="en" else d["ja"])}</span><p>{esc(dtext(d["slug"],0))}</p></a>'

def build_home():
    muni_counts = Counter(r["municipality"] for r in PLACES if r["municipality"])
    arts = "".join(art_card(d) for d in DISC.values() if n_places(d["slug"]))
    area_opts = "".join(f'<option value="{s}">{esc(mname(s))}</option>' for s in sorted(muni_counts, key=lambda s: MUNI_SLUGS[s][1]))
    art_opts = "".join(f'<option value="{d["slug"]}">{esc(dname(d["slug"]))}</option>' for d in DISC.values() if n_places(d["slug"]))
    verified = sum(1 for r in PLACES if r["verification"] == "A")
    n, na = len(PLACES), len(ARTS_WITH)
    if LANG == "ja":
        hero = f'''<span class="jp">空手発祥の地 · 沖縄</span><h1>沖縄で、道場を見つけよう。</h1><p class="lede">{na}種目・{n}か所の稽古場所を、地域と種目で検索できます。各掲載には「いつ確認したか」を正直に表示しています。</p>'''
    else:
        hero = f'''<span class="jp">空手発祥の地 · 沖縄</span><h1>Find your dojo in Okinawa.</h1><p class="lede">{n} places to train across {na} martial arts and combat sports — searchable by area and style, with honest labels showing how recently each one was checked.</p>'''
    body = f'''<section class="hero"><div class="wrap">{hero}
<form id="home-search" class="searchbox" action="{url("/find/")}" role="search"><div><label for="h-q">{T("Name, place or instructor","名称・地名・指導者")}</label><input id="h-q" name="q" type="search" placeholder="{T("e.g. Naha, Goju-ryu, 那覇","例：那覇、剛柔流、Naha")}" autocomplete="off"></div>
<div><label for="h-art">{T("Art","種目")}</label><select id="h-art" name="art"><option value="">{T("Any art","すべて")}</option>{art_opts}</select></div>
<div><label for="h-area">{T("Area","地域")}</label><select id="h-area" name="area"><option value="">{T("Anywhere in Okinawa","沖縄全域")}</option>{area_opts}</select></div>
<button type="submit">{T("Search","検索")}</button></form>
<div class="stats"><div><b>{n}</b><span>{T("places listed","掲載件数")}</span></div><div><b>{na}</b><span>{T("arts","種目")}</span></div><div><b>{len(muni_counts)}</b><span>{T("municipalities","市町村")}</span></div><div><b>{verified}</b><span>{T("checked Oct 2026","2026年10月確認")}</span></div></div></div></section>
<section class="block"><div class="wrap"><h2>{T("Browse by art","種目から探す")} <span class="jp">武道</span></h2><p class="sub">{T("Each art has its own page with an explanation, beginner notes and every listing. Use the “Switch art” menu on any page to hop between them.","各種目に、解説・初心者向けの案内・全掲載をまとめたページがあります。どのページでも「種目を切り替え」から移動できます。")}</p><div class="arts-grid">{arts}</div></div></section>
<section class="block"><div class="wrap"><h2>{T("Browse by area","地域から探す")} <span class="jp">地域</span></h2><p class="sub">{T("Each tile is a municipality, placed roughly where it sits on the island. Darker means more listings.","各タイルは市町村で、おおよその位置に並べています。色が濃いほど掲載が多い地域です。")} <a href="{url("/map/")}">{T("Open the map →","地図を開く →")}</a></p>{tilemap(muni_counts)}</div></section>
<section class="block"><div class="wrap two"><div><h2>{T("New to training here?","初めての方へ")}</h2><p>{T("Visiting for a week or settling in for years — our beginner guide covers how to ask for a trial in Japanese, etiquette, what to bring, and which places are used to English speakers.","数日の滞在でも長期の移住でも。体験の申し込み方、礼儀作法、持ち物、英語対応のある場所などを案内します。")}</p><p><a class="btn" href="{url("/start/")}">{T("Read the guide","ガイドを読む")}</a> <a class="btn secondary" href="{url("/find/?eng=1")}">{T("English-friendly places","英語対応あり")}</a></p></div>
<div><h2>{T("Know something we don't?","情報をお持ちですか？")}</h2><p>{T("Dojo move, close and change phone numbers. Every listing has a “Report a problem” link, and owners can claim, update or remove their entry.","道場の移転・閉鎖・電話番号の変更はよくあります。各掲載に「誤りを報告」リンクがあり、運営者ご本人は掲載の更新・削除もできます。")} <a href="{url("/about-data/")}">{T("How we check the data","確認方法")}</a> · <a href="{url("/sources/")}">{T("Sources","情報源")}</a></p><p><a class="btn secondary" href="{url("/suggest-edit/")}">{T("Suggest an edit","修正・追加を提案")}</a></p></div></div></section>'''
    page("/", T(f'{CFG["site_name"]} — find a dojo, gym or club', f'{CFG["site_name_ja"]} — 道場・ジム・クラブを探す'),
         T(f'{n} karate, kobudo, judo, BJJ, MMA, boxing, kendo and other martial arts places in Okinawa, searchable by area and style.', f'沖縄の空手・古武道・柔道・BJJ・MMA・ボクシング・剣道など{n}か所を、地域と種目で検索。'), body, cur="home",
         jsonld={"@context":"https://schema.org","@type":"WebSite","name":CFG["site_name"],"url":CFG["base_url"]})

def build_arts_index():
    out = []
    for g in GROUPS:
        cards = "".join(art_card(d) for d in DISC.values() if d["group"] == g)
        out.append(f'<h2 class="region">{esc(T(g, GROUPS_JA[g]))}</h2><div class="arts-grid">{cards}</div>')
    rows = "".join(f'<tr><td><a href="{url("/arts/"+d["slug"]+"/")}">{esc(dname(d["slug"]))}</a></td><td lang="ja">{esc(d["ja"])}</td><td>{n_places(d["slug"])}</td><td>{sum(1 for r in by_disc[d["slug"]] if r["is_org"])}</td></tr>' for d in DISC.values())
    body = f'''<div class="wrap pagehead"><div class="crumbs"><a href="{url("/")}">{T("Home","ホーム")}</a> › {T("Arts","種目")}</div><h1>{T("All arts","すべての種目")}</h1>
<p class="sub">{T("Places to train are counted separately from governing bodies. A place that teaches several arts is counted under each.","稽古場所と統括団体は別々に数えています。複数の種目を教える場所は、それぞれの種目で数えます。")}</p>{switcher("")}{"".join(out)}
<h2 class="region">{T("Counts at a glance","件数一覧")}</h2><table class="data"><thead><tr><th>{T("Art","種目")}</th><th>日本語</th><th>{T("Places to train","稽古場所")}</th><th>{T("Governing bodies","統括団体")}</th></tr></thead><tbody>{rows}</tbody></table></div>'''
    page("/arts/", T("All martial arts in Okinawa","沖縄の武道・格闘技の種目一覧"), T("Every martial art and combat sport we list in Okinawa, with counts.","掲載している全種目と件数。"), body, cur="arts")

def build_art(d):
    s = d["slug"]; rs = by_disc[s]
    places = [r for r in rs if not r["is_org"]]; orgs = [r for r in rs if r["is_org"]]
    mc = Counter(r["municipality"] for r in places if r["municipality"])
    chk = Counter(r["verification"] for r in places)
    styles = Counter(style_txt(r) for r in places)
    top_styles = "".join(f"<tr><td>{esc(k)}</td><td>{v}</td></tr>" for k, v in styles.most_common(14))
    orgs_html = f'<h2 class="region">{T("Governing bodies & contacts","統括団体・連絡先")}</h2><div class="cards">{"".join(card(r) for r in orgs)}</div>' if orgs else ""
    nm = dname(s)
    sub = T(f'{len(places)} place{"s" if len(places)!=1 else ""} to train · {len(mc)} municipalit{"ies" if len(mc)!=1 else "y"} · {chk["A"]} checked Oct 2026', f'稽古場所 {len(places)}か所 · {len(mc)}市町村 · 2026年10月確認 {chk["A"]}件')
    body = f'''<div class="wrap pagehead"><div class="crumbs"><a href="{url("/")}">{T("Home","ホーム")}</a> › <a href="{url("/arts/")}">{T("Arts","種目")}</a> › {esc(nm)}</div>
<span class="kanji" lang="ja">{esc(d["ja"])}</span><h1>{esc(T(d["en"]+" in Okinawa", "沖縄の"+d["ja"]))}</h1><p class="sub">{sub}</p>{switcher(s)}
<div class="two"><div class="prose"><p>{esc(dtext(s,1))}</p><div class="callout info"><b>{T("For beginners:","初心者の方へ：")}</b> {esc(dtext(s,2))}</div>
<p><a class="btn" href="{url("/find/?art="+s)}">{T("Search & filter","検索・絞り込み")}</a> <a class="btn secondary" href="{url("/map/?art="+s)}">{T("See on map","地図で見る")}</a></p></div>
<div>{tilemap(mc, caption=T("places","件")) if mc else ""}</div></div>
{('<h2 class="region">'+T("Styles listed","掲載されている流派・スタイル")+'</h2><table class="data"><thead><tr><th>'+T("Style / affiliation","流派・スタイル")+'</th><th>'+T("Places","件数")+'</th></tr></thead><tbody>'+top_styles+'</tbody></table>') if len(styles)>1 else ""}
{grouped_cards(places)}{orgs_html}</div>'''
    page(f"/arts/{s}/", T(f'{d["en"]} in Okinawa — {len(places)} places to train', f'沖縄の{d["ja"]} — 稽古場所{len(places)}か所'), dtext(s,0), body, cur="arts")

def build_areas():
    muni_counts = Counter(r["municipality"] for r in PLACES if r["municipality"])
    unk = sum(1 for r in PLACES if not r["municipality"])
    lists = []
    for key, label in REGIONS:
        items = [(s, MUNI_SLUGS[s]) for s in muni_counts if MUNI_SLUGS[s][2] == key]
        if not items: continue
        lis = "".join(f'<tr><td><a href="{url("/areas/"+s+"/")}">{esc(v[0] if LANG=="ja" else v[1])}</a></td><td lang="ja">{esc(v[0])}</td><td>{muni_counts[s]}</td><td><div class="bar" style="width:{max(2,int(muni_counts[s]/max(muni_counts.values())*160))}px"></div></td></tr>' for s, v in sorted(items, key=lambda x: -muni_counts[x[0]]))
        lists.append(f'<h2 class="region">{esc(REGIONS_JA[key] if LANG=="ja" else label)}</h2><table class="data"><thead><tr><th>{T("Municipality","市町村")}</th><th>日本語</th><th>{T("Places","件数")}</th><th></th></tr></thead><tbody>{lis}</tbody></table>')
    unk_t = T(f'{unk} listing(s) have no location we could confirm yet.', f'{unk}件は、所在地をまだ確認できていません。') if unk else ""
    body = f'''<div class="wrap pagehead"><div class="crumbs"><a href="{url("/")}">{T("Home","ホーム")}</a> › {T("Areas","地域")}</div><h1>{T("Browse by area","地域から探す")}</h1>
<p class="sub">{T("Counts are places we have listed, not every place that exists. Areas covered mostly by the 2019 roster (karate) will read higher than areas where only gyms are known.","件数は「掲載している数」であり、実在する数ではありません。2019年名簿（空手）が中心の地域は多く、ジムのみが分かっている地域は少なく見えます。")}</p>{tilemap(muni_counts)}
{"".join(lists)}{f'<p class="sub" style="margin-top:20px">{unk_t}</p>' if unk else ""}</div>'''
    page("/areas/", T("Martial arts in Okinawa by area","沖縄の武道・格闘技（地域別）"), T("Browse dojo, gyms and clubs by municipality across Okinawa.","市町村ごとに道場・ジム・クラブを探せます。"), body, cur="areas")

def build_area(slug):
    ja, en, region = MUNI_SLUGS[slug]
    rs = [r for r in ROWS if r["municipality"] == slug and r["status"] != "closed"]
    places = [r for r in rs if not r["is_org"]]
    dc = Counter(d for r in places for d in r["disc"])
    pills = " ".join(f'<a class="chip" href="{url("/find/?area="+slug+"&art="+d)}">{esc(dname(d))} · {n}</a>' for d, n in dc.most_common() if d in DISC)
    ordered = sorted(rs, key=lambda r: (r["verification"], r["name_en"].lower()))
    nm = ja if LANG == "ja" else en
    body = f'''<div class="wrap pagehead"><div class="crumbs"><a href="{url("/")}">{T("Home","ホーム")}</a> › <a href="{url("/areas/")}">{T("Areas","地域")}</a> › {esc(nm)}</div>
<span class="kanji" lang="ja">{esc(ja)}</span><h1>{esc(T("Martial arts in "+en, ja+"の武道・格闘技"))}</h1><p class="sub">{T(f'{len(places)} place{"s" if len(places)!=1 else ""} listed · {len(dc)} art{"s" if len(dc)!=1 else ""}', f'{len(places)}か所掲載 · {len(dc)}種目')}</p>
<div class="pill-row" style="margin:10px 0 18px">{pills}</div><div class="cards">{"".join(card(r) for r in ordered)}</div></div>'''
    page(f"/areas/{slug}/", T(f"Martial arts in {en}, Okinawa — {len(places)} listings", f"{ja}の武道・格闘技 — {len(places)}件"), T(f"Dojo, gyms and clubs in {en} ({ja}), Okinawa, by style.", f"{ja}の道場・ジム・クラブ。"), body, cur="areas")

def row(k, v, raw=False):
    return f"<dt>{esc(k)}</dt><dd>{v if raw else esc(v)}</dd>" if v else ""

def build_listing(r):
    chips = "".join(f'<a class="chip" href="{url("/arts/"+d+"/")}">{esc(dname(d))}</a>' for d in r["disc"] if d in DISC)
    web = r["website"] if r["website"].startswith("http") or not r["website"] else "https://" + r["website"]
    has_ll = bool(r["lat"] and r["lon"])
    gq = f'{r["lat"]},{r["lon"]}' if has_ll else (r["address_ja"] if r["municipality"] and r["address_ja"] else (r["name_ja"] + " 沖縄"))
    gmaps = ("https://www.google.com/maps/search/?api=1&query=" + urllib.parse.quote(gq)) if (r["kind"] != "organization" or r["address_ja"]) else ""
    tel = f'<a href="tel:{esc("".join(c for c in r["phone"] if c.isdigit() or c=="+"))}">{esc(r["phone"])}</a>' if r["phone"] and r["phone"][0].isdigit() else r["phone"]
    eng = r["english"] if r["english"] != "unknown" else T("Not known — ask when you contact them", "不明（問い合わせ時に確認）")
    facts = "".join([
        row(T("Japanese name","日本語名"), r["name_ja"]) if LANG == "en" else row("名称（英語）", r["name_en"] if r["verification"] != "C" else ""),
        row(T("Style","流派・スタイル"), style_txt(r)), row(T("Type","種別"), r["kind"].capitalize() if LANG=="en" else KIND_JA.get(r["kind"], r["kind"])),
        row(T("Address (Japanese)","住所"), r["address_ja"]), row(T("Where (English)","所在地（英語）") if LANG=="en" else "所在地", r["address_en"] if LANG=="en" else (r["m_ja"] if not r["address_ja"] else "")),
        row(T("Phone","電話"), tel, raw=True),
        row(T("Website","ウェブサイト"), f'<a href="{esc(web)}" rel="noopener nofollow">{esc(r["website"])}</a>' if web else "", raw=True),
        row("SNS" if LANG=="ja" else "Social", f'<a href="{esc(r["social"])}" rel="noopener nofollow">{esc(r["social"])}</a>' if r["social"].startswith("http") else r["social"], raw=True),
        row(T("Email","メール"), f'<a href="mailto:{esc(r["email"])}">{esc(r["email"])}</a>' if r["email"] else "", raw=True),
        row(T("Hours / classes","稽古日時"), r["hours"]), row(T("Instructor / contact","指導者・連絡先"), r["contact"]), row(T("Visitors & trials","見学・体験"), r["visitors"]),
        row(T("English","英語対応"), eng), row(T("Also known as","別名"), r["aliases"]),
    ])
    srcs = ", ".join(f'<a href="{url("/sources/")}#{esc(s)}">{esc(SRC[s]["title"].split(" — ")[0][:60])}</a>' for s in r["srcs"] if s in SRC)
    verif_txt = f'{badge(r["verification"])} <span class="sub">{esc(vlabel(r["verification"])[1])}</span>'
    if r["status"] == "needs_check": verif_txt += T('<div class="callout"><b>Needs a check.</b> We could not fully confirm this listing — call or look at the operator\'s own page before travelling.</div>','<div class="callout"><b>要確認。</b>この掲載は十分に確認できていません。お出かけ前に電話か運営者のページでご確認ください。</div>')
    if r["verification"] == "C": verif_txt += T('<div class="callout"><b>Heads up:</b> this dojo comes from the 2019 prefectural roster and has not been re-checked. Phone numbers are often not published for traditional dojo — if you know them, please <a href="'+esc(issue_url(r))+'">tell us</a>.</div>','<div class="callout"><b>ご注意：</b>この道場は2019年の県内道場名簿の掲載で、再確認していません。伝統道場は電話番号が公開されていないことが多く、ご存じでしたら<a href="'+esc(issue_url(r))+'">お知らせください</a>。</div>')
    ld = None
    if r["verification"] in ("A", "B") and r["kind"] != "organization":
        ld = {"@context":"https://schema.org","@type":"SportsActivityLocation","name":r["name_en"],"alternateName":r["name_ja"] or None,"url":web or None,
              "telephone":r["phone"] or None,"address":{"@type":"PostalAddress","addressCountry":"JP","addressRegion":"Okinawa","addressLocality":r["m_en"],"streetAddress":r["address_ja"] or None}}
        if has_ll: ld["geo"] = {"@type":"GeoCoordinates","latitude":float(r["lat"]),"longitude":float(r["lon"])}
        ld = {k: v for k, v in ld.items() if v}
        ld["address"] = {k: v for k, v in ld["address"].items() if v}
    first = r["disc"][0] if r["disc"] and r["disc"][0] in DISC else None
    sec = secondary_name(r)
    nt = f'<p>{esc(r["notes"])}</p>' if r["notes"] else ""
    body = f'''<div class="wrap pagehead"><div class="crumbs"><a href="{url("/")}">{T("Home","ホーム")}</a> › {f'<a href="{url("/arts/"+first+"/")}">{esc(dname(first))}</a>' if first else ""} › {esc(primary_name(r))}</div>
<div class="pill-row" style="margin-top:8px">{chips}{"<span class='chip'>"+T("Organization","団体")+"</span>" if r["is_org"] else ""}{eng_chips(r)}</div>
<h1>{esc(primary_name(r))}</h1>{f'<div lang="{T("ja","en")}" style="font-family:var(--jp);color:var(--muted);font-size:1.15rem">{esc(sec)}</div>' if sec else ""}
<div style="margin:14px 0">{verif_txt}</div>
<div class="two"><div><dl class="facts">{facts}</dl>{nt}
<p class="sub" style="font-size:.85rem">{T("Sources","情報源")}: {srcs or "—"} · {T("Source date","情報の時点")}: {esc(r["source_date"] or "—")} · {T("Last verified","最終確認")}: {esc(r["last_verified"] or T("not yet","未確認"))}{(" · "+esc(r["privacy_note"])) if r["privacy_note"] else ""}</p></div>
<div><div class="callout info"><b>{T("Something wrong or changed?","誤りや変更がありますか？")}</b><p style="margin:.4em 0">{T("Dojo close, move and change numbers. Two minutes of your time keeps this useful for the next person.","道場は閉鎖・移転・番号変更があります。数分のご協力が、次に探す人の助けになります。")}</p>
<p>{report_buttons(r)}</p>
<p style="font-size:.88rem;margin-bottom:0">{T("Run this place?","運営者の方は")} <a href="{url("/for-dojos/")}">{T("Claim, update or remove it","掲載の更新・削除")}</a>.</p></div>
{f'<p><a class="btn secondary" href="{esc(gmaps)}" rel="noopener nofollow">{T("Open in Google Maps ↗","Googleマップで開く ↗")}</a> <a class="btn secondary" href="{url("/map/?id="+r["id"])}">{T("Show on our map","このサイトの地図で見る")}</a></p>' if gmaps else ""}
<p class="sub" style="font-size:.85rem">{T("We don't embed Google Maps or copy map-service data; the link opens a search in your own map app.","Googleマップの埋め込みや地図サービスのデータの複製は行いません。リンクは、お使いの地図アプリで検索を開きます。")}</p></div></div></div>'''
    noindex = (r["verification"] == "C" and not CFG["index_roster_pages"])
    page(f'/l/{r["id"]}/', T(f'{r["name_en"]} — {r["m_en"]}, Okinawa', f'{primary_name(r)} — {r["m_ja"] or "沖縄"}'),
         T(f'{r["name_en"]} ({r["style"]}) in {r["m_en"]}, Okinawa. {VERIF[r["verification"]][0]}.', f'{primary_name(r)}（{style_txt(r)}）。{r["m_ja"]}。{VERIF_JA[r["verification"]][0]}。'), body, cur="", noindex=noindex, jsonld=ld)

def data_blob():
    ui = T({"places":"places","place":"place","none":"No matches. Try removing a filter — many small dojo are listed in Japanese only, so a Japanese place name (e.g. 那覇) can help.","more":"Show more","website":"Website ↗","noloc":"Location not listed","km":"km","org":"Organization","nocoord":"Distance needs coordinates — only places with a map position are ranked.","locating":"Finding your location…","denied":"Couldn’t get your location (permission denied or unavailable)."},
           {"places":"件","place":"件","none":"該当なし。絞り込みを外してみてください。小規模な道場は日本語表記のみのことが多く、地名（例：那覇）で探すと見つかる場合があります。","more":"さらに表示","website":"ウェブサイト ↗","noloc":"所在地未掲載","km":"km","org":"団体","nocoord":"距離順は、地図上の位置が分かる場所のみが対象です。","locating":"現在地を取得中…","denied":"現在地を取得できませんでした（許可がない、または利用できません）。"})
    ui = dict(ui); ui.update(T({"eng":"English","engl":"English (likely)"},{"eng":"英語OK","engl":"英語可の可能性"}))
    locs = []
    for r in ROWS:
        if r["status"] == "closed": continue
        locs.append({"id": r["id"], "n": primary_name(r), "j": secondary_name(r), "a": loc_text(r), "aj": r["address_ja"], "m": r["municipality"], "m_en": r["m_en"] if LANG=="en" else r["m_ja"],
                     "d": r["disc"], "k": r["kind"], "v": r["verification"], "p": r["phone"], "w": (r["website"] if r["website"].startswith("http") or not r["website"] else "https://"+r["website"]),
                     "c": r["contact"], "s": style_txt(r), "al": r["aliases"], "e": r["eng_level"], "r": list(r["rating"]) if r["rating"] else None,
                     "la": float(r["lat"]) if r["lat"] else None, "lo": float(r["lon"]) if r["lon"] else None, "ne": r["name_en"] if LANG=="ja" else r["name_ja"]})
    return {"base": BASE, "pfx": "/ja" if LANG == "ja" else "", "disc": {k: dname(k) for k in DISC}, "verif": {k: list(vlabel(k)) for k in "ABCD"}, "ui": ui, "locations": locs}

def build_find():
    art_opts = "".join(f'<option value="{d["slug"]}">{esc(dname(d["slug"]))} ({n_places(d["slug"])})</option>' for d in DISC.values() if by_disc[d["slug"]])
    mc = Counter(r["municipality"] for r in ROWS if r["municipality"] and r["status"] != "closed")
    area_opts = "".join(f'<option value="{s}">{esc(mname(s))} ({mc[s]})</option>' for s in sorted(mc, key=lambda s: MUNI_SLUGS[s][1]))
    ver_opts = "".join(f'<option value="{k}">{esc(vlabel(k)[0])}</option>' for k in "ABCD") + f'<option value="AB">{T("Checked or listed (A + B)","確認済み＋掲載あり（A・B）")}</option>'
    fn = "data_ja.js" if LANG == "ja" else "data.js"
    write("assets/" + fn, "window.DIR=" + json.dumps(data_blob(), ensure_ascii=False, separators=(",", ":")) + ";")
    body = f'''<div class="wrap pagehead" id="find-app"><h1>{T("Search all places","すべての場所を検索")}</h1><p class="sub">{T("Filter by art, area, language and how recently we checked. Japanese or English words both work.","種目・地域・英語対応・確認の新しさで絞り込めます。日本語でも英語でも検索できます。")}</p>
<form class="filters" onsubmit="return false" role="search"><div style="grid-column:1/-1"><label for="f-q">{T("Search","検索")}</label><input id="f-q" type="search" placeholder="{T("Name, instructor, district, style…","名称・指導者・地区・流派…")}" autocomplete="off"></div>
<div><label for="f-art">{T("Art","種目")}</label><select id="f-art"><option value="">{T("Any art","すべて")}</option>{art_opts}</select></div>
<div><label for="f-area">{T("Area","地域")}</label><select id="f-area"><option value="">{T("Anywhere","すべて")}</option>{area_opts}</select></div>
<div><label for="f-ver">{T("Verification","確認状況")}</label><select id="f-ver"><option value="">{T("Any","すべて")}</option>{ver_opts}</select></div>
<div style="display:flex;flex-direction:column;justify-content:end;gap:6px"><label><input type="checkbox" id="f-eng" style="width:auto;min-height:0"> {T("English-friendly only","英語対応のみ")}</label><label><input type="checkbox" id="f-org" style="width:auto;min-height:0"> {T("Include governing bodies","統括団体を含む")}</label></div>
<div style="display:flex;align-items:end;gap:8px"><button type="button" id="f-near" class="btn secondary">{T("📍 Nearest to me","📍 現在地から近い順")}</button><button type="button" id="f-reset" class="btn secondary">{T("Reset","リセット")}</button></div></form>
<div class="results-bar"><b id="f-count" aria-live="polite"></b><span id="f-msg" class="sub" style="margin:0"></span></div><div id="f-out" class="cards"><noscript><p>{T("Search needs JavaScript. You can still browse by art or by area.","検索にはJavaScriptが必要です。種目別・地域別のページからも探せます。")}</p></noscript></div>
<p style="text-align:center"><button type="button" id="f-more" class="btn secondary" hidden>{T("Show more","さらに表示")}</button></p></div>'''
    page("/find/", T("Search martial arts places in Okinawa","沖縄の武道・格闘技を検索"), T("Search dojo, gyms and clubs in Okinawa by name, style, area and language.","名称・流派・地域・言語で、沖縄の道場・ジム・クラブを検索。"), body, cur="find", scripts=f'<script src="{url("/assets/"+fn)}"></script>')

def build_map():
    n = sum(1 for r in ROWS if r["lat"] and r["lon"] and r["status"] != "closed")
    fn = "data_ja.js" if LANG == "ja" else "data.js"
    art_opts = "".join(f'<option value="{d["slug"]}">{esc(dname(d["slug"]))}</option>' for d in DISC.values() if by_disc[d["slug"]])
    empty = "" if n else f'<div class="callout"><b>{T("Map positions are being added.","地図上の位置は順次追加中です。")}</b> {T("Until then, use search or browse by area.","それまでは検索や地域別ページをご利用ください。")}</div>'
    body = f'''<div class="wrap pagehead"><h1>{T("Map","地図")}</h1><p class="sub">{T(f"{n} places with a map position. Pins for 2019-roster dojo are approximate (rounded to about 100 m) to protect private homes.",f"地図上の位置がある場所：{n}件。2019年名簿の道場は、個人宅保護のため約100 mに丸めた概略位置です。")}</p>{empty}
<div class="switcher"><label for="m-art"><b>{T("Art","種目")}</b></label><select id="m-art"><option value="">{T("All arts","すべて")}</option>{art_opts}</select>
<button type="button" id="m-near" class="btn secondary">{T("📍 Near me","📍 現在地")}</button><span id="m-count" class="sub" style="margin:0"></span></div>
<div id="map" role="region" aria-label="{T("Map of listings","掲載地図")}" style="height:min(70vh,640px);border-radius:12px;border:1px solid var(--line)"></div>
<p class="sub" style="font-size:.8rem">{T("Map © OpenStreetMap contributors.","地図 © OpenStreetMap contributors")}</p></div>'''
    leaf_css = '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css">'
    scripts = f'<script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js"></script><script src="{url("/assets/"+fn)}"></script><script src="{url("/assets/map.js")}"></script>'
    page("/map/", T("Map of martial arts places in Okinawa","沖縄の武道・格闘技 地図"), T("See dojo, gyms and clubs on a map of Okinawa and find the nearest to you.","沖縄の道場・ジム・クラブを地図で確認し、近くの場所を探せます。"), body, cur="map", extra_head=leaf_css, scripts=scripts)

# ---------------------------------------------------------------- long-form pages (EN + JA)
def build_start():
    if LANG == "ja":
        ph = [("見学をしたいのですが。","見学を申し込む"),("体験はできますか？","体験の可否を尋ねる"),("初心者ですが、大丈夫ですか？","初心者であることを伝える"),("英語は話せますか？","英語対応を尋ねる"),("月謝と入会金はいくらですか？","料金を尋ねる"),("道着は必要ですか？","服装・用具を尋ねる"),("子供も参加できますか？","子どもの参加を尋ねる"),("次の稽古はいつですか？","次の稽古日を尋ねる")]
        phr = "".join(f'<div class="phrase"><div class="j" lang="ja">{a}</div><div class="e">{b}</div></div>' for a, b in ph)
        body = f'''<div class="wrap pagehead prose"><div class="crumbs"><a href="{url("/")}">ホーム</a> › 初めての方へ</div><h1>沖縄で武道を始める（続ける）ために</h1>
<p class="sub">観光客・新しく住み始めた方・再開したい方のための実用ガイドです。</p>
<h2>1. 種目を選ぶ</h2><p>空手発祥の地・沖縄には<a href="{url("/arts/karate/")}">空手</a>・<a href="{url("/arts/kobudo/")}">古武道</a>が数多くありますが、<a href="{url("/arts/bjj/")}">BJJ</a>・<a href="{url("/arts/boxing/")}">ボクシング</a>・<a href="{url("/arts/kickboxing/")}">ムエタイ</a>・<a href="{url("/arts/mma/")}">MMA</a>・<a href="{url("/arts/judo/")}">柔道</a>・<a href="{url("/arts/kendo/")}">剣道</a>・<a href="{url("/arts/aikido/")}">合気道</a>なども楽しめます。民間ジム（BJJ・キック・MMA）は入りやすく、伝統的な空手道場は小規模で紹介制のことも多く、ゆっくり関係を築く姿勢が大切です。</p>
<h2>2. 場所を選ぶ</h2><p><a href="{url("/areas/")}">地域別ページ</a>や<a href="{url("/map/")}">地図</a>を使い、英語で案内してほしい場合は<a href="{url("/find/?eng=1")}">英語対応あり</a>で絞り込めます。確認バッジも見てください。緑の「確認済み」は最近確認した情報、灰色の「2019年名簿」は、まず電話で確認をおすすめするという意味です。</p>
<h2>3. 連絡する</h2><ol class="steps"><li><b>電話・LINE・インスタグラム。</b>沖縄の道場は、メールより電話やDMのほうが返事が早いことがよくあります。夜の時間帯がおすすめです。</li>
<li><b>まず見学（けんがく）を。</b>見学は普通のことで、失礼ではありません。指導の雰囲気や年齢層を確認できます。</li>
<li><b>体験（たいけん）の可否を尋ねる。</b>無料や割引の体験を設けるジムは多く、伝統道場は次の稽古にそのまま参加を勧められることもあります。</li>
<li><b>実用面の確認：</b>月謝・入会金・服装・スポーツ保険・英語での指導の有無。</li></ol>
<h2>問い合わせで使う表現</h2><div>{phr}</div>
<h2>礼儀作法の基本</h2><ul><li>10〜15分前に到着し、道場の出入りでは一礼し、周りに合わせます。</li><li>指導者は「先生」と呼び、立つ位置は指示に従います。</li><li>道場では素足（または指定の履物）。爪は短く、道着は清潔に。</li><li>写真・動画は事前に許可を得ます（先生の許可があるときのみ可とする道場もあります）。</li><li>タトゥー：民間ジムや公共施設で扱いが異なります。事前に確認を。</li></ul>
<h2>米軍関係の方・観光客の方へ</h2><p>短期滞在の方は、ドロップインや無料体験週間を案内しているジムが便利です。基地内の<a href="{url("/l/mccs-martial-arts/")}">MCCS武道プログラム</a>は基地への入場許可が必要です。</p>
<h2>お子さん・ご家族へ</h2><p>剣道・柔道・空手・極真・相撲は少年向けの活動が盛んで、夜間や週末に学校の体育館で開かれることが多いです。見学できるかを尋ねましょう。</p>
<div class="callout info">掲載されていない良い道場をご存じですか？<a href="{url("/suggest-edit/")}">教えてください</a>。</div></div>'''
        page("/start/", "初めての方へ — 沖縄で武道を始めるガイド", "道場・ジムの探し方、連絡の仕方、礼儀作法、聞くべきこと。", body, cur="start"); return
    ph = [("見学をしたいのですが。","Kengaku o shitai no desu ga.","I'd like to come and watch a class."),
          ("体験はできますか？","Taiken wa dekimasu ka?","Can I try a class?"),
          ("初心者ですが、大丈夫ですか？","Shoshinsha desu ga, daijōbu desu ka?","I'm a beginner — is that okay?"),
          ("英語は話せますか？","Eigo wa hanasemasu ka?","Do you speak English?"),
          ("料金はいくらですか？","Ryōkin wa ikura desu ka?","How much does it cost?"),
          ("道着は必要ですか？","Dōgi wa hitsuyō desu ka?","Do I need a uniform?"),
          ("子供も参加できますか？","Kodomo mo sanka dekimasu ka?","Can my child join?"),
          ("次の稽古はいつですか？","Tsugi no keiko wa itsu desu ka?","When is the next class?")]
    phr = "".join(f'<div class="phrase"><div class="j" lang="ja">{a}</div><div class="r">{b}</div><div class="e">{c}</div></div>' for a, b, c in ph)
    body = f'''<div class="wrap pagehead prose"><div class="crumbs"><a href="{url("/")}">Home</a> › New to training?</div><h1>Starting (or continuing) training in Okinawa</h1>
<p class="sub">A practical guide for visitors, new residents and returning students.</p>
<h2>1. Pick what you want</h2><p>Okinawa is the birthplace of karate, so <a href="{url("/arts/karate/")}">karate</a> and <a href="{url("/arts/kobudo/")}">kobudo</a> are everywhere — but you will also find <a href="{url("/arts/bjj/")}">BJJ</a>, <a href="{url("/arts/boxing/")}">boxing</a>, <a href="{url("/arts/kickboxing/")}">Muay Thai</a>, <a href="{url("/arts/mma/")}">MMA</a>, <a href="{url("/arts/judo/")}">judo</a>, <a href="{url("/arts/kendo/")}">kendo</a>, <a href="{url("/arts/aikido/")}">aikido</a> and more. Commercial gyms (BJJ, kickboxing, MMA) are usually easiest to join. Traditional karate dojo are often small, introduced by word of mouth, and reward patience.</p>
<h2>2. Choose where</h2><p>Use <a href="{url("/areas/")}">the area map</a> or <a href="{url("/map/")}">the map</a> and filter by <a href="{url("/find/?eng=1")}">English-friendly</a> if you don't speak Japanese. Check the verification badge — a green “Checked” label means we confirmed details recently; a grey “2019 roster” label means call first.</p>
<h2>3. Make contact</h2><ol class="steps"><li><b>Phone, LINE or Instagram.</b> Many Okinawan dojo answer a phone call or a direct message more reliably than email. Evenings are best.</li>
<li><b>Ask to observe first (見学).</b> It's normal and polite. You'll see the teaching style, the age mix and whether it suits you.</li>
<li><b>Ask about a trial (体験).</b> Many gyms offer a free or discounted first class or week. Traditional dojo may simply invite you to join the next session.</li>
<li><b>Ask the practical questions:</b> fees (月謝 monthly fee, 入会金 joining fee), what to wear, insurance (スポーツ保険), whether classes are in English.</li></ol>
<h2>Useful phrases</h2><div>{phr}</div><p class="sub">Romanization is simplified. A native speaker (a friend, hotel staff, or a translation app) can help you check a message before you send it.</p>
<h2>Etiquette basics</h2><ul><li>Arrive 10–15 minutes early. Bow when entering and leaving the training space (一礼, <i>ichirei</i>) and follow what others do.</li><li>Call the teacher <i>sensei</i>. Wait to be told where to stand.</li><li>Shoes off in the dojo; keep nails short and uniform clean.</li><li>Ask before taking photos or video — some dojo allow photos only with the sensei's permission.</li><li>Tattoos: private gyms and public facilities vary. Ask in advance.</li></ul>
<h2>Visitors and military families</h2><p>Short-stay visitors: choose gyms that advertise drop-in rates or a free trial week. The US-military community has a large <a href="{url("/l/mccs-martial-arts/")}">MCCS martial arts program</a> on base, and several off-base BJJ and kickboxing gyms are used to English speakers. On-base classes need installation access; check each listing.</p>
<h2>Kids and families</h2><p>Kendo, judo, karate, Kyokushin and sumo clubs run strong youth programmes — often in school gyms in the evening or at weekends. Look for “youth” classes on the listing and ask whether parents can watch.</p>
<h2>Things that surprise newcomers</h2><ul><li>Class times are often listed as images or on social media; confirm by message.</li><li>Many traditional dojo have no website and no fixed monthly fee system — ask the sensei.</li><li>Schedules shift around school and public holidays (Obon, New Year, Golden Week).</li></ul>
<div class="callout info">Found a great beginner-friendly place that isn't listed? <a href="{url("/suggest-edit/")}">Tell us</a>.</div></div>'''
    page("/start/", "New to martial arts in Okinawa? A beginner's guide", "How to find, contact and join a dojo or gym in Okinawa — phrases in Japanese, etiquette and what to ask.", body, cur="start")

def build_about():
    vc = Counter(r["verification"] for r in ROWS if not r["is_org"]); tot = sum(vc.values())
    rowsv = "".join(f'<tr><td>{badge(k)}</td><td>{esc(vlabel(k)[1])}</td><td>{vc[k]}</td></tr>' for k in "ABCD")
    pstat = Counter(r["status"] for r in ROWS)
    nmap = sum(1 for r in ROWS if r["lat"])
    if LANG == "ja":
        body = f'''<div class="wrap pagehead prose"><div class="crumbs"><a href="{url("/")}">ホーム</a> › データについて</div><h1>データについて</h1>
<p class="sub">何が載っているか、どう集めたか、どれくらい確かか、どう最新に保つか。</p>
<div class="callout"><b>最初にお読みください。</b>これは最善を尽くした案内であり、公式の登録簿ではありません。{tot}か所のうち{vc["C"]}か所は2019年の県内道場名簿に基づき、再確認していません。{vc["A"]}か所は2026年10月に最新の公式ページで確認しました。お出かけ前に必ず電話かメッセージで確認してください。</div>
<h2>確認ラベル</h2><table class="data"><thead><tr><th>ラベル</th><th>意味</th><th>件数</th></tr></thead><tbody>{rowsv}</tbody></table>
<h2>私たちが行っていること</h2><ol class="steps"><li><b>収集。</b>公式名簿・連盟の一覧から始め、運営者の公式サイト、ディレクトリ（手がかりとしてのみ）、利用者からの情報で追加します。</li>
<li><b>確認。</b>運営者または連盟の最新ページと照合し、可能なら電話等で確認し、日付を記録します。</li>
<li><b>表示。</b>すべての掲載に確認レベルと最終確認日を表示します。未確認の情報を黙って格上げすることはありません。</li>
<li><b>定期的な再確認。</b>毎月、再確認期限（確認済み6か月、その他12か月、情報のみ3か月）を過ぎた掲載とリンク切れの一覧を自動作成します。</li>
<li><b>迅速な修正。</b>訪問者・運営者からの報告は公開の一覧に入ります。閉鎖した場所は「閉鎖」として1年間保持します。</li></ol>
<h2>件数の意味</h2><p>件数は「掲載している数」で、全数調査ではありません。「稽古場所」には統括団体を含みません。複数の種目を教える場所は、種目ごとに数えるため、種目別の合計は場所の総数より多くなります。</p>
<h2>名称・翻訳・住所</h2><ul><li>日本語は公表されているとおりに表示します。名簿の空手道場の英語名は、指導者の姓＋流派による説明的な名称で、道場名の読みを推測してはいません。</li><li>指導者名の英字表記は名簿のふりがなに基づく概略です。</li><li>名簿の私的な道場の住所は番地レベルで表示し、建物名・部屋番号は除いています。</li><li>地図の座標（{nmap}件）は公的な住所検索（国土地理院）で付与し、名簿のみの道場は約100 mに丸めています。Googleマップは埋め込まず、リンクのみです。</li></ul>
<h2>既知の不足</h2><ul><li>合気道は一覧に基づく情報で、個別の再確認はしていません。多くの伝統空手道場は電話・時間・ウェブサイトが公開されていません。</li><li>公式ページの稽古時間が画像の場合、自動では読み取れていません。</li><li>自動アクセスを禁じているジムのサイトは確認できていないため、他の情報源に基づき、その旨を表示しています。</li></ul>
<h2>データの再利用</h2><p>全データは<a href="{url("/data/locations.csv")}">locations.csv</a>で公開しています（{esc(CFG["data_license"])}）。出典としてこのサイトを明記し、「最終確認」列を保持してください。</p>
<h2>運営について</h2><p>有志による運営です。<a href="{url("/suggest-edit/")}">修正の提案</a>・<a href="{url("/for-dojos/")}">運営者の方へ</a>をご覧ください。</p></div>'''
        page("/about-data/", "データについて — 方法と確認", "沖縄の武道・格闘技ディレクトリの作成・確認・更新の方法。", body, cur="about"); return
    body = f'''<div class="wrap pagehead prose"><div class="crumbs"><a href="{url("/")}">Home</a> › About this data</div><h1>About this data</h1>
<p class="sub">What is here, how it was gathered, how confident we are, and how it stays current.</p>
<div class="callout"><b>Read this first.</b> This is a best-effort directory, not an official register. {vc["C"]} of {tot} places come from a 2019 prefectural roster and have not been re-checked; {vc["A"]} were checked against a current official page in October 2026. Always confirm by phone or message before travelling.</div>
<h2>How we rate every listing</h2><table class="data"><thead><tr><th>Label</th><th>Meaning</th><th>Places now</th></tr></thead><tbody>{rowsv}</tbody></table>
<h2>What we do</h2><ol class="steps"><li><b>Collect.</b> Start from official rosters and federation lists, then add gyms and clubs found through operators' own websites, directories (as leads only) and community reports.</li>
<li><b>Verify.</b> Compare each listing with the operator's or federation's own current page. Where possible, confirm with a call or message. Record the date.</li>
<li><b>Label.</b> Every listing shows its verification level and last-checked date. Unconfirmed items are labelled, never silently promoted.</li>
<li><b>Re-check on a schedule.</b> A monthly automated report lists entries older than their re-check window (checked: 6 months; others: 12 months; leads: 3 months) and dead website links.</li>
<li><b>Fix quickly.</b> Reports from visitors and owners go into a public queue. Closed places are marked closed and kept for a year so people searching old names find the answer.</li></ol>
<h2>Counts and what they mean</h2><p>The counts on the home, art and area pages are numbers of <em>listed</em> places, not a census. An art or area with few listings may simply be under-researched. “Places” excludes governing bodies; a place that teaches several arts is counted under each, so art totals add up to more than the number of places.</p>
<h2>Names, translations, addresses and map positions</h2><ul><li>Japanese is shown as published. English names for karate dojo from the roster are descriptive (instructor surname + style); we do not guess at readings of dojo names.</li><li>Instructor names are romanised from the roster's furigana (kana readings); treat spellings as approximate.</li><li>Addresses for private dojo from the roster are shown at block level; apartment names and room numbers are removed.</li><li>Map positions ({nmap} places so far) come from the Japanese government's public address-search service (GSI); roster-only dojo are rounded to about 100 m. We link out to Google Maps rather than embedding it.</li></ul>
<h2>Known gaps</h2><ul><li>Aikido and Shorinji Kempo come from federation directories, not individually re-checked; most traditional karate dojo have no published phone, hours or website.</li><li>Class times on several official pages are images and could not be read automatically.</li><li>Some gym websites forbid automated access; those gyms are listed from other sources and labelled accordingly.</li></ul>
<h2>Data you can reuse</h2><p>The full list is in <a href="{url("/data/locations.csv")}">locations.csv</a> ({esc(CFG["data_license"])}). Please credit this site and keep the “last verified” column.</p>
<h2>Who maintains this</h2><p>This is a volunteer project. See <a href="{url("/suggest-edit/")}">Suggest an edit</a> or <a href="{url("/for-dojos/")}">For dojo owners</a>. Status of all rows: {", ".join(f"{STATUS.get(k,k)} {v}" for k, v in pstat.most_common())}.</p></div>'''
    page("/about-data/", "About this data — methodology and verification", "How the Okinawa martial arts directory is compiled, verified and kept up to date.", body, cur="about")

def build_sources():
    rows = []
    for s in SRC.values():
        link = f'<a href="{esc(s["url"])}" rel="noopener nofollow">{esc(s["url"])}</a>' if s["url"] else "—"
        rows.append(f'<tr id="{esc(s["id"])}"><td><b>{esc(s["title"])}</b><br>{link}</td><td>{esc(s["type"])}</td><td>{esc(s["how_used"])}</td><td>{esc(s["policy"])}</td></tr>')
    if LANG == "ja":
        body = f'''<div class="wrap pagehead"><div class="crumbs"><a href="{url("/")}">ホーム</a> › 情報源</div><h1>情報源と帰属</h1>
<div class="prose"><p class="sub">情報の出どころと、他者の掲載情報の扱い方。</p>
<h2>方針</h2><ul><li><b>内容ではなく事実のみ。</b>名称・住所・電話番号・稽古時間といった事実を記録し、運営者へリンクします。説明文・写真・評価・口コミ・ページ構成は複製しません。</li>
<li><b>ディレクトリは「手がかり」。</b>民間ディレクトリ（THE GYMS 沖縄など）は、ジムの存在を知るためにだけ使い、運営者の公式サイトや電話で確認します。確認できないものはその旨を表示します。</li>
<li><b>robots.txtと利用規約を尊重。</b>自動アクセスを禁じるサイトは取得していません。</li>
<li><b>地図。</b>地図サービスのデータは複製・埋め込みをしません。「Googleマップで開く」はお使いのアプリで検索を開くだけです。座標は国土地理院の公開住所検索を使い、地図表示はOpenStreetMapです。</li>
<li><b>削除。</b>運営者はいつでも修正・削除を依頼できます（<a href="{url("/for-dojos/")}">運営者の方へ</a>）。</li></ul></div>
<h2>使用した情報源</h2><div style="overflow-x:auto"><table class="data"><thead><tr><th>情報源</th><th>種類</th><th>用途</th><th>扱い</th></tr></thead><tbody>{"".join(rows)}</tbody></table></div></div>'''
        page("/sources/", "情報源と帰属", "沖縄の武道・格闘技ディレクトリの情報源と他者の掲載情報の扱い。", body, cur="about"); return
    body = f'''<div class="wrap pagehead"><div class="crumbs"><a href="{url("/")}">Home</a> › Sources</div><h1>Sources &amp; attribution</h1>
<div class="prose"><p class="sub">Where the information comes from, and how we treat other people's listings.</p>
<h2>Our policy</h2><ul><li><b>Facts, not content.</b> We record facts (a name, an address, a phone number, a class time) and link to the operator. We do not copy descriptions, photographs, ratings, reviews or page layouts.</li>
<li><b>Directories are leads, not sources of record.</b> Commercial directories (for example THE GYMS Okinawa and similar) are used only to discover that a gym exists. We then check it against the operator's own site or a call, and label it if we couldn't.</li>
<li><b>We respect robots.txt and site terms.</b> Sites that disallow automated access were not scraped; those gyms are listed from other sources and labelled accordingly.</li>
<li><b>Maps.</b> No map-service data is copied or embedded. The “Open in Google Maps” links simply open a search in your own map app. Coordinates come from the Geospatial Information Authority of Japan's public address search; the map tiles are © OpenStreetMap contributors.</li>
<li><b>Removal.</b> Owners can ask for correction or removal at any time — see <a href="{url("/for-dojos/")}">For dojo owners</a>.</li></ul></div>
<h2>Sources used</h2><div style="overflow-x:auto"><table class="data"><thead><tr><th>Source</th><th>Type</th><th>Used for</th><th>Policy</th></tr></thead><tbody>{"".join(rows)}</tbody></table></div></div>'''
    page("/sources/", "Sources & attribution", "Where the Okinawa martial arts directory's information comes from and how other listings are treated.", body, cur="about")

def build_suggest():
    repo = CFG["github_repo"]
    def iu(t): return f"https://github.com/{repo}/issues/new?template={t}" if CFG.get("use_github", True) else f"mailto:{CFG['contact_email']}?subject=" + urllib.parse.quote("Add a place")
    if LANG == "ja":
        body = f'''<div class="wrap pagehead prose"><div class="crumbs"><a href="{url("/")}">ホーム</a> › 修正・追加の提案</div><h1>修正・追加の提案</h1>
<p class="sub">運営者でなくても構いません。番号がつながらない、移転した、掲載にない場所をご存じ——そんなときはお知らせください。</p>
<div class="cards"><div class="card"><h3>誤りを報告</h3><p>各掲載ページの「誤りを報告」ボタンから、掲載内容があらかじめ入力された状態で送れます。まず<a href="{url("/find/")}">掲載を探して</a>ください。</p></div>
<div class="card"><h3>未掲載の場所を追加</h3><p>名称・地域・連絡先・情報の出どころを教えてください。ウェブサイトやSNSのリンクがあれば最適です。</p><p><a class="btn" href="{esc(iu("add-listing.yml"))}" rel="noopener">場所を追加</a></p></div>
<div class="card"><h3>メールで送る</h3><p><a href="mailto:{esc(CFG["contact_email"])}">{esc(CFG["contact_email"])}</a> に、掲載名と修正内容をお送りください。代わりに入力します。</p></div></div>
<h2>特に助かる情報</h2><ul><li>最後に訪問・電話した日付。</li><li>現在つながる電話番号やSNS。</li><li>英語対応・見学可否。</li></ul></div>'''
        page("/suggest-edit/", "修正・追加の提案", "沖縄の武道・格闘技ディレクトリへの修正報告・追加の提案。", body); return
    body = f'''<div class="wrap pagehead prose"><div class="crumbs"><a href="{url("/")}">Home</a> › Suggest an edit</div><h1>Suggest an edit</h1>
<p class="sub">You don't need to be an owner. If a number is dead, a dojo has moved, or you know a place we've missed, tell us.</p>
<div class="cards"><div class="card"><h3>Report incorrect info</h3><p>Every listing has a “Report a problem” button that pre-fills the listing. Or <a href="{url("/find/")}">find the listing</a> first.</p></div>
<div class="card"><h3>Add a missing place</h3><p>Name, area, how to reach them, and how you know. A website or social link is perfect.</p><p><a class="btn" href="{esc(iu("add-listing.yml"))}" rel="noopener">Add a place</a></p></div>
<div class="card"><h3>Prefer email?</h3><p>Email <a href="mailto:{esc(CFG["contact_email"])}">{esc(CFG["contact_email"])}</a> with the listing name and what to change.</p></div></div>
<h2>What helps most</h2><ul><li>The date you last visited or called.</li><li>A phone number or social page that is currently working.</li><li>Whether English is spoken and visitors are welcome.</li></ul>
<p>We review reports and update the data regularly. See <a href="{url("/about-data/")}">About this data</a>.</p></div>'''
    page("/suggest-edit/", "Suggest an edit or add a place", "Report incorrect information or add a missing martial arts place in Okinawa.", body)

def build_dojos():
    repo = CFG["github_repo"]
    OWNER_LINK = f"https://github.com/{repo}/issues/new?template=owner-update.yml" if CFG.get("use_github", True) else f"mailto:{CFG['contact_email']}?subject=" + urllib.parse.quote("Owner update")
    if LANG == "ja":
        body = f'''<div class="wrap pagehead prose"><div class="crumbs"><a href="{url("/")}">ホーム</a> › 運営者の方へ</div><h1>道場・ジムの運営者の方へ</h1>
<p class="sub">掲載内容の修正・追加・削除は、いつでもお申し込みいただけます。掲載は無料です。</p>
<h2>掲載の更新・確認</h2><p>掲載ページの「誤りを報告」から「運営者です」を選び、変更内容と、ご本人であることの確認方法（公式サイトやSNSで十分です）をお知らせください。電話番号・営業時間・体験の可否・英語対応の有無を教えていただけると、利用者の助けになります。</p>
<p><a class="btn" href="{OWNER_LINK}" rel="noopener">運営者用フォーム</a> <a class="btn secondary" href="mailto:{esc(CFG["contact_email"])}">メールで連絡</a></p>
<h2>掲載・個人情報の削除</h2><p>2019年の名簿に基づく指導者名や住所は県が公表した情報ですが、ご希望があれば、速やかに削除または縮小します。理由は不要です。上記フォームまたはメールでご連絡ください。</p>
<h2>表示している内容</h2><p>名称・流派・地域・住所・電話・ウェブサイト／SNS・稽古日時・連絡先担当者・見学や英語対応の可否。会員名簿や生徒の写真は掲載しません。</p></div>'''
        page("/for-dojos/", "道場・ジムの運営者の方へ — 掲載の更新・削除", "運営者が掲載を修正・確認・削除する方法。", body); return
    body = f'''<div class="wrap pagehead prose"><div class="crumbs"><a href="{url("/")}">Home</a> › For dojo &amp; gym owners</div><h1>For dojo &amp; gym owners</h1>
<p class="sub">道場・ジムの運営者の方へ — You can correct, complete or remove your listing at any time.</p>
<h2>Update or claim your listing</h2><p>Find your listing, press “Report a problem”, and choose “I run this place”. Give us the changes and a way to confirm it's you (your official website or social page is enough). We don't charge for listings.</p>
<p><a class="btn" href="{OWNER_LINK}" rel="noopener">Owner update form</a> <a class="btn secondary" href="mailto:{esc(CFG["contact_email"])}">Email us</a></p>
<h2>Remove your listing or your personal details</h2><p>Instructor names and addresses from the 2019 roster were published by the prefecture, but you can ask us to remove or trim them at any time. We will do so promptly. Use the owner form or email — no reason needed.</p>
<h2>日本語でのご連絡</h2><p lang="ja">掲載内容の修正・追加・削除のご希望は、上記のメールまたはフォームからご連絡ください。電話番号・営業時間・体験の可否・英語対応の有無をお知らせいただけると、利用者の役に立ちます。掲載の削除も、理由なくお受けします。</p>
<h2>What we show</h2><p>Name, style, area, address, phone, website/social, hours, contact person, and whether visitors/English are welcome. We never show member lists or photos of students.</p></div>'''
    page("/for-dojos/", "For dojo & gym owners — update or remove your listing", "How owners can correct, claim or remove a listing in the Okinawa martial arts directory.", body)

def build_privacy():
    an_en = "This site uses privacy-friendly, cookie-free analytics (page views only, no personal profiles)." if ANALYTICS else "This site has no accounts, no ads and sets no tracking cookies."
    an_ja = "このサイトはCookieを使わないプライバシー配慮型のアクセス解析（ページ閲覧数のみ・個人の特定なし）を使用しています。" if ANALYTICS else "このサイトにはアカウント・広告・追跡用Cookieはありません。"
    if LANG == "ja":
        body = f'''<div class="wrap pagehead prose"><div class="crumbs"><a href="{url("/")}">ホーム</a> › プライバシー</div><h1>プライバシーと削除依頼</h1>
<ul><li>{an_ja}</li><li>「現在地から近い順」「現在地」は、お使いのブラウザ内でのみ位置を使います。位置情報は当サイトのサーバーに送信・保存されません。</li><li>掲載には、公開名簿や運営者のサイトで公表されている事業情報と指導者名が含まれます。</li><li>私的な道場の住所は番地レベルに縮小し、建物名・部屋番号は除いています。名簿のみの道場のページは検索エンジンに表示されません。地図の位置も約100 mに丸めています。</li><li>掲載された方は、いつでも修正・削除を依頼できます（<a href="{url("/for-dojos/")}">運営者の方へ</a>）。</li><li>「誤りを報告」を押すとGitHub（またはメールアプリ）に移動し、そちらのプライバシーポリシーが適用されます。地図はOpenStreetMapのタイルを読み込みます。</li></ul></div>'''
        page("/privacy/", "プライバシーと削除依頼", "個人情報の扱いと削除依頼の方法。", body); return
    body = f'''<div class="wrap pagehead prose"><div class="crumbs"><a href="{url("/")}">Home</a> › Privacy</div><h1>Privacy &amp; removal</h1>
<ul><li>{an_en}</li><li>“Nearest to me” and “Near me” use your location only inside your browser; it is never sent to or stored on our servers.</li><li>Listings contain business details and the names of instructors as published in public rosters or on operators' sites.</li><li>For private dojo, addresses are trimmed to block level (no apartment names or room numbers), pages for roster-only dojo are hidden from search engines, and map pins are rounded to about 100 m.</li><li>Anyone named on this site can ask for correction or removal at any time — see <a href="{url("/for-dojos/")}">For dojo owners</a>.</li><li>When you press “Report a problem”, you leave this site for GitHub (or open your email app) and its own privacy policy applies. The map page loads tiles from OpenStreetMap.</li></ul></div>'''
    page("/privacy/", "Privacy & removal requests", "How personal information is handled and how to request removal.", body)

def build_404():
    write("404.html", f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Page not found</title><link rel="stylesheet" href="{url("/assets/style.css")}"></head><body><main class="wrap pagehead"><h1>Page not found / ページが見つかりません</h1><p>Try <a href="{url("/find/")}">searching</a> or go <a href="{url("/")}">home</a>. · <a href="{BASE}/ja/">日本語トップへ</a></p></main></body></html>''')

def build_static():
    shutil.copytree(ROOT/"templates/assets", DIST/"assets", dirs_exist_ok=True)
    (DIST/"data").mkdir(exist_ok=True)
    shutil.copy(ROOT/"data/locations.csv", DIST/"data/locations.csv")
    (DIST/".nojekyll").write_text("")

ARTS_WITH = [d for d in DISC if n_places(d)]

def sitemap():
    pages = ["/", "/arts/", "/areas/", "/find/", "/map/", "/start/", "/about-data/", "/sources/", "/suggest-edit/", "/for-dojos/", "/privacy/"]
    pages += [f"/arts/{d}/" for d in DISC if by_disc[d]] + [f"/areas/{s}/" for s in {r["municipality"] for r in ROWS if r["municipality"]}]
    pages += [f'/l/{r["id"]}/' for r in ROWS if not (r["verification"] == "C" and not CFG["index_roster_pages"])]
    allp = sorted(pages) + sorted("/ja" + p for p in pages)
    sm = "".join(f'<url><loc>{CFG["base_url"]}{p}</loc><lastmod>{TODAY}</lastmod></url>' for p in allp)
    write("sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{sm}</urlset>')
    write("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {CFG['base_url']}/sitemap.xml\n")

def build_language():
    build_home(); build_arts_index(); build_areas(); build_find(); build_map(); build_start(); build_about(); build_sources(); build_suggest(); build_dojos(); build_privacy()
    for d in DISC.values():
        if by_disc[d["slug"]]: build_art(d)
    for s in {r["municipality"] for r in ROWS if r["municipality"]}: build_area(s)
    for r in ROWS: build_listing(r)

def main():
    global LANG
    if DIST.exists(): shutil.rmtree(DIST)
    DIST.mkdir()
    build_static(); build_404(); sitemap()
    for LANG in ("en", "ja"):
        build_language()
    print("pages:", sum(1 for _ in DIST.rglob("index.html")), "places:", len(PLACES), "arts:", len(ARTS_WITH))

if __name__ == "__main__":
    main()
