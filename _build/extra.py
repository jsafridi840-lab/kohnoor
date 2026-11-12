# Extra content: route legs (Rome2rio style), trails (AllTrails style), curious places (Atlas Obscura style), seasonal pass status.
# Hours are approximate ranges in good weather. First leg starts from Islamabad.
# leg = (mode, to_en, to_ur, hmin, hmax, note_en, note_ur)
LEGS = {
 "fairy-meadows": [("car", "Raikot Bridge (KKH)", "رائےکوٹ پل", 11, 13, "Via Babusar in summer or the KKH all year", "گرمیوں میں بابوسر یا سارا سال شاہراہِ قراقرم سے"), ("jeep", "Tato / Jhel", "تتو / جھیل", 1.5, 2, "Official jeep stand only", "صرف سرکاری جیپ سٹینڈ"), ("hike", "Fairy Meadows", "فیری میڈوز", 2, 3, "Steady uphill trail", "مسلسل چڑھائی والا راستہ")],
 "mahodand": [("car", "Kalam", "کالام", 7, 8, "M-1 and Swat Expressway", "ایم-ون اور سوات ایکسپریس وے"), ("jeep", "Mahodand Lake", "مہوڈنڈ جھیل", 2, 3, "Via Ushu and Matiltan", "اوشو اور مٹلتان کے راستے")],
 "kandol-lake": [("car", "Kalam", "کالام", 7, 8, "", ""), ("jeep", "Utror trailhead", "اتروڑ ٹریل ہیڈ", 1.5, 2, "", ""), ("hike", "Kandol Lake", "کنڈول جھیل", 1, 2, "Local guide advised", "مقامی گائیڈ بہتر")],
 "daral-lake": [("car", "Bahrain", "بحرین", 6, 7, "", ""), ("hike", "Daral Lake", "درال جھیل", 16, 24, "Two to three days with camping", "کیمپنگ کے ساتھ دو تا تین دن")],
 "gabin-jabba": [("car", "Matta", "مٹہ", 5, 6, "", ""), ("jeep", "Gabin Jabba", "گبین جبہ", 1, 1.5, "", "")],
 "kumrat": [("car", "Thall", "تھل", 8, 9, "Via Chakdara and Dir", "چکدرہ اور دیر کے راستے"), ("jeep", "Kumrat forest", "کمراٹ جنگل", 1, 1.5, "", "")],
 "jahaz-banda": [("car", "Thall", "تھل", 8, 9, "", ""), ("jeep", "Jandrai", "جندرئی", 1, 1.5, "", ""), ("hike", "Jahaz Banda", "جہاز بانڈہ", 3, 4, "Horses available", "گھوڑے دستیاب")],
 "katora-lake": [("car", "Thall", "تھل", 8, 9, "", ""), ("jeep", "Jandrai", "جندرئی", 1, 1.5, "", ""), ("hike", "Jahaz Banda (night stop)", "جہاز بانڈہ (رات قیام)", 3, 4, "", ""), ("hike", "Katora Lake", "کٹورہ جھیل", 3, 4, "Guide advised", "گائیڈ بہتر")],
 "naran": [("car", "Naran", "ناران", 6, 7, "Hazara Motorway", "ہزارہ موٹروے"), ("jeep", "Lake Saif-ul-Malook", "جھیل سیف الملوک", 1, 1.5, "", "")],
 "shogran": [("car", "Kiwai", "کیوائی", 5, 5.5, "", ""), ("jeep", "Shogran", "شوگران", 0.75, 1, "", ""), ("jeep", "Siri Paye", "سری پائے", 1, 1, "", "")],
 "deosai": [("car", "Skardu", "سکردو", 18, 20, "Or fly (see below)", "یا پرواز (نیچے دیکھیں)"), ("jeep", "Deosai Plains", "دیوسائی", 2, 3, "Via Sadpara Lake", "صدپارہ جھیل کے راستے")],
 "naltar": [("car", "Gilgit", "گلگت", 12, 14, "", ""), ("car", "Nomal", "نومل", 0.5, 0.75, "", ""), ("jeep", "Naltar Bala", "نلتر بالا", 1.5, 2, "", "")],
 "astore-rama": [("car", "Astore", "استور", 12, 13, "KKH via Jaglot", "جگلوٹ کے راستے شاہراہِ قراقرم"), ("jeep", "Rama meadows", "راما چراگاہ", 1, 1, "", "")],
 "ratti-gali": [("car", "Dowarian", "دواریاں", 8, 9, "Via Muzaffarabad", "مظفرآباد کے راستے"), ("jeep", "Base camp", "بیس کیمپ", 2, 3, "", ""), ("hike", "Ratti Gali Lake", "رتی گلی جھیل", 1, 1.5, "", "")],
 "arang-kel": [("car", "Kel", "کیل", 9, 10, "", ""), ("cable", "Across the river", "دریا پار", 0.2, 0.2, "Small cable car", "چھوٹی کیبل کار"), ("hike", "Arang Kel", "اڑنگ کیل", 0.75, 1, "Steep path", "کھڑی چڑھائی")],
 "taobat": [("car", "Kel", "کیل", 9, 10, "", ""), ("jeep", "Taobat", "تاؤبٹ", 1.5, 2, "", "")],
 "leepa": [("car", "Muzaffarabad", "مظفرآباد", 3, 3.5, "", ""), ("jeep", "Leepa Valley", "لیپہ ویلی", 3.5, 4.5, "Over the Reshian pass", "ریشیاں درے سے")],
 "dudipatsar": [("car", "Besal", "بیسل", 7, 8, "Past Naran", "ناران سے آگے"), ("hike", "Dudipatsar Lake", "دودی پت سر جھیل", 5, 7, "Long day, guide advised", "لمبا دن، گائیڈ بہتر")],
 "shandur": [("car", "Chitral", "چترال", 9, 10, "Lowari Tunnel", "لواری ٹنل"), ("jeep", "Shandur Pass", "شندور پاس", 4, 5, "Via Booni and Mastuj", "بونی اور مستوج کے راستے")],
 "sarfaranga": [("car", "Skardu", "سکردو", 18, 20, "Or fly", "یا پرواز"), ("jeep", "Sarfaranga dunes", "سرفرنگا ٹیلے", 0.5, 0.75, "", "")],
 "utror-gabral": [("car", "Kalam", "کالام", 7, 8, "", ""), ("jeep", "Utror", "اتروڑ", 1, 1, "", "")],
 "ushu-matiltan": [("car", "Kalam", "کالام", 7, 8, "", ""), ("jeep", "Matiltan", "مٹلتان", 0.3, 0.7, "", "")],
 "kalash": [("car", "Chitral", "چترال", 9, 10, "", ""), ("jeep", "Bumburet", "بمبوریت", 1.5, 2, "Narrow road", "تنگ سڑک")],
 "passu-khunjerab": [("car", "Karimabad (Hunza)", "کریم آباد (ہنزہ)", 14, 16, "", ""), ("car", "Passu", "پسو", 1, 1.25, "Through Attabad tunnels", "عطا آباد سرنگوں سے"), ("car", "Khunjerab Pass", "خنجراب پاس", 2.5, 3, "", "")],
 "babusar": [("car", "Naran", "ناران", 6, 7, "", ""), ("car", "Babusar Top", "بابوسر ٹاپ", 2, 2.5, "Summer only", "صرف گرمیوں میں")],
 "miranjani": [("car", "Nathia Gali", "نتھیا گلی", 2.5, 3, "", ""), ("hike", "Miranjani summit", "میرانجانی چوٹی", 2, 3, "", "")],
 "malam-jabba": [("car", "Malam Jabba", "مالم جبہ", 5, 6, "Via Mingora and Manglawar", "مینگورہ اور منگلور کے راستے")],
}
# Road time from the airport town to the place, for places with a 'fly' field.
FLY_ROAD = {"skardu": 0, "deosai": 2.5, "shigar": 1, "khaplu": 3, "kachura": 0.7, "sarfaranga": 0.6, "manthoka": 2.5,
            "gilgit": 0, "hunza": 2.2, "attabad": 2.7, "passu-khunjerab": 3.5, "naltar": 2, "phander": 5.5, "khalti": 4, "borith": 3.6,
            "chitral": 0, "kalash": 1.8, "garam-chashma": 1.5, "shandur": 5}
