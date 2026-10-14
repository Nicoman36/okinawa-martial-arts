"""Hand-curated (non-roster) listings. Each dict is one location.
ver: A = official/primary source checked 2026-10; B = third-party listing or older page, not independently confirmed;
     D = lead only (exact location unconfirmed).
"""
V = "2026-10-12"

def L(id, ja, en, disc, style, kind, muni, addr_ja="", addr_en="", phone="", web="", social="", email="",
      hours="", contact="", notes="", visitors="", english="unknown", ver="B", status="active", src=(), src_date="", verified=None, alias=""):
    return dict(id=id, name_ja=ja, name_en=en, disciplines=list(disc), style=style, kind=kind, muni=muni,
                address_ja=addr_ja, address_en=addr_en, phone=phone, website=web, social=social, email=email,
                hours=hours, contact=contact, notes=notes, visitors=visitors, english=english, verification=ver,
                status=status, sources=list(src), source_date=src_date,
                last_verified=(verified if verified is not None else (V if ver == "A" else "")), aliases=alias)

KY = "kyokushin-okinawa"
KYK = [  # Kyokushinkaikan (IKO) Okinawa branch — official site subpages, fetched 2026-10-12
 L("kyokushinkaikan-naha","極真会館沖縄県支部 県本部 那覇道場","Kyokushinkaikan (IKO) Okinawa Branch — Naha Dojo (Prefectural HQ)",["kyokushin"],"Kyokushin full-contact karate (IKO Kyokushinkaikan)","dojo","那覇市","那覇市泉崎2-4-2 Kinjo Bldg 3F",
   phone="098-854-0079",web="https://www.kyokushinokinawa.com/",email="kyokushin_okinawa@yahoo.co.jp",contact="Branch chief 七戸康博 (Yasuhiro Shichinohe)",
   notes="Junior, women's and general divisions. Class schedule is posted on the site as an image — confirm by phone/email.",ver="A",src=[KY],src_date="2026-10"),
 L("kyokushinkaikan-ginowan","極真会館沖縄県支部 宜野湾道場","Kyokushinkaikan (IKO) — Ginowan Dojo",["kyokushin"],"Kyokushin full-contact karate (IKO Kyokushinkaikan)","dojo","宜野湾市","〒901-2204 宜野湾市上原1-2-9 (Kopo Tiger 205)",
   phone="070-5816-9027",web="https://www.kyokushinokinawa.com/",hours="Tue/Thu 7:30–9:00 (Shinta Tawata); Sat 7:15–8:30 (Shinji Tawata) — AM/PM not stated on the branch page; confirm",contact="Shinta Tawata / Shinji Tawata (田場)",
   notes="Second number during practice: 098-892-7256.",ver="A",src=[KY],src_date="2026-10"),
 L("kyokushinkaikan-itoman","極真会館沖縄県支部 糸満道場","Kyokushinkaikan (IKO) — Itoman Dojo",["kyokushin"],"Kyokushin full-contact karate (IKO Kyokushinkaikan)","dojo","糸満市","糸満市西崎2-35-8",
   phone="090-3797-2911",web="https://www.kyokushinokinawa.com/",contact="大城久男",visitors="Visitors invited to observe a class (per branch site).",ver="A",src=[KY],src_date="2026-10"),
 L("kyokushinkaikan-nago","極真会館沖縄県支部 名護道場","Kyokushinkaikan (IKO) — Nago Dojo",["kyokushin"],"Kyokushin full-contact karate (IKO Kyokushinkaikan)","dojo","名護市","〒905-0015 名護市大南2-5-15 2F",
   phone="090-9784-9809",web="https://www.kyokushinokinawa.com/",ver="A",src=[KY],src_date="2026-10"),
 L("kyokushinkaikan-uruma","極真会館沖縄県支部 うるま道場","Kyokushinkaikan (IKO) — Uruma Dojo",["kyokushin"],"Kyokushin full-contact karate (IKO Kyokushinkaikan)","dojo","うるま市","〒904-2215 うるま市みどり町4-20-28",
   phone="090-2394-4593",web="https://www.kyokushinokinawa.com/",contact="金城芽唯美",ver="A",src=[KY],src_date="2026-10"),
 L("kyokushinkaikan-ishigaki","極真会館沖縄県支部 石垣道場","Kyokushinkaikan (IKO) — Ishigaki Dojo",["kyokushin"],"Kyokushin full-contact karate (IKO Kyokushinkaikan)","dojo","石垣市","〒907-0004 石垣市字登野城918-7",
   phone="090-1877-3868",web="https://www.kyokushinokinawa.com/",contact="田福雄市",ver="A",src=[KY],src_date="2026-10"),
 L("kyokushinkaikan-urasoe","極真会館沖縄県支部 浦添道場","Kyokushinkaikan (IKO) — Urasoe Dojo",["kyokushin"],"Kyokushin full-contact karate (IKO Kyokushinkaikan)","dojo","浦添市","浦添市宮城3-1-3 1F",
   phone="090-1946-4109",web="https://www.kyokushinokinawa.com/",contact="宮城健志",ver="A",src=[KY],src_date="2026-10"),
 L("kyokushinkaikan-shuri","極真会館沖縄県支部 首里道場","Kyokushinkaikan (IKO) — Shuri Dojo",["kyokushin"],"Kyokushin full-contact karate (IKO Kyokushinkaikan)","dojo","那覇市","那覇市首里石嶺町4-9-1 グランビュー石嶺202",
   phone="098-885-7690",web="https://www.kyokushinokinawa.com/",contact="七戸康博 / 宮城健志",ver="A",src=[KY],src_date="2026-10"),
 L("kyokushinkaikan-miyako","極真会館沖縄県支部 宮古道場","Kyokushinkaikan (IKO) — Miyako Dojo",["kyokushin"],"Kyokushin full-contact karate (IKO Kyokushinkaikan)","dojo","宮古島市","〒906-0013 宮古島市平良下里1146-5 2F (南修館内)",
   phone="080-4697-8992",web="https://www.kyokushinokinawa.com/",email="kyokushinmiyako@gmail.com",contact="下地正喜 (Masaki Shimoji)",ver="A",src=[KY],src_date="2026-10"),
 L("kyokushinkaikan-yaese","極真会館沖縄県支部 八重瀬道場","Kyokushinkaikan (IKO) — Yaese Dojo",["kyokushin"],"Kyokushin full-contact karate (IKO Kyokushinkaikan)","dojo","八重瀬町","〒901-0406 八重瀬町字屋宜原147-1 (屋宜原公民館)",
   phone="090-2394-3427",web="https://www.kyokushinokinawa.com/",hours="Wed & Fri: kids (age 4–6th grade) 18:30–20:00; general (junior high & up) 20:00–21:30",contact="屋宜秀多朗 (Shutaro Yagi)",ver="A",src=[KY],src_date="2026-10"),
]

SK = "shinkyokushin-okinawa"
def _sk(id, ja, en, muni, addr, phone):
    return L(id, ja, en, ["kyokushin"], "Shinkyokushinkai (WKO) full-contact karate", "dojo", muni, addr, phone=phone, web="https://yoshidadojo.jp/",
             contact="Branch chief 吉田富和 (Tomikazu Yoshida)", visitors="Ages 3+ accepted; trial lessons advertised on the branch page.", ver="B", src=[SK], src_date="2026")
