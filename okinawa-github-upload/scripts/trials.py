# Curated trial / drop-in prices for the visitors page.
# Each entry: listing id -> (group, sort_yen, price_en, price_ja)
# group: "free" | "paid" | "agency". Prices are as published by the operator (or agency) when checked;
# the listing page carries the source. Keep in step with the listing's "visitors" text.

TRIALS = {
    # free trials
    "roster-129": ("free", 0, "Free trial class", "無料体験クラス"),
    "carpediem-okinawa": ("free", 0, "Free trial (one per person); visitors ¥3,000 a day", "無料体験（1人1回）・ビジター1日3,000円"),
    "waka-jiujitsu": ("free", 0, "Free trial; visitors ¥3,000 a session (book ahead)", "無料体験・ビジター1回3,000円（要予約）"),
    "pacific-grappler-mihara": ("free", 0, "1-week free trial; drop-in ¥2,000", "1週間無料体験・ドロップイン2,000円"),
    "kurohata-bjj": ("free", 0, "1-week free trial; drop-in ¥5,000", "1週間無料体験・ドロップイン5,000円"),
    "axross-jiujitsu": ("free", 0, "1-month free trial", "1か月無料体験"),
    "polidia": ("free", 0, "Free trial (personal-lesson trial ¥2,200)", "無料体験（パーソナル体験2,200円）"),
    "refinas-naha": ("free", 0, "Free first trial", "初回無料体験"),
    "riotgym": ("free", 0, "Free trial", "無料体験"),
    "tomigusuku-gym": ("free", 0, "Free trial (web booking only)", "無料体験（ウェブ予約のみ）"),
    "nago-muaythai": ("free", 0, "Free trial lessons", "無料体験"),
    "itoman-gym": ("free", 0, "Free trial; visitors ¥3,300", "無料体験・ビジター3,300円"),
    "sekai-sokyokushin-okinawa": ("free", 0, "Free trial lessons", "無料体験"),
    # paid trials, drop-ins and dojo experiences
    "drop-kickboxing": ("paid", 1000, "Trial ¥1,000", "体験1,000円"),
    "coa-jiujitsu-naha": ("paid", 1500, "Visitors ¥1,500 a day", "出稽古1日1,500円"),
    "roster-108": ("paid", 3000, "Trial ¥3,000", "体験3,000円"),
    "roster-167": ("paid", 3000, "Karate & kobudo experience ¥3,000 (about 3 hours)", "空手・古武道体験3,000円（約3時間）"),
    "asato-dojo": ("paid", 3000, "Visitors ¥3,000 a class; 1-month pass ¥20,000", "ビジター1回3,000円・1か月20,000円"),
    "blackbelt-japan-naha": ("paid", 3300, "Trial ¥3,000 + tax an hour", "体験1時間3,000円＋税"),
    "blackbelt-japan-koza": ("paid", 3300, "Trial ¥3,000 + tax an hour", "体験1時間3,000円＋税"),
    "roster-065": ("paid", 4000, "Trial in a regular class ¥4,000 (90 min); private ¥8,000", "通常稽古体験4,000円（90分）・個人8,000円"),
    "roster-004": ("paid", 5000, "Trial ¥5,000", "体験5,000円"),
    "roster-190": ("paid", 5000, "Trial ¥5,000 (about 90 min)", "体験5,000円（約90分）"),
    "roster-267": ("paid", 5000, "Trial ¥5,000", "体験5,000円"),
    "roster-034": ("paid", 5000, "Regular class ¥5,000 (120 min); private ¥10,000 (90 min)", "道場稽古5,000円（120分）・個人10,000円（90分）"),
    "kobukai-naha": ("paid", 8800, "Group lesson ¥8,000, private ¥20,000 (plus tax)", "グループ8,000円・個人20,000円（税別）"),
    "okinawa-karate-kaikan": ("paid", 10000, "Karate experience ¥10,000 per person (groups of 3+, book a month ahead)", "空手体験1人10,000円（3名以上・1か月前までに予約）"),
    "roster-030": ("paid", 10000, "Experience ¥20,000 for one; ¥10,000 each for 3–6", "体験1名20,000円・3〜6名は1人10,000円"),
    "roster-008": ("paid", 20000, "Experience ¥20,000 for 1–10 people (120 min)", "体験1〜10名で20,000円（120分）"),
}
# Dojo that take visitors' lessons booked through Ageshio Japan (group ¥8,000 / private ¥20,000 + tax)
AGESHIO = ["roster-004", "roster-270", "roster-040", "roster-246", "roster-190", "roster-129", "roster-035",
           "roster-037", "roster-065", "roster-248", "roster-170", "roster-153", "roster-087", "roster-076"]