FLY_FROM = {"Skardu": ("Skardu", "سکردو"), "Gilgit": ("Gilgit", "گلگت"), "Chitral": ("Chitral", "چترال")}

# AllTrails-style trails. Distances one way unless stated; figures are approximate.
TRAILS = [
 {"id": "pipeline-track", "place": "nathia-gali", "name": "Pipeline Track: Dunga Gali to Ayubia", "ur": "پائپ لائن ٹریک: ڈونگا گلی تا ایوبیہ", "diff": 1, "km": 4, "gain": 50, "hrs": "1.5–2", "type": "One way", "start": 2400, "top": 2450, "season": "All year (icy in winter)",
  "desc": "A flat, shaded path along an old water pipeline through oak and pine forest. The easiest family walk in the Galiyat.", "dur": "ایک قدیم پانی کی پائپ لائن کے ساتھ بلوط اور دیودار کے جنگل میں ہموار، سایہ دار راستہ۔ گلیات کی سب سے آسان خاندانی سیر۔"},
 {"id": "mushkpuri", "place": "nathia-gali", "name": "Mushkpuri Top", "ur": "مکشپوری ٹاپ", "diff": 2, "km": 4, "gain": 300, "hrs": "1.5–2.5", "type": "Out and back", "start": 2500, "top": 2800, "season": "Apr–Nov",
  "desc": "A steady forest climb from Dunga Gali to open grassy slopes with wide views over the Galiyat and, on clear days, the Pir Panjal.", "dur": "ڈونگا گلی سے جنگل میں مسلسل چڑھائی، کھلی گھاس والی ڈھلوانوں تک جہاں سے گلیات کے وسیع نظارے ملتے ہیں۔"},
 {"id": "miranjani", "place": "miranjani", "name": "Miranjani summit", "ur": "میرانجانی چوٹی", "diff": 2, "km": 4.5, "gain": 500, "hrs": "2–3 up", "type": "Out and back", "start": 2500, "top": 2990, "season": "Apr–Nov",
  "desc": "The highest point of the Galiyat. A forest trail that ends on a rocky top with views towards Nanga Parbat on clear mornings.", "dur": "گلیات کا بلند ترین مقام۔ جنگل کا راستہ جو پتھریلی چوٹی پر ختم ہوتا ہے جہاں سے صاف صبحوں میں نانگا پربت نظر آتا ہے۔"},
 {"id": "fairy-meadows-trek", "place": "fairy-meadows", "name": "Tato to Fairy Meadows", "ur": "تتو سے فیری میڈوز", "diff": 2, "km": 5, "gain": 650, "hrs": "2–3", "type": "One way", "start": 2650, "top": 3300, "season": "May–Oct",
  "desc": "The classic walk from the jeep road end up through pine forest to the meadow facing Nanga Parbat. Horses can carry bags.", "dur": "جیپ روڈ کے اختتام سے دیودار کے جنگل میں نانگا پربت کے سامنے والی چراگاہ تک کلاسیک راستہ۔ سامان کے لیے گھوڑے مل جاتے ہیں۔"},
 {"id": "beyal-viewpoint", "place": "fairy-meadows", "name": "Beyal Camp and Nanga Parbat viewpoint", "ur": "بیال کیمپ اور نانگا پربت ویو پوائنٹ", "diff": 3, "km": 7, "gain": 600, "hrs": "3–4 up", "type": "Out and back", "start": 3300, "top": 3900, "season": "Jun–Sep",
  "desc": "From Fairy Meadows on to Beyal and the moraine viewpoint under the Raikot glacier. Big views of the north face.", "dur": "فیری میڈوز سے آگے بیال اور رائےکوٹ گلیشیئر تلے ویو پوائنٹ تک۔ شمالی رخ کے شاندار نظارے۔"},
 {"id": "jahaz-banda-trek", "place": "jahaz-banda", "name": "Jandrai to Jahaz Banda", "ur": "جندرئی سے جہاز بانڈہ", "diff": 2, "km": 8, "gain": 800, "hrs": "3–4", "type": "One way", "start": 2300, "top": 3100, "season": "Jun–Sep",
  "desc": "Up through forest and past a waterfall to a huge flat meadow with herders' huts. Usually done with a night on the meadow.", "dur": "جنگل اور آبشار سے گزرتا ہوا چرواہوں کی جھونپڑیوں والی وسیع ہموار چراگاہ تک۔ عموماً چراگاہ پر رات گزاری جاتی ہے۔"},
 {"id": "katora-trek", "place": "katora-lake", "name": "Jahaz Banda to Katora Lake", "ur": "جہاز بانڈہ سے کٹورہ جھیل", "diff": 3, "km": 7, "gain": 450, "hrs": "3–4", "type": "Out and back", "start": 3100, "top": 3550, "season": "Jul–Sep",
  "desc": "Up the valley over boulders and snow patches to a turquoise bowl-shaped lake under snowfields. Unmarked, go with a guide.", "dur": "وادی میں پتھروں اور برف کے ٹکڑوں سے گزر کر برفانی میدانوں تلے فیروزی پیالہ نما جھیل تک۔ راستہ نشان زدہ نہیں، گائیڈ کے ساتھ جائیں۔"},
 {"id": "kandol-trek", "place": "kandol-lake", "name": "Kandol Lake hike", "ur": "کنڈول جھیل ہائیک", "diff": 2, "km": 3, "gain": 350, "hrs": "1–2", "type": "Out and back", "start": 2550, "top": 2900, "season": "Jun–Sep",
  "desc": "A short climb from the jeep point above Utror to a deep blue lake below pine ridges. Spin Khwar lake is a longer add-on.", "dur": "اتروڑ کے اوپر جیپ پوائنٹ سے دیودار کی چوٹیوں تلے گہری نیلی جھیل تک مختصر چڑھائی۔"},
 {"id": "ratti-gali-trek", "place": "ratti-gali", "name": "Ratti Gali base camp to the lake", "ur": "رتی گلی بیس کیمپ سے جھیل", "diff": 2, "km": 2.5, "gain": 250, "hrs": "1–1.5", "type": "Out and back", "start": 3450, "top": 3700, "season": "Jul–Sep",
  "desc": "Through flower meadows from the jeep base camp to the glacial lake. Short but high, so walk slowly.", "dur": "جیپ بیس کیمپ سے پھولوں بھری چراگاہوں سے گلیشیائی جھیل تک۔ مختصر مگر بلند، اس لیے آہستہ چلیں۔"},
 {"id": "arang-kel-trek", "place": "arang-kel", "name": "Kel to Arang Kel", "ur": "کیل سے اڑنگ کیل", "diff": 2, "km": 2, "gain": 350, "hrs": "0.75–1", "type": "One way", "start": 2050, "top": 2400, "season": "May–Oct",
  "desc": "After the cable car across the river, a steep path climbs to the wooden village on its meadow.", "dur": "دریا پار کیبل کار کے بعد کھڑی پگڈنڈی چراگاہ پر لکڑی کے گاؤں تک جاتی ہے۔"},
 {"id": "rama-lake", "place": "astore-rama", "name": "Rama meadows to Rama Lake", "ur": "راما چراگاہ سے راما جھیل", "diff": 2, "km": 4, "gain": 250, "hrs": "1.5–2", "type": "Out and back", "start": 3300, "top": 3550, "season": "Jun–Sep",
  "desc": "From the forest meadows above Astore to a glacial lake under the Nanga Parbat massif.", "dur": "استور کے اوپر جنگلاتی چراگاہوں سے نانگا پربت کے سلسلے تلے گلیشیائی جھیل تک۔"},
 {"id": "dudipatsar-trek", "place": "dudipatsar", "name": "Besal to Dudipatsar Lake", "ur": "بیسل سے دودی پت سر جھیل", "diff": 3, "km": 12, "gain": 900, "hrs": "5–7", "type": "One way", "start": 3000, "top": 3800, "season": "Jul–Sep",
  "desc": "A long, high day up a side valley into the national park to a snow-ringed lake. Camp near the lake and return next day.", "dur": "نیشنل پارک میں ایک ذیلی وادی میں لمبا، بلند دن، برف سے گھری جھیل تک۔ جھیل کے قریب کیمپ کر کے اگلے دن واپسی۔"},
 {"id": "daral-trek", "place": "daral-lake", "name": "Bahrain to Daral Lake", "ur": "بحرین سے درال جھیل", "diff": 3, "km": 25, "gain": 2000, "hrs": "2–3 days", "type": "Out and back", "start": 1400, "top": 3400, "season": "Jul–Sep",
  "desc": "A multi-day trek up the Daral stream through forest and herders' huts to a remote high lake. For fit, experienced hikers only.", "dur": "درال ندی کے ساتھ جنگل اور چرواہوں کی جھونپڑیوں سے دور دراز بلند جھیل تک کئی دن کا ٹریک۔ صرف مضبوط اور تجربہ کار ہائیکرز کے لیے۔"},
 {"id": "hussaini-borith", "place": "borith", "name": "Hussaini bridge and Borith Lake", "ur": "حسینی پل اور بورت جھیل", "diff": 1, "km": 3, "gain": 150, "hrs": "1–1.5", "type": "Loop", "start": 2500, "top": 2650, "season": "Apr–Oct",
  "desc": "Cross the famous suspension bridge, then walk up to the small lake with views of the Passu Cones.", "dur": "مشہور معلق پل پار کریں، پھر پسو کونز کے نظاروں والی چھوٹی جھیل تک پیدل جائیں۔"},
 {"id": "eagles-nest", "place": "hunza", "name": "Duikar to Eagle's Nest", "ur": "دوئیکر سے ایگلز نیسٹ", "diff": 1, "km": 1, "gain": 100, "hrs": "0.5", "type": "Out and back", "start": 2900, "top": 3000, "season": "Apr–Oct",
  "desc": "A short walk above Duikar village to rocks with a 360° view over Hunza, Rakaposhi and Ultar. Best at sunrise or sunset.", "dur": "دوئیکر گاؤں کے اوپر چٹانوں تک مختصر سیر جہاں سے ہنزہ، راکاپوشی اور التر کا 360 درجے نظارہ ملتا ہے۔"},
 {"id": "udegram-castle", "place": "udegram", "name": "Raja Gira's castle climb", "ur": "راجہ گیرا قلعے کی چڑھائی", "diff": 2, "km": 1.5, "gain": 250, "hrs": "0.75", "type": "Out and back", "start": 1000, "top": 1250, "season": "Oct–Apr best",
  "desc": "A steep climb past the Ghaznavid mosque to castle ruins with views over the Swat valley.", "dur": "غزنوی مسجد سے گزر کر قلعے کے کھنڈرات تک کھڑی چڑھائی، جہاں سے وادیٔ سوات نظر آتی ہے۔"},
]
DIFF = {1: ("Easy", "آسان", "#2E7D57"), 2: ("Moderate", "درمیانہ", "#B7860F"), 3: ("Hard", "مشکل", "#B24A3B")}