SKS = [
 _sk("shinkyokushin-aja","新極真会沖縄支部 安謝本部道場","Shinkyokushinkai (WKO) Okinawa — Aja Honbu Dojo","那覇市","〒900-0003 那覇市字安謝231-2 丸喜ビル1F","098-943-9696"),
 _sk("shinkyokushin-makiminato","新極真会沖縄支部 浦添牧港道場","Shinkyokushinkai (WKO) Okinawa — Urasoe Makiminato Dojo","浦添市","〒901-2131 浦添市牧港5-11-5 プログレスビル2F","080-9068-1789"),
 _sk("shinkyokushin-hambeetown","新極真会沖縄支部 北谷ハンビータウン道場","Shinkyokushinkai (WKO) Okinawa — Chatan Hambeetown Dojo","北谷町","〒904-0117 北谷町北前1-2-3 サンエーハンビータウン スタジオOK内","080-9068-1789"),
 _sk("shinkyokushin-uruma","新極真会沖縄支部 うるま道場","Shinkyokushinkai (WKO) Okinawa — Uruma Dojo","うるま市","〒904-2214 うるま市安慶名18-263 安慶名公民館内","080-9068-1789"),
 _sk("shinkyokushin-tomigusuku","新極真会沖縄支部 豊見城道場","Shinkyokushinkai (WKO) Okinawa — Tomigusuku Dojo","豊見城市","〒901-0244 豊見城市宜保21 宜保公民館","090-3414-4114"),
 _sk("shinkyokushin-itoman","新極真会沖縄支部 糸満道場","Shinkyokushinkai (WKO) Okinawa — Itoman Dojo","糸満市","〒901-0364 糸満市潮崎町1-1-2 シャボン玉石けん くくる糸満内","090-3414-4114"),
 _sk("shinkyokushin-omoromachi","新極真会沖縄支部 おもろまち道場","Shinkyokushinkai (WKO) Okinawa — Omoromachi Dojo","那覇市","〒900-0006 那覇市おもろまち1-1-25 リュークスタワー集会室","080-9068-1789"),
 L("kyokushinkan-ginoza","極真館 沖縄道場","Kyokushinkan Okinawa Dojo (Ginoza)",["kyokushin"],"Kyokushinkan full-contact karate","dojo","宜野座村","宜野座村字惣慶1490",phone="090-3321-7300",web="https://kyokushinkan.org/",contact="平田亘 (Wataru Hirata)",ver="B",src=["kyokushinkan-org"],src_date="2026"),
 L("byakurenkaikan-okinawa","白蓮会館 沖縄支部 (那覇・宜野湾)","Byakurenkaikan Okinawa Branch (Naha & Ginowan)",["kyokushin"],"Byakuren-kaikan full-contact karate","dojo","那覇市",ver="D",status="needs_check",
   notes="Active in competition results; no official Okinawa branch page found. Addresses not confirmed.",src=["competition-results"],src_date="2025"),
 L("sekai-sokyokushin-okinawa","世界総極真 沖縄 (空田道場ほか)","Sekai Sokyokushin Okinawa (incl. Kuta Dojo)",["kyokushin"],"Sekai Sokyokushin full-contact karate","dojo","",web="okinawakyokushin.com",ver="D",status="needs_check",
   notes="Address not published online; location (Naha area) not confirmed.",src=["official-site"],src_date="2026"),
]

KENDO_SRC = ["okikenren"]
def _k(id, ja, en, muni, venue, phone, hours, contact, notes="", kind="club"):
    return L(id, ja, en, ["kendo"], "Kendo (youth club)", kind, muni, venue, phone=phone, web="https://www.okikenren.jp/kyoushitsu-ichiran/", hours=hours, contact=contact,
             notes=notes or "Youth kendo class listed by the Okinawa Kendo Federation. Adults/parents: ask the contact whether beginners or adults can join.", ver="A", src=KENDO_SRC, src_date="2026-10")
KENDO_YOUTH = [
 _k("kendo-miyako-renmei","宮古郡剣道連盟","Miyako District Kendo Federation (youth class)","宮古島市","北小学校体育館 (Kita Elementary School gym)","0980-73-4882","Mon/Wed/Fri 18:30–20:00","根間"),
 _k("kendo-yaeyama-youth","八重山地区剣道スポーツ少年団","Yaeyama Area Kendo Youth Sports Club","石垣市","八重山警察署武道場 (Yaeyama Police Station dojo)","098-082-0110","Mon/Wed/Fri 18:00–20:00","船道"),
 _k("kendo-honbu-yaedake","本部警察署八重岳少年剣道クラブ","Motobu Police Yaedake Youth Kendo Club","本部町","本部警察署武道場 (2nd/4th Tue) / 本部中学校体育館 (Tue/Thu)","070-3800-7033","2nd & 4th Tue 19:00–21:00; Tue/Thu 19:00–21:00","大城"),
 _k("kendo-nago-kyoshitsu","名護剣道教室","Nago Kendo Class","名護市","名護小学校体育館 (Tue) / 大宮小学校体育館 (Thu)","0980-53-0772","Tue/Thu 19:00–20:30","与那覇"),
 _k("kendo-nago-police","名護警察署スポーツ少年団","Nago Police Sports Youth Club (Kendo)","名護市","東江小学校体育館 (Tue) / 名護警察署武道場 (Fri)","090-1510-4847","Tue/Fri 19:00–21:00","屋比久"),
 _k("kendo-ishikawa-gaku","石川岳少年剣道教室","Ishikawa-dake Youth Kendo Class","うるま市","沖縄県警察学校体育館 (Okinawa Police Academy gym)","098-964-2788","Tue/Thu 18:30–20:00","山田"),
 _k("kendo-gushikawa","具志川少年剣道クラブ","Gushikawa Youth Kendo Club","うるま市","あげな中学校武道場 (Agena Junior High dojo)","098-972-3766","Mon/Fri 18:30–20:30","兼城"),
 _k("kendo-kenshikan","沖縄剣志館","Okinawa Kenshikan (Kendo)","うるま市","沖縄剣志館 (Ishikawa 818-4 per earlier listing)","098-965-7041","Beginner Tue/Thu 17:30–18:30; Intermediate Tue/Thu/Fri 19:00–20:45; Advanced Mon/Wed/Fri 19:00–20:45","糸数",kind="dojo"),
 _k("kendo-okinawa-city-youth","沖縄市幼少年剣道部","Okinawa City Youth Kendo Section","沖縄市","沖縄市武道館 (Okinawa City Budokan)","098-938-7393","Mon/Thu 18:30–20:00; Sat 18:00–19:00","町田"),
 _k("kendo-okinawa-police","沖縄警察署スポーツ少年団","Okinawa Police Station Sports Youth Club (Kendo)","沖縄市","沖縄警察署武道場","098-932-1768","Tue/Wed/Fri 18:30–20:00; Sat 17:00–19:00","大道"),
 _k("kendo-kadena","嘉手納少年剣道クラブ","Kadena Youth Kendo Club","嘉手納町","練武館 (Renbukan)","090-5028-1377","Mon/Wed/Fri 18:30–20:30","竹下"),
 _k("kendo-nirai","ニライ剣道スポーツ少年団","Nirai Kendo Youth Sports Club","北谷町","浜川小学校体育館 (Hamagawa Elementary gym)","090-2968-3592","Tue 17:30–19:00; Sat 16:30–19:00 (winter shorter)","比嘉"),
 _k("kendo-nishihara","西原剣道クラブ","Nishihara Kendo Club","西原町","西原町民体育館武道場","098-944-3325","Tue/Fri 19:00–21:00; Wed 20:00–21:00 (armor group)","手登根"),
 _k("kendo-ginowan-chiku","宜野湾地区スポーツ少年団","Ginowan Area Sports Youth Club (Kendo)","宜野湾市","宜野湾警察署道場","098-874-8258","Tue/Thu/Sat 18:00–21:00","宮里"),
 _k("kendo-ginowan-hagoromo","宜野湾市はごろも剣道スポーツ少年団","Ginowan Hagoromo Kendo Youth Sports Club","宜野湾市","宜野湾市大謝名児童センター","098-893-1805","Tue/Thu/Fri 18:30–20:30","根本"),
 _k("kendo-ginowan-gaja","宜野湾市 剣道 我如古道場","Ginowan Kendo — Gaja Dojo","宜野湾市","志真志小学校体育館 (Wed) / 我如古区公民館 (Fri)","090-8415-9272","Wed/Fri 18:00–20:00","前泊"),
 _k("kendo-urasoe-youth","浦添少年剣道クラブ","Urasoe Youth Kendo Club","浦添市","浦添警察署内武道場 / 西原町民体育館 (Sat)","090-9490-2226","Mon/Wed/Fri 18:00–20:00; Sat 9:00–12:00","仲村"),
 _k("kendo-wakawashi","わかわし剣道スポーツ少年団","Wakawashi Kendo Youth Sports Club","那覇市","真和志小学校体育館","090-4343-4172","Wed/Thu 18:00–19:00; Sat 16:00–19:00","請舛"),
 _k("kendo-johoku","城北剣道クラブスポーツ少年団","Johoku Kendo Club","那覇市","那覇市立城北小体育館","098-890-5808","Tue 18:00–20:00; Sat 7:30–9:30; Sun 9:00–11:00","上間"),
 _k("kendo-tenpi","天妃剣道教室","Tenpi Kendo Class","那覇市","天妃小学校体育館","098-867-9441","Thu 17:45–18:00; Sat/Sun/holidays 9:30–12:00","下地"),
 _k("kendo-daidojuku","大道塾 (剣道)","Daidojuku Kendo (Mihara, Naha)","那覇市","大道塾 (三原3-12-32 per earlier listing)","098-855-2507","Tue/Thu/Sat 18:00–20:00; Sun 9:30–11:30","松川",kind="dojo"),
 _k("kendo-ougon-no-mori","黄金の森剣道クラブスポーツ少年団","Ougon-no-Mori Kendo Youth Club","南風原町","南風原中学校武道場","090-5489-1783","Tue/Thu 17:00–19:00; Sat 9:00–12:00","仲間"),
 _k("kendo-toyosaki","豊崎剣道クラブ","Toyosaki Kendo Club","豊見城市","豊崎小学校体育館","090-8412-1403","Tue/Thu 18:00–20:00; Sat 9:00–11:30","島田"),
 _k("kendo-ryushikan","豊見城剣道教室 琉志館","Ryushikan Kendo Class (Okinawa Karate Kaikan)","豊見城市","沖縄空手会館 (Okinawa Karate Kaikan)","080-6491-7816","Mon/Thu/Fri 17:00–19:00","山川"),
 _k("kendo-yonabaru-police","与那原警察署スポーツ少年団若駒励心会","Yonabaru Police Wakakoma Reishinkai (Kendo)","与那原町","与那原警察署武道場","098-945-0110","Tue/Thu 18:00–20:00","宮城"),
 _k("kendo-renmakai","錬磨会","Renmakai Kendo","南城市","大里北児童館","098-946-9164","Sun 9:00–12:00; Wed 18:30–20:00; Sat 8:00–9:30; holidays 9:00–11:00","梶原"),
 _k("kendo-itoman-kenshikai","糸満剣志会","Itoman Kenshikai","糸満市","兼城小学校体育館","090-7395-8851","Tue/Fri 18:30–20:00; Thu 18:00–20:00","金良"),
 _k("kendo-gushikawa-elem","具小剣道教室","Gushikawa Elementary Kendo Class","うるま市","具志川小学校体育館","090-9789-1979","Tue 17:30–19:00; Sat 10:00–12:00","天願"),
]
def _g(id, ja, en, muni, venue, phone, hours, contact, disc=("kendo",), style="Kendo (adult / general practice group)"):
    return L(id, ja, en, disc, style, "club", muni, venue, phone=phone, web="https://www.okikenren.jp/", hours=hours, contact=contact, ver="A", src=KENDO_SRC, src_date="2026-10",
             notes="General (adult) practice session listed by the Okinawa Kendo Federation; confirm beginner access with the contact.")
