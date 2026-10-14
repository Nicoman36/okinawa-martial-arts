# Verification & update workflow

Dojo close, move and change numbers. This is the routine that keeps the directory honest.

## Who owns it
**Data steward:** _(name one person — and a backup)_. They triage reports weekly and run the monthly queue. Everyone else can suggest edits; only the steward (or a trusted editor) merges them.

## Verification levels (column `verification`)
| Level | Meaning | Re-check every |
|---|---|---|
| A | Confirmed against the operator's/federation's own current page (or by phone) | 6 months |
| B | Found on a third-party listing or older page; not independently confirmed | 12 months (aim to upgrade to A) |
| C | From the 2019 prefectural roster; not re-checked | 12 months (upgrade as you go) |
| D | A lead: exists, but where/whether operating is unconfirmed | 3 months |

`status`: `active`, `unverified`, `needs_check`, `closed`, `moved`. Always set `last_verified` (YYYY-MM-DD) when you confirm something.

## Inbound reports (suggest-an-edit)
1. Each listing page links to a pre-filled GitHub issue form (and a mailto fallback). Owners use `owner-update.yml`.
2. **Triage within 7 days.** Label `data`. Reply to the reporter either way.
3. **Confirm before changing** unless the reporter is clearly the owner: check the operator's site/social or call. Owner requests for *removal or personal-detail removal* are done immediately, no questions.
4. Edit `data/locations.csv`, set `last_verified`, add the source id, open a PR (CI runs `validate_data.py`), merge → the site redeploys.

## Monthly queue (automated)
On the 1st of each month `.github/workflows/verification-queue.yml` runs `stale_report.py` (entries past their window + `needs_check`) and `check_links.py` (dead websites), and opens an issue titled "Verification queue — YYYY-MM". Work it top-down; budget 1–2 hours.

## Closing a place
Set `status` to `closed` (hidden from counts and search; page removed) or `moved` with the new place in `notes`. Keep the row for 12 months so old links and searches resolve, then archive it.

## Upgrading the roster rows (level C)
Priority order: dojo with a website/phone known → dojo in tourist-heavy areas (Naha, Chatan, Okinawa City) → the rest. A 2-minute web/Instagram check usually promotes a row to B; a call or visit to A. Do 10 a month and the roster is cleared in under three years — or ask the associations (沖縄伝統空手道振興会, 沖縄空手会館) for a current roster.

## Every release
`python3 scripts/validate_data.py && python3 scripts/build_site.py` — then spot-check three listings and the home counts.
