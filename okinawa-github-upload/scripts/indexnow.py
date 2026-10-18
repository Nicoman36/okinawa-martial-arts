"""Tell IndexNow (Bing, Yandex, Naver, ...) about recently changed pages. Run after deploy; never fails the build."""
import datetime, json, re, sys, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CFG = json.loads((ROOT / "config.json").read_text(encoding="utf-8"))
BASE = CFG["base_url"].rstrip("/")
KEY = CFG.get("indexnow_key", "")
DAYS = 3

def main():
    if not KEY:
        print("no indexnow_key; skipping"); return
    xml = urllib.request.urlopen(BASE + "/sitemap.xml", timeout=30).read().decode("utf-8")
    cutoff = (datetime.date.today() - datetime.timedelta(days=DAYS)).isoformat()
    urls = []
    for loc, rest in re.findall(r"<url><loc>([^<]+)</loc>(.*?)</url>", xml):
        m = re.search(r"<lastmod>([^<]+)</lastmod>", rest)
        if m and m.group(1) >= cutoff: urls.append(loc)
    urls = urls[:9000]
    if not urls:
        print("nothing recent to submit"); return
    body = json.dumps({"host": BASE.split("//", 1)[1], "key": KEY, "keyLocation": f"{BASE}/{KEY}.txt", "urlList": urls}).encode()
    req = urllib.request.Request("https://api.indexnow.org/indexnow", data=body, headers={"Content-Type": "application/json; charset=utf-8"})
    try:
        r = urllib.request.urlopen(req, timeout=30)
        print("IndexNow accepted", len(urls), "urls, HTTP", r.status)
    except Exception as e:
        print("IndexNow failed:", e)

if __name__ == "__main__":
    try: main()
    except Exception as e: print("IndexNow skipped:", e)