KENDO_GENERAL = [
 _g("kendo-gen-miyako","宮古郡剣道連盟 (一般稽古)","Miyako District Kendo Federation (adult practice)","宮古島市","北小学校体育館","070-4086-9555","Mon/Wed/Fri 19:00–20:30","根間康雄"),
 _g("kendo-gen-yaeyama","八重山剣道連盟 (一般稽古)","Yaeyama Kendo Federation (adult practice)","石垣市","石垣第二中学校","090-5747-6761","Mon/Wed/Thu/Sat 16:30–18:00 (Sat from 14:30)","吉見"),
 _g("kendo-gen-kunigami","国頭郡剣道連盟 (一般稽古)","Kunigami District Kendo Federation (adult practice)","本部町","本部中学校 / 本部警察署 (2nd & 4th Tue)","090-7585-3941","Tue/Thu 19:00–21:00","大城"),
 _g("kendo-gen-nago","名護市剣道連盟 (一般稽古)","Nago City Kendo Federation (adult practice)","名護市","名護小学校 (Tue) / 大宮小学校 (Thu)","0980-53-0772","Tue 19:00–21:00; Thu (time not listed)","与那覇"),
 _g("kendo-gen-uruma","うるま市剣道連盟 (一般稽古)","Uruma City Kendo Federation (adult practice)","うるま市","あげな中学校武道場","098-972-3766","Mon 20:00–21:00","兼城"),
 _g("kendo-gen-okinawa-city","沖縄市剣道連盟 (一般稽古)","Okinawa City Kendo Federation (adult practice)","沖縄市","沖縄市武道館","090-9650-5824","Mon/Thu 20:00–21:00","町田"),
 _g("kendo-gen-urasoe","浦添市剣道連盟 (一般稽古)","Urasoe City Kendo Federation (adult practice)","浦添市","うらそえぐすく児童館","090-1944-4323","4th Thu 20:00–22:00","松田"),
 _g("kendo-gen-naha","那覇市剣道連盟 (一般稽古)","Naha City Kendo Federation (adult practice)","那覇市","県立武道館 錬成道場2F (Okinawa Prefectural Budokan)","","Mon/Wed/Fri 18:00–20:00","(not listed)"),
 _g("kendo-gen-itoman","糸満市剣道連盟 (一般稽古)","Itoman City Kendo Federation (adult practice)","糸満市","兼城小学校","098-992-3887","Tue/Thu/Fri 18:30–20:00","山城忍"),
 _g("kendo-ryudai","琉球大学剣道部","University of the Ryukyus Kendo Club","西原町","琉球大学第一体育館 2階武道場","","Tue/Thu/Sat 18:00–19:30 (Sat also 11:00–13:00)","比嘉",style="Kendo (university club)"),
 _g("iaido-okinawa","沖縄県剣道連盟 居合道部","Okinawa Kendo Federation — Iaido Section","那覇市","県立武道館 第2錬成道場 (奥武山町)","090-7150-1517","Thu 18:30–20:30","竹田忠司 (教士七段)",disc=("kendo",),style="Iaido"),
 _g("jodo-hachikuku","破竹杖道会","Hachiku Jodo-kai","浦添市","浦添体育館内 武道場","090-7150-1517","Tue/Fri 18:30–20:30","竹田忠司",disc=("kendo",),style="Jodo"),
 _g("jodo-meisuikan","明垂館道場","Meisuikan Dojo (Jodo)","那覇市","那覇市銘苅1-17-6","090-3795-2056","Mon/Wed/Fri (times vary — see federation list)","譜久原朝彰",disc=("kendo",),style="Jodo"),
]