# Atlas Obscura-style curious places.
WONDERS = [
 {"place": "chilas", "title": "Ten thousand carvings on the Indus", "ur": "دریائے سندھ پر دس ہزار نقوش", "text": "Rocks along the KKH near Chilas carry tens of thousands of carvings and inscriptions: stupas, ibex, hunters and scripts left by traders and pilgrims over two thousand years.", "tur": "چلاس کے قریب شاہراہِ قراقرم کے ساتھ پتھروں پر دسیوں ہزار نقوش اور کتبے ہیں: سٹوپا، آئبیکس، شکاری اور دو ہزار سال میں تاجروں اور زائرین کے لکھے رسم الخط۔"},
 {"place": "attabad", "title": "A lake born from a landslide", "ur": "لینڈ سلائیڈ سے پیدا ہونے والی جھیل", "text": "In 2010 a mountainside collapsed and dammed the Hunza River. The turquoise lake that formed drowned villages and part of the highway, and is now one of Pakistan's most photographed views.", "tur": "2010 میں ایک پہاڑ گرا اور دریائے ہنزہ رک گیا۔ بننے والی فیروزی جھیل نے گاؤں اور شاہراہ کا حصہ ڈبو دیا، اور اب یہ پاکستان کے سب سے زیادہ تصویر کھینچے جانے والے نظاروں میں سے ہے۔"},
 {"place": "borith", "title": "The bridge that sways", "ur": "جھولتا ہوا پل", "text": "Hussaini's suspension bridge of planks and cables hangs over the Hunza River with gaps between the boards. Villagers have rebuilt it themselves several times.", "tur": "حسینی کا تختوں اور تاروں سے بنا معلق پل دریائے ہنزہ پر لٹکا ہے اور تختوں کے بیچ خلا ہیں۔ گاؤں والوں نے اسے خود کئی بار دوبارہ بنایا۔"},
 {"place": "sarfaranga", "title": "A desert at 2,200 metres", "ur": "2,200 میٹر بلندی پر صحرا", "text": "White sand dunes sit beneath snow peaks near Skardu, one of the highest cold deserts on earth, where jeeps race in summer.", "tur": "سکردو کے قریب برفانی چوٹیوں تلے سفید ریت کے ٹیلے، دنیا کے بلند ترین سرد صحراؤں میں سے ایک، جہاں گرمیوں میں جیپیں دوڑتی ہیں۔"},
 {"place": "deosai", "title": "Land of giants and bears", "ur": "دیوؤں اور ریچھوں کی سرزمین", "text": "Local legend says giants lived on this vast plateau. Today it is home to the rare Himalayan brown bear, protected since 1993.", "tur": "مقامی روایت کہتی ہے کہ اس وسیع سطح مرتفع پر دیو رہتے تھے۔ آج یہ نایاب ہمالیائی بھورے ریچھ کا گھر ہے جو 1993 سے محفوظ ہے۔"},
 {"place": "jahanabad-buddha", "title": "The Buddha who got his face back", "ur": "وہ بدھا جسے چہرہ واپس ملا", "text": "Militants blasted the face of this 7th-century rock Buddha in 2007. Italian conservators restored it in 2016 using 3D scans and careful stonework.", "tur": "2007 میں شدت پسندوں نے ساتویں صدی کے اس چٹانی بدھا کا چہرہ دھماکے سے اڑا دیا۔ اطالوی ماہرین نے 2016 میں تھری ڈی سکین اور احتیاطی پتھر کے کام سے اسے بحال کیا۔"},
 {"place": "shandur", "title": "Polo on the roof of the world", "ur": "دنیا کی چھت پر پولو", "text": "At about 3,700 m, Shandur hosts a fierce polo match between Chitral and Gilgit every July, often called the highest polo ground in the world.", "tur": "تقریباً 3,700 میٹر پر شندور میں ہر جولائی چترال اور گلگت کے درمیان زبردست پولو میچ ہوتا ہے، جسے اکثر دنیا کا بلند ترین پولو گراؤنڈ کہا جاتا ہے۔"},
 {"place": "sharda", "title": "The lost university of Kashmir", "ur": "کشمیر کی گمشدہ درسگاہ", "text": "On a hill above the Neelum stand the ruins of Sharda Peeth, a famous seat of learning that gave its name to the old Sharada script.", "tur": "نیلم کے اوپر پہاڑی پر شاردا پیٹھ کے کھنڈر ہیں، علم کا مشہور مرکز جس کے نام پر پرانا شاردا رسم الخط ہے۔"},
 {"place": "kalash", "title": "A culture unlike any other", "ur": "سب سے الگ ثقافت", "text": "In three valleys near Chitral the Kalash keep their own faith, language and seasonal festivals, one of the smallest and oldest living cultures in the region.", "tur": "چترال کے قریب تین وادیوں میں کیلاش اپنا مذہب، زبان اور موسمی تہوار سنبھالے ہوئے ہیں، خطے کی سب سے چھوٹی اور قدیم زندہ ثقافتوں میں سے ایک۔"},
 {"place": "passu-khunjerab", "title": "A border at 4,690 metres", "ur": "4,690 میٹر پر سرحد", "text": "Khunjerab Pass on the China border is one of the highest paved border crossings in the world, with snow leopards and marmots in the national park around it.", "tur": "چین کی سرحد پر خنجراب پاس دنیا کی بلند ترین پکی سرحدی گزرگاہوں میں سے ایک ہے، جس کے گرد نیشنل پارک میں برفانی چیتے اور مارموٹ رہتے ہیں۔"},
 {"place": "butkara", "title": "A stupa inside a stupa", "ur": "سٹوپا کے اندر سٹوپا", "text": "Butkara's great stupa was rebuilt around itself several times over a thousand years, so the oldest one, perhaps from Ashoka's time, lies hidden inside.", "tur": "بٹکڑہ کا بڑا سٹوپا ہزار سال میں کئی بار اپنے ہی گرد دوبارہ بنایا گیا، اس لیے سب سے پرانا، شاید اشوک کے دور کا، اس کے اندر چھپا ہے۔"},
 {"place": "naltar", "title": "The seven-colour lake", "ur": "ست رنگی جھیل", "text": "Satrangi Lake in Naltar shows bands of green, blue and turquoise depending on depth and light, among pine forest high above Gilgit.", "tur": "نلتر کی ست رنگی جھیل گہرائی اور روشنی کے مطابق سبز، نیلے اور فیروزی رنگ دکھاتی ہے، گلگت سے بہت اوپر دیودار کے جنگل میں۔"},
]

