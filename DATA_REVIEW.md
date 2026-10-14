# Data review log — October 2026

Starting point: the earlier workbook (407 rows). Result: `data/locations.csv` (453 rows: 443 places to train + 10 governing bodies).

## What was wrong and is now fixed
- **Karate roster re-parsed from scratch.** The earlier merge swallowed ~30 dojo into neighbouring records and split instructor names across fields. The 2019 roster now parses to **309 dojo** (was 279) with no duplicated dojo+address pairs; 11 multi-line association names and 2 records were hand-corrected against the raw text.
- **Romanisation.** The earlier workbook used machine romanisation of Japanese names; much of it was wrong. Instructor names are now romanised from the roster's own furigana; dojo names are descriptive English ("Higa Dojo — Goju-ryu"), not guessed readings.
- **Merged duplicates:** Boxing Club Nakazato = Boxing Club Okinawa (same address and phone); Paraestra Okinawa = THE BLACKBELT JAPAN Naha; Capoeira Academy Okinawa → Moriniere Martial Arts (probable successor, flagged); Nagahama dojo (Uechi-ryu / "Seizan") = the roster's 長浜山会 entry.
- **Wrong or unsupported entries removed:** ZENQUEST (Lenox, MA), Otanaha Muay Thai (Kediri, Indonesia) and Oikawa Dojo (Osaka) appeared in searches but are not in Okinawa. 泰道道場 is not a separate Kyokushin dojo.
- **Corrections:** DROP is kickboxing (not BJJ) and has a proper address; Pacific Grappler's second location is unconfirmed, so only Mihara is listed; Impacto BJJ's site shows a closure/relocation notice → `needs_check`; Kuro Hata's address, phone, hours and trial policy added; Kyokushinkaikan branch subpages (10 dojo) now have real addresses, phones, instructors.
- **Kendo** now uses the federation's full published lists: 28 youth clubs, 10 adult groups, 3 iaido/jodo groups (was a 21-club sample).
- **Phone numbers were missing for all 309 karate rows** — the roster does not publish them. They are left blank rather than guessed.
- **Privacy:** apartment names/room numbers trimmed from roster addresses (`privacy_note` column); roster-only listing pages are `noindex` by default.

## New this round
Kobukai (Naha, Uechi-ryu/Matayoshi kobudo), MCCS Martial Arts Program (full programme list with fees and joining steps), Kyokushinkaikan dojo detail, full kendo lists, Leos BJJ Academy, Tenka Ichi Dojo Chatan, Wild Shisa Koza, MMA/kickboxing/boxing/BJJ/jujutsu all as first-class art pages.

## Not resolved (be honest about these)
- **Judo** now has the 13 dojo from the All Japan Judo Federation's Dojo Navi (days/times/addresses; phone numbers are on each dojo's detail page and not yet copied).
- **309 karate rows are level C** (2019, not re-verified). No phone, hours or website for almost all of them.
- Itoman Gym's site disallows automated access → could not be verified (level B, `needs_check`).
- Kyokushin Kusaba and Matsue subpages were not fetched; Kyokushinkaikan class schedules are images.
- No coordinates → no map or "near me" yet.
- Several gyms (Maki Gym Chatan, PoliDia, CROSS×LINE, Ground Slam, BJ MMA, Wild Shisa) are known only from directories with no street address; labelled D/`needs_check`.
- Aikido and Shorinji Kempo dojo came from federation directories, not re-checked individually.

## Update (same day)
- Impacto BJJ (Chatan and Ginowan) set to **active** on a member's first-hand report (level B, because the gym's own site shows a closure notice) — confirm which location(s) and update.
- Kyokushinkaikan 'Matsue Dojo' is listed on the Okinawa branch's site with a Kitakyushu (Fukuoka) address — excluded. The 'Kusaba' page was a duplicate of it.
- Not yet cross-checked against: Okinawa Karatedo Federation 加盟道場一覧, Okinawa Karatedo Rengokai (okf.okinawa) 加盟道場一覧 (2024), Okinawa Karate Navi, Prefectural Sports Association member list. These are the best next sources for the 2019 roster sweep.
