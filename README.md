# Okinawa Martial Arts Directory

Static, no-framework, no-database directory site. Python 3 standard library only.

```
data/locations.csv   ← the source of truth (edit this)
data/sources.csv     ← where facts come from (shown on /sources/)
config.json          ← site name, repo, email, base path  ← EDIT BEFORE PUBLISHING
scripts/             build_data.py (rebuild CSV from roster+curated), build_site.py, validate_data.py, stale_report.py, check_links.py
templates/assets/    CSS + JS
.github/             issue forms + deploy + monthly verification-queue workflows
VERIFICATION.md      the update/re-check routine
DATA_REVIEW.md       what was found wrong in the earlier data and what is still open
```

## Run it
```
python3 scripts/validate_data.py
python3 scripts/build_site.py          # → dist/
BASE_PATH="" DIST_DIR=/tmp/site python3 scripts/build_site.py && cd /tmp/site && python3 -m http.server   # local preview
```
`build_data.py` regenerates `locations.csv` from the raw roster and `curated.py`. **Once you start editing the CSV by hand, stop running it** (it would overwrite your edits) — the CSV is then the master.

## Publish (GitHub Pages)
1. Create the repo, push, set Settings → Pages → Source: GitHub Actions.
2. Edit `config.json` (`github_repo`, `contact_email`, `base_url`, `base_path`; use `""` for a custom domain) and the email in `.github/ISSUE_TEMPLATE/config.yml`.
3. Push to `main` — `deploy.yml` validates, builds and publishes.

## Decisions only you can make
1. Site name & domain. 2. Who is the data steward (see VERIFICATION.md). 3. Public contact email. 4. Data licence (default CC BY 4.0 for the compilation). 5. Whether to index roster-only pages (`index_roster_pages`, default off). 6. Whether to add analytics (privacy page says none today).

## Map, near-me, analytics, Japanese
- **Coordinates:** `python3 scripts/geocode.py` (free GSI address search, needs internet, ~8 min) or run the "Geocode addresses" GitHub Action — it opens a PR. Spot-check ~10 pins on /map/. Until coordinates exist the map shows a notice and "nearest to me" has nothing to rank.
- **Analytics:** paste a cookie-free tracker `<script>` tag into `config.json → analytics_snippet`. The privacy page updates itself.
- **Japanese site:** every page is generated twice (`/` and `/ja/`) with hreflang links. UI text, art descriptions and guides are translated; per-listing notes/hours/visitor text stay in the original (mostly English). **Have a native speaker review `scripts/catalog.py` (DISC_JA etc.) and the `LANG == "ja"` blocks in `scripts/build_site.py` before launch.**

## No GitHub needed
`config.json → use_github: false` (the default now) makes every report/suggest link an email link, and the built `dist/` folder is plain files you can drop on any static host (Cloudflare Pages / Netlify drop). Set `use_github: true` later if you want public issue tracking.