# Seasonal status of key passes and roads: months usually open (1) or closed (0). Not live data.
PASSES = [
 {"name": "Babusar Pass", "ur": "بابوسر پاس", "place": "babusar", "open": "000001111100", "alt": 4170, "note": "Kaghan to Chilas", "nur": "کاغان سے چلاس"},
 {"name": "Khunjerab Pass", "ur": "خنجراب پاس", "place": "passu-khunjerab", "open": "000111111110", "alt": 4690, "note": "Hunza to China border", "nur": "ہنزہ سے چین کی سرحد"},
 {"name": "Deosai Plains road", "ur": "دیوسائی روڈ", "place": "deosai", "open": "000000111000", "alt": 4100, "note": "Skardu to Astore", "nur": "سکردو سے استور"},
 {"name": "Shandur Pass", "ur": "شندور پاس", "place": "shandur", "open": "000001111000", "alt": 3700, "note": "Chitral to Ghizer", "nur": "چترال سے غذر"},
 {"name": "Lowari Tunnel", "ur": "لواری ٹنل", "place": "chitral", "open": "111111111111", "alt": 2400, "note": "Dir to Chitral, open all year", "nur": "دیر سے چترال، سارا سال کھلی"},
 {"name": "Karakoram Highway", "ur": "شاہراہِ قراقرم", "place": "gilgit", "open": "111111111111", "alt": 1500, "note": "Open all year; landslides after rain", "nur": "سارا سال کھلی؛ بارش کے بعد لینڈ سلائیڈ"},
 {"name": "Naran–Kaghan road beyond Naran", "ur": "ناران سے آگے سڑک", "place": "naran", "open": "000011111100", "alt": 2400, "note": "Snow closes it in winter", "nur": "سردیوں میں برف سے بند"},
 {"name": "Kalam–Mahodand track", "ur": "کالام–مہوڈنڈ راستہ", "place": "mahodand", "open": "000001111000", "alt": 2865, "note": "Jeep track", "nur": "جیپ کا راستہ"},
]