OTHER = [
 # ---------- Karate / Kobudo (non-roster) ----------
 L("kobukai-naha","古武会 (金城 隆)","Kobukai — Uechi-ryu & Matayoshi Kobudo (Naha)",["karate","kobudo"],"Uechi-ryu karate; Kobu-ryu / Matayoshi kobudo","dojo","那覇市",addr_en="Naha City (street address not published)",
   phone="098-988-3888",web="https://ageshiojapan.com/",email="contact@ageshiojapan.com",hours="Tue/Thu 20:00–21:30; Sat 18:00–19:30 (a morning class is mentioned, no time given)",contact="Takashi Kinjo (Uechi-ryu 10th dan)",
   visitors="Group lesson ¥8,000 and private ¥20,000 (excl. tax) per the dojo page; bring your own belt if you have one; photos only with the sensei's permission, no video.",english="Site is bilingual; lesson language not stated.",ver="A",src=["ageshio"],src_date="2026-10"),
 L("asato-dojo","首里手・古武道 安里道場 (Asato Dojo)","Asato Dojo — Shuri-te / Kobudo (Naha)",["karate","kobudo"],"Shuri-te / kobudo","dojo","那覇市",addr_en="Near Kokusai-dori, Naha (exact address not published)",
   contact="James Pankiewicz Sensei",ver="B",status="needs_check",src=["visitor-reviews"],src_date="2019",notes="Appears in visitor write-ups; no official site found. Confirm before visiting."),
 L("intl-karate-study-centre","国際空手研修センター","International Karate Study Centre (Yomitan)",["karate"],"Traditional Okinawan karate (multi-style host)","dojo","読谷村",addr_en="Yomitan Village (address not confirmed)",ver="B",status="needs_check",src=["visitor-reviews"]),
 L("okinawa-karate-kaikan","沖縄空手会館","Okinawa Karate Kaikan (visitor centre & dojo)",["karate","kobudo"],"Cultural facility — multi-style demonstrations and short experiences","program","豊見城市","豊見城市豊見城854-1",
   web="https://karatekaikan.jp/en",notes="Prefectural karate centre with a museum, dojo and short karate/kobudo experiences for visitors. Also hosts Daido-juku Naha and the Ryushikan kendo class.",english="Yes — English-language visitor information is provided.",ver="A",src=["karatekaikan"],src_date="2026-10"),
 L("ryukyukan-kadena","琉球館 嘉手納基地道場","Ryukyukan International — Kadena Air Base Dojo",["karate","kobudo"],"Shorin-ryu (Ryukyukan International)","club","嘉手納町",addr_en="Kadena Air Base (on-base; building not published)",social="https://www.facebook.com/ryukyukankadena",
   notes="On-base: access requires base authorization.",english="Yes (base community).",ver="B",src=["facebook"],src_date="2026"),
 L("nix-seidokan","ニックス 成道館","Nix Seidokan Dojo — Motobu-ryu (Okinawa City)",["karate","kobudo"],"Motobu-ryu Seidokan (RSKKR)","dojo","沖縄市",addr_en="Okinawa City (street address not published)",contact="Ron Nix",ver="B",status="needs_check",src=["official-site"]),

 # ---------- Judo (All Japan Judo Federation "Dojo Navi", Okinawa list of 13, fetched 2026-10-12) ----------
 L("judo-okinawa-police-youth","沖縄署スポーツ少年団柔道部","Okinawa Police Sports Youth Club — Judo (Okinawa City)",["judo"],"Kodokan judo (youth club)","club","沖縄市","沖縄市山里2-4-20 沖縄警察署",hours="Mon & Thu 18:30–20:30; Sat 9:30–12:00",ver="A",src=["judo-dojo-navi"],src_date="2026-10",web="https://www.judo.or.jp/dojo-navi/dojo/detail/14370"),
 L("judo-miyakojima-police","宮古島警察署少年柔道クラブ","Miyakojima Police Station Youth Judo Club",["judo"],"Kodokan judo (youth club)","club","宮古島市","宮古島市平良西里1092-1 宮古島警察署3階武道場",hours="Mon/Wed/Fri 19:00–20:30",ver="A",src=["judo-dojo-navi"],src_date="2026-10",web="https://www.judo.or.jp/dojo-navi/dojo/detail/15807"),
 L("judo-yomitan-youth","読谷少年柔道クラブ","Yomitan Youth Judo Club",["judo"],"Kodokan judo (youth club)","club","読谷村","読谷村字座喜味2976-2 読谷中学校武道場",hours="Mon/Wed/Thu/Fri/Sat 18:00–20:00 (Sat may be morning); closed Tue & Sun",ver="A",src=["judo-dojo-navi"],src_date="2026-10",web="https://www.judo.or.jp/dojo-navi/dojo/detail/14840"),
 L("judo-shinjukai","真柔会少年柔道","Shinjukai Youth Judo (Naha)",["judo"],"Kodokan judo (youth club)","club","那覇市","那覇市松山2-24-1 那覇中学校",hours="Mon 18:00–20:00; Wed & Fri 18:30–20:30",ver="A",src=["judo-dojo-navi"],src_date="2026-10",web="https://www.judo.or.jp/dojo-navi/dojo/detail/10564"),
 L("judo-shogaku","沖縄尚学少年柔道教室","Okinawa Shogaku Youth Judo Class (Naha)",["judo"],"Kodokan judo (youth class)","club","那覇市","那覇市字国場747 沖縄尚学高等学校武道場",hours="Mon/Wed/Fri 19:00–21:00",ver="A",src=["judo-dojo-navi"],src_date="2026-10",web="https://www.judo.or.jp/dojo-navi/dojo/detail/10761"),
 L("judo-senbukan","泉武館","Senbukan Judo (Uruma)",["judo"],"Kodokan judo","dojo","うるま市","うるま市勝連平安名2805",hours="Mon/Wed/Thu/Fri/Sat 17:30–19:30; closed Tue",ver="A",src=["judo-dojo-navi"],src_date="2026-10",web="https://www.judo.or.jp/dojo-navi/dojo/detail/10655"),
 L("judo-shorekan","奨励館勝山塾","Shorekan Katsuyama-juku (Judo, Naha)",["judo"],"Kodokan judo","dojo","那覇市","那覇市松山2-24-1 那覇中学校武道場 (体育館最上階・外階段より)",hours="Tue/Thu/Sat 19:00–21:00",ver="A",src=["judo-dojo-navi"],src_date="2026-10",web="https://www.judo.or.jp/dojo-navi/dojo/detail/16356"),
 L("judo-hagoromo","はごろも柔道クラブ","Hagoromo Judo Club (Ginowan)",["judo"],"Kodokan judo (children / junior high)","club","宜野湾市","宜野湾市真志喜3-19-1 真志喜中学校",hours="Mon/Wed/Fri 18:30–20:30 (children/junior high); Tue/Thu 18:30–20:00 (junior high); Sat by arrangement",ver="A",src=["judo-dojo-navi"],src_date="2026-10",web="https://www.judo.or.jp/dojo-navi/dojo/detail/17239"),
 L("judo-shiseikan","至誠館","Shiseikan (Judo, Tomigusuku)",["judo"],"Kodokan judo","dojo","豊見城市","豊見城市瀬長17-8 豊見城警察署",hours="Mon & Wed 19:00–21:00; Sat 9:30–12:00",ver="A",src=["judo-dojo-navi"],src_date="2026-10",web="https://www.judo.or.jp/dojo-navi/dojo/detail/16903"),
 L("judo-higa-dojo","比嘉道場 (柔道)","Higa Dojo (Judo, Kitanakagusuku)",["judo"],"Kodokan judo","dojo","北中城村","北中城村字喜舎場306 北中城中学校武道場",hours="Mon & Thu 16:00–18:00",ver="A",src=["judo-dojo-navi"],src_date="2026-10",web="https://www.judo.or.jp/dojo-navi/dojo/detail/15688"),
 L("judo-oroku-hiroba","小禄柔道クラブ・みんなで楽しく柔道ひろば","Oroku Judo Club & Judo Hiroba (Naha)",["judo"],"Kodokan judo (club + monthly family event)","club","那覇市","那覇市宇栄原2-23-1 小禄中学校体育館2階",hours="Club Thu 19:30–21:30; 'hiroba' roughly monthly on Saturdays at the Prefectural Budokan 3F (dates on the federation site)",
   notes="Run by the prefectural judo federation; a good first contact for adults and families.",ver="A",src=["judo-dojo-navi"],src_date="2026-10",web="https://www.judo.or.jp/dojo-navi/dojo/detail/10098"),
 L("judo-ginowan-police","宜野湾警察署スポーツ少年団","Ginowan Police Station Sports Youth Club (Judo)",["judo"],"Kodokan judo (youth club)","club","宜野湾市","宜野湾市真志喜2-1-3 宜野湾警察署",hours="Mon/Wed/Fri 18:30–20:20",ver="A",src=["judo-dojo-navi"],src_date="2026-10",web="https://www.judo.or.jp/dojo-navi/dojo/detail/12933"),
 L("judo-itoman-police","糸満署少年柔道クラブ","Itoman Police Youth Judo Club",["judo"],"Kodokan judo (youth club)","club","糸満市","糸満市糸満1736-6 糸満警察署道場",hours="Mon/Wed/Fri 19:00–21:00",ver="A",src=["judo-dojo-navi"],src_date="2026-10",web="https://www.judo.or.jp/dojo-navi/dojo/detail/13857"),
 L("judo-federation","沖縄県柔道連盟","Okinawa Judo Federation",["judo"],"Governing body","organization","那覇市","那覇市長田2-5-31-101",web="judo.spoyell.okinawa",contact="会長 上江洲智明",ver="B",src=["federation-sites"],src_date="2026"),

 # ---------- Kendo federation ----------
 L("kendo-federation","沖縄県剣道連盟","Okinawa Kendo Federation",["kendo"],"Governing body (kendo / iaido / jodo)","organization","那覇市","那覇市奥武山町51-2 沖縄県体協スポーツ会館501",phone="098-859-0410",web="https://www.okikenren.jp/",
   notes="Publishes the youth, general and iaido/jodo practice lists used on this site. Iaido/jodo inquiries: 羽地 090-3198-5862.",ver="A",src=KENDO_SRC,src_date="2026-10"),

 # ---------- Aikido ----------
 L("aikido-naha","沖縄合気会 那覇道場","Okinawa Aikikai — Naha Dojo",["aikido"],"Aikikai aikido","dojo","那覇市","奥武山町52 県立武道館 錬成道場3F",web="https://www.aikido.ne.jp/dojo/okinawa.html",contact="山口巌",ver="B",src=["aikikai-dir"],src_date="2026"),
 L("aikido-honbu","沖縄合気会 本部道場","Okinawa Aikikai — Honbu Dojo",["aikido"],"Aikikai aikido","dojo","那覇市","那覇市宇栄原1-21-3",web="https://www.aikido.ne.jp/dojo/okinawa.html",contact="山口巌",ver="B",src=["aikikai-dir"],src_date="2026"),
 L("aikido-ryukyu-shimpo","琉球新報カルチャー合気道教室","Ryukyu Shimpo Culture Center Aikido Class",["aikido"],"Aikikai aikido","program","那覇市","奥武山町52 県立武道館",web="https://www.aikido.ne.jp/dojo/okinawa.html",contact="山口巌",ver="B",src=["aikikai-dir"],src_date="2026"),
 L("aikido-meio","沖縄合気会 名桜大学合気道部","Okinawa Aikikai — Meio University Aikido Club",["aikido"],"Aikikai aikido","club","名護市","名桜大学柔道場 為又1220-1",web="https://www.aikido.ne.jp/dojo/okinawa.html",ver="B",src=["aikikai-dir"],src_date="2026"),
 L("aikido-uruma","沖縄合気会 うるま市道場","Okinawa Aikikai — Uruma Dojo",["aikido"],"Aikikai aikido","dojo","うるま市","うるま市昆布924",web="https://www.aikido.ne.jp/dojo/okinawa.html",contact="クレンダー ケン (Ken Klender)",ver="B",src=["aikikai-dir"],src_date="2026"),
 L("aikido-koza","沖縄合気会 コザ武道館 (嘉手納基地道場)","Okinawa Aikikai — Koza Budokan",["aikido"],"Aikikai aikido","dojo","沖縄市","コザ総合運動場内武道館 諸見里2-1-1",web="https://www.aikido.ne.jp/dojo/okinawa.html",ver="B",src=["aikikai-dir"],src_date="2026"),
 L("aikido-haebaru","沖縄合気会 南風原カルチャーセンター教室","Okinawa Aikikai — Haebaru Culture Center Class",["aikido"],"Aikikai aikido","program","南風原町","南風原ジャスコ文化センター2F 宮平264",web="https://www.aikido.ne.jp/dojo/okinawa.html",ver="B",src=["aikikai-dir"],src_date="2026"),
 L("aikido-urasoe","合気道教室 浦添道場","Aikido Class — Urasoe Dojo",["aikido"],"Aikikai aikido","dojo","浦添市","浦添市民体育館1階武道場 仲間1-13-1",web="https://www.aikido.ne.jp/dojo/okinawa.html",contact="玉城文雄",ver="B",src=["aikikai-dir"],src_date="2026"),
 L("aikido-kunigami","合気道教室 国頭道場","Aikido Class — Kunigami Dojo",["aikido"],"Aikikai aikido","dojo","国頭村","国頭総合体育館2F武道場 辺士名2142",web="https://www.aikido.ne.jp/dojo/okinawa.html",contact="玉城文雄",ver="B",src=["aikikai-dir"],src_date="2026"),
 L("aikido-yoshinkan","養神館沖縄合気道会","Yoshinkan Aikido Okinawa",["aikido"],"Yoshinkan aikido","club","那覇市","県立武道館 / 沖縄市武道館",ver="B",src=["aikikai-dir"],src_date="2026",notes="Trains at the Prefectural Budokan (Naha) and Okinawa City Budokan."),
 L("aikido-shinshin-toitsu","心身統一合氣道会 沖縄教室","Shin-shin Toitsu Aikido — Okinawa Class",["aikido"],"Ki Society (Shinshin Toitsu) aikido","club","那覇市","奥武山武道館3F",contact="松本康歳",ver="B",src=["aikikai-dir"],src_date="2026"),

 # ---------- Taekwondo ----------
 L("taekwondo-naha","沖縄テコンドー協会 那覇クラス","Okinawa Taekwondo Association — Naha class",["taekwondo"],"Taekwondo (WT)","club","那覇市","沖縄県立武道館 3F 錬成道場, 奥武山町52",web="https://taekwondookinawa.ti-da.net/",hours="Wed & Sun evenings",
   notes="Contact via LINE — see the association blog.",ver="B",src=["official-site"],src_date="2026"),
 L("taekwondo-okinawa-city","沖縄テコンドー協会 沖縄市クラス","Okinawa Taekwondo Association — Okinawa City class",["taekwondo"],"Taekwondo (WT)","club","沖縄市","沖縄県総合運動公園体育館 (泡瀬)",web="https://taekwondookinawa.ti-da.net/",hours="~19:00",ver="B",src=["official-site"],src_date="2026"),

 # ---------- BJJ / grappling ----------
 L("blackbelt-japan-naha","THE BLACKBELT JAPAN 那覇 (旧パラエストラ沖縄)","THE BLACKBELT JAPAN Naha (formerly The Paraestra Okinawa)",["bjj","mma"],"BJJ / Shooto / MMA","gym","那覇市","那覇市国場532-1 メゾンセピア2F",phone="098-851-4739",web="https://theparaestra.jp/",
   contact="松根良太 (Ryota Matsune)",visitors="2018 visitor report: day pass ¥2,000 cash — confirm current policy.",english="Reported English-friendly (visitor reports).",ver="B",src=["official-site","bjjglobetrotters"],src_date="2018–2026",alias="The Paraestra Okinawa"),
 L("blackbelt-japan-koza","THE BLACKBELT JAPAN コザ","THE BLACKBELT JAPAN Koza",["bjj","mma"],"BJJ / Shooto / MMA","gym","沖縄市","沖縄市胡屋2-1-59",web="https://theparaestra.jp/",ver="B",src=["official-site"],src_date="2026"),
 L("carpediem-okinawa","カルペディエム沖縄","Carpe Diem Okinawa (BJJ)",["bjj"],"BJJ (Carpe Diem lineage)","gym","北谷町","北谷町北谷2-14-4 ワイズコーストテラスアラハ2F",phone="050-3187-7867",web="https://carpediem.okinawa/",hours="Operates 7 days a week — see site",ver="B",src=["official-site"],src_date="2026"),
 L("axross-jiujitsu","アクロス柔術","Axross Jiu-Jitsu",["bjj"],"BJJ","gym","沖縄市","沖縄市中央2-7-43 1F",phone="090-6285-3486",web="https://axross.site/",ver="B",src=["official-site"],src_date="2026"),
 L("waka-jiujitsu","若ブラジリアン柔術道場","Waka Brazilian Jiu-Jitsu Dojo",["bjj"],"BJJ","gym","那覇市","那覇市首里山川町3-61-9 1F",phone="098-884-0029",web="https://wakajiujitsu.com/",ver="B",src=["official-site"],src_date="2026"),
 L("kukurosu-jiujitsu","ククロス柔術アカデミー","Kukurosu Jiu-Jitsu Academy",["bjj"],"BJJ","gym","那覇市","那覇市銘苅322-1 真栄城ビル",ver="B",status="needs_check",src=["directory"],src_date="2026",notes="Single directory listing — confirm it is operating."),
 L("gracie-oceania-okinawa","グレイシー・オセアニア沖縄","Gracie Oceania Okinawa",["bjj"],"BJJ (Gracie lineage)","gym","中城村","中城村南上原948",phone="070-6596-5494",ver="B",status="needs_check",src=["directory"],src_date="2026"),
 L("shimazilians","SHIMAZILIANS","SHIMAZILIANS (Nanjo)",["bjj"],"BJJ","club","南城市","南城市大里仲間978 大里中学校武道場",ver="B",status="needs_check",src=["directory"],src_date="2026"),
 L("impacto-okinawa-chatan","IMPACTO BJJ OKINAWA — WKO道場 (北谷)","IMPACTO BJJ Okinawa — WKO Dojo (Chatan)",["bjj"],"BJJ (Impacto lineage)","gym","北谷町","北谷町伊平458",web="https://bjjokinawa.jp/",social="https://www.facebook.com/flavio.d.tanaka",
   contact="Flavio Da Silva",notes="Reported open and training regularly (Oct 2026, community report from members). The gym's own website showed a closure/relocation notice, so confirm class times before visiting.",ver="B",status="active",src=["official-site","community-report"],src_date="2026-10",verified="2026-10-12"),
 L("impacto-okinawa-ginowan","IMPACTO BJJ OKINAWA — 宜野湾道場","IMPACTO BJJ Okinawa — Ginowan Dojo",["bjj"],"BJJ (Impacto lineage)","gym","宜野湾市","宜野湾市真栄原3-8-3",web="https://bjjokinawa.jp/",social="https://www.facebook.com/flavio.d.tanaka",
   contact="Flavio Da Silva",notes="Reported open and training regularly (Oct 2026, community report from members). The gym's own website showed a closure/relocation notice, so confirm class times before visiting.",ver="B",status="active",src=["official-site","community-report"],src_date="2026-10",verified="2026-10-12"),
 L("sakamoto-bjj","イヴァン・サカモト BJJ沖縄 (BJJO)","Ivan Sakamoto BJJ Okinawa (BJJO)",["bjj"],"BJJ","club","沖縄市",addr_en="Trains at Kadena AB, Camp Foster, Camp Courtney and Naha Budokan (per organizer page)",phone="090-4268-0731",
   social="https://www.facebook.com/BJJO-ivan-sakamoto-114460028660049",email="ivansakamoto_bjjo@hotmail.com",contact="Ivan Sakamoto",
   notes="Hosts the annual Okinawa International Jiu-Jitsu Championship (Koza Budokan). Also instructs in the MCCS BJJ program.",ver="B",src=["facebook","mccs"],src_date="2026"),
 L("pacific-grappler-mihara","パシフィック・グラップラー道場 (沖縄市三原)","Pacific Grappler Dojo — Okinawa City (Mihara)",["bjj"],"BJJ","gym","沖縄市","沖縄市三原1-11-2",phone="090-6860-9642",web="https://pacificgrappler.com/",
   contact="Joseph (Joe) Davis",visitors="1-week free trial advertised on the official site.",english="Yes — English-speaking staff.",ver="A",src=["official-site"],src_date="2026-10"),
 L("kurohata-bjj","黒旗 BJJ沖縄","Kuro Hata BJJ Okinawa",["bjj"],"BJJ (IBJJF-certified black belt instructor)","gym","うるま市",addr_en="599-6 Kyan, Uruma, Okinawa 904-2225",phone="070-9095-3740",web="https://kurohataokinawa.com/",email="Admin@kurohataokinawa.com",
   hours="16:30–21:30 (days vary — see site class schedule); women's class Tue/Thu 12:00–13:00",contact="Mike (Michael) Cates",visitors="One-week free trial, equipment provided (per official site).",english="Yes — instruction in English and Japanese.",ver="A",src=["official-site"],src_date="2026-10"),
 L("leos-bjj","レオス BJJ アカデミー","Leos BJJ Academy",["bjj"],"BJJ (gi & no-gi)","gym","",addr_en="Location not confirmed",contact="Andy Murasaki",ver="D",status="needs_check",src=["stripes"],src_date="2026-04",
   notes="Named in an April 2026 Stars and Stripes feature; no address or website found."),
 L("my-bjj-team-futenma","My BJJ Team Okinawa (MCAS Futenma)","My BJJ Team Okinawa (MCAS Futenma)",["bjj"],"BJJ (gi / no-gi)","club","宜野湾市",addr_en="MCAS Futenma (on-base)",   hours="2018 report: Mon & Wed gi 18:00–20:00; Fri no-gi 18:00–20:00",contact="Joseph Davis (2018)",notes="Based on a 2018 write-up — treat as unverified.",ver="D",status="needs_check",src=["bjjglobetrotters"],src_date="2018"),

 # ---------- MMA / kickboxing / Muay Thai ----------
 L("krazy-bee","KRAZY BEE 沖縄","KRAZY BEE Okinawa (Itoman)",["mma","kickboxing","bjj"],"Kickboxing / MMA / BJJ","gym","糸満市","糸満市西崎2-24-3 ホワイトハウス102",phone="098-996-3269",web="https://krazybee.okinawa/",hours="Mon–Fri 13:00–23:00; Sat/Sun/holidays 10:00–15:00",ver="B",src=["official-site"],src_date="2026"),
 L("maki-gym-urasoe","真樹ジムオキナワ (浦添)","Maki Gym Okinawa (Urasoe)",["kickboxing"],"Kickboxing / Muay Thai","gym","浦添市","浦添市内間1-14-5 3F",phone="098-874-5794",ver="B",src=["directory"],src_date="2026"),
 L("maki-gym-chatan","真樹ジム 北谷・沖縄市","Maki Gym Chatan / Okinawa City",["kickboxing"],"Kickboxing / Muay Thai","gym","北谷町",addr_en="Chatan / Okinawa City (exact address not published)",hours="Tue & Fri 18:00–19:00 elementary-school class",visitors="Free trial lesson advertised.",ver="B",status="needs_check",src=["directory"],src_date="2026"),
 L("moriniere-martial-arts","モリニエ・マーシャルアーツ","Moriniere Martial Arts (Chatan)",["bjj","mma","kickboxing"],"Capoeira / BJJ / kickboxing / MMA","gym","北谷町","北谷町北谷2-20-3",phone="098-936-8883",web="https://morinieremartialarts.com/",contact="Benjamin Moriniere",
   alias="Capoeira Academy Okinawa",english="Yes (visitor reports).",notes="Probably the successor to Capoeira Academy Okinawa (2018 write-ups: drop-in ¥2,200).",ver="B",src=["official-site","bjjglobetrotters"],src_date="2026"),
 L("polidia","PoliDia","PoliDia — semi-personal & kickboxing gym (Ginowan)",["kickboxing"],"Kickboxing / BJJ / MMA + fitness","gym","宜野湾市",addr_en="Ginowan (street address not confirmed)",ver="B",status="needs_check",src=["directory"],src_date="2026"),
 L("drop-kickboxing","キックボクシングジム DROP","DROP Kickboxing (Ginowan / Chatan)",["kickboxing"],"Kickboxing / Muay Thai (not BJJ)","gym","宜野湾市","宜野湾市宇地泊",web="https://kickboxingdrop.com/",contact="ロット (Thai-based instructor)",ver="A",src=["official-site"],src_date="2026-10",
   notes="Earlier lists mislabeled DROP as BJJ; it is a kickboxing gym."),
 L("tenka-ichi-chatan","天下一道場 北谷","Tenka Ichi Dojo Chatan",["kickboxing"],"Kickboxing","gym","北谷町",addr_en="Chatan (street address not confirmed)",ver="D",status="needs_check",src=["directory"],src_date="2026",notes="Appears with DROP in a directory group; confirm independently."),
 L("wild-shisa-naha","ワイルドシーサー 那覇","Wild Shisa Naha",["kickboxing"],"Kickboxing / fitness","gym","那覇市",addr_en="Naha — 3 minutes' walk from Kojima station (per directory)",ver="B",status="needs_check",src=["directory"],src_date="2026"),
 L("wild-shisa-koza","ワイルドシーサー コザ","Wild Shisa Koza",["kickboxing"],"Kickboxing / fitness","gym","沖縄市",addr_en="Okinawa City (Koza) — street address not confirmed",ver="D",status="needs_check",src=["directory"],src_date="2026"),
 L("crossline","CROSS×LINE","CROSS×LINE (MMA)",["mma"],"MMA","gym","",addr_en="Okinawa (location not confirmed)",contact="砂辺光久 (Mitsuhisa Sunabe)",ver="D",status="needs_check",src=["directory"],src_date="2026"),
 L("bj-mma-school","BJ MMA SCHOOL","BJ MMA School (Tomigusuku)",["mma","kickboxing"],"MMA / kickboxing / kids wrestling","gym","豊見城市",addr_en="Tomigusuku (street address not confirmed)",ver="D",status="needs_check",src=["directory"],src_date="2026"),
 L("groundslam-app","グランドスラム沖縄 A.P.P","MMA & Fit Ground Slam Okinawa A.P.P",["mma"],"MMA / kickboxing / BJJ / grappling","gym","",addr_en="Okinawa (location not confirmed)",ver="D",status="needs_check",src=["directory"],src_date="2026"),
 L("refinas-naha","リフィナス沖縄那覇","Refinas Naha (kickboxing fitness chain)",["kickboxing"],"Kickboxing fitness (chain)","gym","那覇市","那覇市安里2-4-12 3F",web="https://refinas.jp/gym/naha",hours="Weekdays 11:00–22:00; Sat 10:00–20:00; Sun/holidays 10:00–18:00; closed Mondays",
   notes="Fitness-oriented kickboxing studio rather than a fight gym.",ver="B",src=["official-site"],src_date="2026"),
 L("riotgym","RIOTGYM","RIOTGYM (Ginowan)",["kickboxing"],"Kickboxing / fitness","gym","宜野湾市","宜野湾市愛知",phone="098-943-9499",web="https://riotgym.jimdofree.com/",ver="B",src=["official-site"],src_date="2026"),
 L("tomigusuku-gym","豊見城ジム (Y'ZD)","Tomigusuku Gym (Y'ZD)",["kickboxing"],"Kickboxing","gym","豊見城市",addr_en="Tomigusuku (street address not confirmed)",web="https://okinawakickboxing.net/",ver="B",status="needs_check",src=["directory"],src_date="2026"),
 L("nago-muaythai","名護ムエタイスクール","Nago Muay Thai School",["kickboxing"],"Muay Thai / kickboxing","gym","名護市",addr_en="Nago (street address not confirmed)",web="https://muaythai-nago.blog.jp/",ver="B",status="needs_check",src=["official-site"],src_date="2026"),
 L("itoman-gym","糸満ジム","Itoman Gym (Muay Thai / kickboxing)",["kickboxing"],"Muay Thai / kickboxing","gym","糸満市","糸満市西川町23-11 高良アパート1F",web="https://www.itomangym.com/",ver="B",status="needs_check",src=["directory"],src_date="2026",
   notes="The gym's site disallows automated access, so we could not re-verify it; details come from directory listings."),
 L("setkudo-mccs","セツクド (MCCS)","Setkudo Mixed Martial Arts (MCCS)",["kickboxing","mma"],"Kickboxing, Muay Thai, karate, capoeira","program","宜野湾市",addr_en="MCCS fitness centers (on base)",web="https://www.okinawa.usmc-mccs.org/recreation-fitness/sports/martial-arts",
   contact="Nobuhiro & Kana Hirahara",notes="Folded into the MCCS Martial Arts Program entry below for contact details.",ver="B",status="active",src=["mccs"],src_date="2026-10"),

 # ---------- Boxing ----------
 L("boxing-club-nakazato","ボクシングクラブ ナカザト (ボクシングクラブオキナワ)","Boxing Club Nakazato (a.k.a. Boxing Club Okinawa)",["boxing"],"Boxing","gym","宜野湾市","宜野湾市大山4-2-1 2F",phone="098-890-2785",ver="B",src=["directory"],src_date="2026",alias="ボクシングクラブオキナワ",
   notes="Two earlier directory entries shared this address and phone; merged as one gym."),
 L("okinawa-world-ring","沖縄ワールドリング","Okinawa World Ring (boxing)",["boxing"],"Boxing","gym","宜野湾市","宜野湾市大山2-22-3",phone="098-899-1215",ver="B",src=["directory"],src_date="2026"),
 L("ryuyutaka-boxing","琉豊ボクシングスタジオ","Ryuyutaka Boxing Studio",["boxing"],"Boxing","gym","中城村","中城村和宇慶633-2",phone="098-943-1618",ver="B",src=["directory"],src_date="2026"),
 L("ryukyu-boxing","琉球ボクシングジム","Ryukyu Boxing Gym",["boxing"],"Boxing","gym","宜野湾市","宜野湾市愛知235",phone="098-893-6670",ver="B",src=["directory"],src_date="2026"),
 L("taira-naka-boxing","平仲ボクシングスクール","Tairanaka Boxing School",["boxing"],"Boxing","gym","豊見城市","豊見城市真玉橋175-1",phone="098-856-7888",ver="B",src=["directory"],src_date="2026"),
 L("shimabukuro-boxing","島袋ボクシングジム","Shimabukuro Boxing Gym",["boxing"],"Boxing","gym","沖縄市","沖縄市松本5-19-2 3F",phone="098-934-9321",ver="B",src=["directory"],src_date="2026"),
 L("gushikawa-boxing","具志川ボクシングジム","Gushikawa Boxing Gym",["boxing"],"Boxing","gym","沖縄市","沖縄市中央1-14-2 2F",phone="098-938-4917",ver="B",src=["directory"],src_date="2026"),
 L("boxing-federation","沖縄県ボクシング連盟","Okinawa Boxing Federation (amateur)",["boxing"],"Governing body (amateur boxing)","organization","那覇市",web="https://okinawa.jabf-revival.com/",contact="会長 東江勉",ver="B",src=["federation-sites"],src_date="2026"),

 # ---------- Shorinji Kempo ----------
 L("shorinji-federation","沖縄県少林寺拳法連盟","Okinawa Shorinji Kempo Federation",["shorinji"],"Governing body","organization","浦添市","浦添市宮城4-12-6-403",web="https://shorinji-okinawa.jp/",contact="会長 安室和人",ver="B",src=["federation-sites"],src_date="2026"),
 L("shorinji-nanzan","沖縄南山道院","Okinawa Nanzan Doin (Shorinji Kempo)",["shorinji"],"Shorinji Kempo","dojo","那覇市",addr_en="See shorinji-okinawa.jp for the current address",web="https://shorinji-okinawa.jp/",ver="B",status="needs_check",src=["federation-sites"],src_date="2026"),
 L("shorinji-yanbaru","沖縄やんばる道院","Okinawa Yanbaru Doin (Shorinji Kempo)",["shorinji"],"Shorinji Kempo","dojo","国頭村",addr_en="Northern Okinawa (Yanbaru) — see shorinji-okinawa.jp",web="https://shorinji-okinawa.jp/",ver="B",status="needs_check",src=["federation-sites"],src_date="2026"),

 # ---------- Other arts ----------
 L("sumo-federation","沖縄県相撲連盟","Okinawa Sumo Federation",["sumo"],"Governing body","organization","沖縄市","沖縄市美里4-18-1 (美咲特別支援学校内)",web="https://sumo.spoyell.okinawa/",contact="会長 和宇慶勝則",ver="B",src=["federation-sites"],src_date="2026"),
 L("sumo-gushikawa","沖縄具志川相撲クラブ","Okinawa Gushikawa Sumo Club",["sumo"],"Sumo","club","うるま市",addr_en="Uruma (former Gushikawa)",ver="B",status="needs_check",src=["directory"],src_date="2026"),
 L("wrestling-federation","沖縄県レスリング協会","Okinawa Wrestling Association",["wrestling"],"Governing body","organization","豊見城市",addr_en="Tomigusuku (Nanbu Agriculture & Forestry High School)",ver="B",src=["federation-sites"],src_date="2026"),
 L("wrestling-kadena","嘉手納レスリングクラブ","Kadena Wrestling Club",["wrestling"],"Wrestling","club","嘉手納町",addr_en="Kadena area",ver="B",status="needs_check",src=["directory"],src_date="2026"),
 L("oj-kids-wrestling","OJ KIDS","OJ KIDS (wrestling)",["wrestling"],"Kids wrestling","club","南風原町",addr_en="Haebaru High School dojo",ver="B",status="needs_check",src=["directory"],src_date="2026"),
 L("daidojuku-naha","大道塾 那覇同好会","Daido-juku Kudo — Naha Study Group",["other"],"Kudo (Daido-juku)","club","豊見城市","沖縄空手会館 (Okinawa Karate Kaikan)",contact="佐藤和浩",ver="B",src=["official-site"],src_date="2026"),
 L("capoeira-amants","カプージャポン沖縄支部 (那覇)","Capu Japon Okinawa — Naha (Capoeira Angola)",["capoeira"],"Capoeira Angola","club","那覇市","小禄南公民館 (Oroku Minami Community Center)",social="https://www.instagram.com/amants7_okinawa_capoeira",hours="Sun 13:00–15:00",ver="B",src=["social-media"],src_date="2026"),
 L("capoeira-oist","カプージャポン OIST支部 (恩納)","Capu Japon OIST Branch (Onna)",["capoeira"],"Capoeira Angola","club","恩納村","OIST Ocean View Room",social="https://www.instagram.com/okinawa_oist_capoeira",hours="Tue & Thu 19:30",ver="B",src=["social-media"],src_date="2026"),
 L("krav-maga-uruma","クラヴ・マガ沖縄 (うるま)","Krav Maga Okinawa (Uruma)",["krav-maga"],"Krav Maga","club","うるま市","うるま市安慶名2-23-59",phone="090-4510-9979",email="KravMaga.Okinawa@gmail.com",hours="Tue & Thu 18:30–20:00",contact="Kenneth",english="Yes.",ver="B",status="needs_check",src=["directory"],src_date="2026"),
 L("krav-maga-japan-rycom","Krav Maga Japan 沖縄 (ライカム)","Krav Maga Japan Okinawa (Rycom)",["krav-maga"],"Krav Maga (chain)","gym","北中城村","北中城村字ライカム640",web="https://fitsearch.jp/group/kravmaga/okinawa",ver="B",src=["directory"],src_date="2026"),
 L("kyudo-federation","沖縄県弓道連盟","Okinawa Kyudo Federation",["other"],"Kyudo — governing body","organization","宜野湾市","宜野湾市嘉数2-15-25",web="https://kyudo.spoyell.okinawa/",ver="B",src=["federation-sites"],src_date="2026"),
 L("naginata-federation","沖縄県なぎなた連盟","Okinawa Naginata Federation",["other"],"Naginata — governing body","organization","西原町",addr_en="Nishihara area (secretariat)",web="https://naginata.spoyell.okinawa/",ver="B",src=["federation-sites"],src_date="2026"),
 L("jukendo-federation","沖縄県銃剣道連盟","Okinawa Jukendo Federation",["other"],"Jukendo — governing body","organization","糸満市",addr_en="Itoman area (secretariat)",contact="会長 加藤哲也",ver="B",src=["federation-sites"],src_date="2026"),
 L("wushu-federation","沖縄県武術太極拳連盟","Okinawa Wushu & Taijiquan Federation",["other"],"Wushu / Taijiquan — governing body","organization","宜野湾市",addr_en="Ginowan area (secretariat)",ver="B",src=["federation-sites"],src_date="2026"),

 # ---------- US-military MCCS program ----------
 L("mccs-martial-arts","MCCS 武道プログラム (米海兵隊)","MCCS Martial Arts Program (Marine Corps Community Services)",["karate","kobudo","bjj","kickboxing","other"],
   "Isshin-ryu, Okinawan Kenpo, kobudo, BJJ, aiki ju-jutsu, Setkudo kickboxing/Muay Thai","program","宜野湾市","Gunner's Fitness Center, Bldg 5902, Camp Foster (program office)",
   phone="098-970-3141",web="https://www.okinawa.usmc-mccs.org/recreation-fitness/sports/martial-arts",email="fitnesscenters@okinawa.usmc-mccs.org",
   hours="Fitness center Mon–Fri 07:30–16:30. Class times are in the program's yearly schedule PDF.",
   contact="Instructors incl. Tsuyoshi Uechi (Isshin-ryu), Toru Kiyan (Okinawan Kenpo), Masayoshi Umeda (Aiki Ju-Jutsu), Kiyoto Yogi (kobudo), Ivan & Arine Sakamoto, Elton Cruz, Joe Davis, Emerson Azuma (BJJ), Nobuhiro & Kana Hirahara (Setkudo)",
   visitors="Meet the instructor before class; once approved, register at the fitness-center counter. Monthly fees (2026 page): Isshin-ryu/Kenpo/Kobudo $50; Aiki Ju-Jutsu $30 child / $40 adult; Setkudo $50 child / $60 adult; BJJ $80 child / $100 adult. On-base: access requires installation authorization.",
   english="Yes.",ver="A",src=["mccs"],src_date="2026-10"),
]

ALL = KYK + SKS + KENDO_YOUTH + KENDO_GENERAL + OTHER
