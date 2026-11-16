# Privacy policy and contact pages (English + Urdu). Called from build.py.
from datetime import date

UPDATED = "16 November 2026"
UPDATED_UR = "16 نومبر 2026"
SOCIAL = [("Facebook", "https://www.facebook.com/profile.php?id=61596627986405"), ("Pinterest", "https://www.pinterest.com/kohnoorguide/")]


def social_links(sep=""):
    return sep.join(f'<a href="{u}" rel="noopener me" target="_blank">{n}</a>' for n, u in SOCIAL)


def build_legal(B):
    e, page, hero, CONTACT = B.e, B.page, B.hero, B.CONTACT
    mail = CONTACT.get("email", "")

    # ---------- Privacy (EN) ----------
    body = hero('<img src="/img/passu-khunjerab.jpg" alt="">', "Privacy", "Privacy policy", "رازداری کی پالیسی", f"Last updated {UPDATED}.", short=True)
    body += f'''<div class="wrap"><div class="layout"><div class="prose">
<p class="lead">KohNoor (kohnoor.pages.dev) is a free travel guide to Northern Pakistan. This page explains what information is collected when you use the site, why, and the choices you have. We keep it as small as we can.</p>
<h2>What we collect</h2>
<ul>
<li><b>Usage statistics.</b> We use Google Analytics (through Google Tag Manager) and Cloudflare Web Analytics to see which pages are read and how people find the site. These tools record things like pages visited, device and browser type, approximate country and the page that sent you. Cloudflare Web Analytics does not use cookies. Google Analytics uses cookies only as allowed by your choice in the cookie banner.</li>
<li><b>Road updates, reviews and photos you send.</b> If you submit a road report, review or photo, we store what you type or upload, the name you give (or "Traveller"), the place and the date. Nothing is published until we approve it. To stop spam we keep a one-way hash of your IP address, not the address itself.</li>
<li><b>Emails you send us.</b> If you write to us, we keep your message and email address only to reply and to handle business listings.</li>
</ul>
<p>We do not ask for your name, phone number or account to read the guide, we do not sell personal information, and we do not run advertising on the site at the moment.</p>
<h2>Cookies and storage on your device</h2>
<ul>
<li><b>Consent choice.</b> Your cookie choice is saved in your browser so we do not ask again.</li>
<li><b>Analytics cookies.</b> Set by Google Analytics only when allowed. Visitors in Europe and the UK see everything switched off until they agree. You can change your choice at any time with <a href="#" onclick="siteConsent.open();return false">Cookie settings</a> at the bottom of every page.</li>
<li><b>Offline data.</b> Weather, your packing list and pages you open are saved on your own device so the guide works without signal. This stays on your phone and is not sent to us. Clearing your browser data removes it.</li>
</ul>
<h2>Services we rely on</h2>
<ul>
<li><b>Cloudflare</b> hosts the site and stores submitted reports and photos.</li>
<li><b>Google</b> (Tag Manager and Analytics) for usage statistics.</li>
<li><b>Open-Meteo</b> provides weather forecasts. Your browser asks it for the weather at the place you are viewing, not at your location.</li>
<li><b>OpenTopoMap and unpkg</b> serve the map tiles and map code on map pages.</li>
</ul>
<p>Each of these services may see your IP address when your browser loads something from them, under their own privacy policies.</p>
<h2>How long we keep things</h2>
<p>Analytics data is kept for up to 14 months. Approved reports and photos stay on the site while they are useful; rejected ones are deleted. Emails are kept as long as we need them to reply or manage a listing.</p>
<h2>Your choices and rights</h2>
<p>You can refuse analytics cookies, use the site without submitting anything, and ask us to show, correct or delete anything you sent us. Write to <a href="mailto:{mail}?subject=KohNoor%20privacy">{e(mail)}</a> and we will reply within 30 days.</p>
<h2>Children</h2>
<p>KohNoor is a general travel guide and is not aimed at children under 13. We do not knowingly collect information from them.</p>
<h2>Changes</h2>
<p>If we change how we handle information, for example if we add advertising, we will update this page and the date at the top.</p>
</div>
<aside><div class="sticky"><div class="card-box"><h3>Questions?</h3><p style="margin:0 0 10px">Email us about privacy or anything else on the site.</p><p><a class="btn" href="/contact/">Contact KohNoor</a></p></div></div></aside></div></div>'''
    page("/privacy/", "Privacy policy", "How KohNoor handles your information: analytics, cookies, offline storage, traveller reports and your choices.", body, active="/privacy/", over=True)

    # ---------- Privacy (UR) ----------
    body = hero('<img src="/img/passu-khunjerab.jpg" alt="">', "رازداری", "رازداری کی پالیسی", "", f"آخری تبدیلی: {UPDATED_UR}", short=True)
    body += f'''<div class="wrap"><div class="layout"><div class="prose">
<p class="lead">کوہِ نور شمالی پاکستان کا مفت سفری رہنما ہے۔ اس صفحے پر بتایا گیا ہے کہ سائٹ استعمال کرتے وقت کون سی معلومات جمع ہوتی ہیں، کیوں، اور آپ کے پاس کیا اختیار ہے۔</p>
<h2>ہم کیا جمع کرتے ہیں</h2>
<ul>
<li><b>استعمال کے اعداد و شمار۔</b> ہم گوگل اینالیٹکس اور کلاؤڈ فلیئر ویب اینالیٹکس سے دیکھتے ہیں کہ کون سے صفحات پڑھے جاتے ہیں۔ ان میں دیکھے گئے صفحات، ڈیوائس اور براؤزر، اندازاً ملک اور آپ کہاں سے آئے، شامل ہوتے ہیں۔ گوگل اینالیٹکس کی کوکیز صرف آپ کی اجازت کے مطابق لگتی ہیں۔</li>
<li><b>آپ کی بھیجی گئی سڑک کی خبریں، ریویو اور تصاویر۔</b> ہم آپ کا لکھا ہوا متن یا تصویر، دیا گیا نام، جگہ اور تاریخ محفوظ کرتے ہیں۔ منظوری سے پہلے کچھ شائع نہیں ہوتا۔ اسپام روکنے کے لیے ہم آئی پی ایڈریس کا صرف ایک خفیہ ہیش رکھتے ہیں، اصل ایڈریس نہیں۔</li>
<li><b>آپ کی ای میل۔</b> اگر آپ ہمیں لکھیں تو پیغام اور ای میل صرف جواب دینے کے لیے رکھی جاتی ہے۔</li>
</ul>
<p>رہنما پڑھنے کے لیے نام، فون یا اکاؤنٹ نہیں چاہیے۔ ہم ذاتی معلومات فروخت نہیں کرتے اور فی الحال سائٹ پر اشتہارات نہیں ہیں۔</p>
<h2>کوکیز اور آپ کے فون پر محفوظ ڈیٹا</h2>
<ul>
<li>آپ کی کوکی کی پسند براؤزر میں محفوظ ہوتی ہے۔ آپ ہر صفحے کے نیچے <a href="#" onclick="siteConsent.open();return false">کوکی کی ترتیبات</a> سے اسے کبھی بھی بدل سکتے ہیں۔</li>
<li>موسم، سامان کی فہرست اور کھولے گئے صفحات آپ کے اپنے فون پر محفوظ ہوتے ہیں تاکہ سگنل کے بغیر بھی رہنما چلے۔ یہ ہمیں نہیں بھیجے جاتے۔</li>
</ul>
<h2>جن سروسز پر ہم انحصار کرتے ہیں</h2>
<p>کلاؤڈ فلیئر (ہوسٹنگ اور رپورٹس)، گوگل (اینالیٹکس)، اوپن میٹیو (موسم، جگہ کے لیے نہ کہ آپ کے مقام کے لیے)، اوپن ٹوپو میپ اور unpkg (نقشے)۔</p>
<h2>آپ کے حقوق</h2>
<p>آپ اینالیٹکس کوکیز سے انکار کر سکتے ہیں، اور ہم سے اپنی بھیجی گئی کوئی بھی چیز دکھانے، درست کرنے یا ہٹانے کا کہہ سکتے ہیں۔ <a href="mailto:{mail}?subject=KohNoor%20privacy">{e(mail)}</a> پر لکھیں، ہم 30 دن میں جواب دیں گے۔</p>
<h2>تبدیلیاں</h2>
<p>اگر ہم معلومات کے استعمال کا طریقہ بدلیں، مثلاً اشتہارات شامل کریں، تو یہ صفحہ اور اوپر کی تاریخ بدل دی جائے گی۔</p>
</div>
<aside><div class="sticky"><div class="card-box"><h3>سوال؟</h3><p><a class="btn" href="/ur/contact/">رابطہ کریں</a></p></div></div></aside></div></div>'''
    page("/ur/privacy/", "رازداری کی پالیسی", "کوہِ نور آپ کی معلومات کیسے استعمال کرتا ہے: اینالیٹکس، کوکیز، آف لائن ڈیٹا اور آپ کے اختیارات۔", body, active="/ur/privacy/", over=True, lang="ur")

    # ---------- Contact (EN + UR) ----------
    for U in (False, True):
        T = (lambda a, b: b if U else a)
        pre = "/ur" if U else ""
        rows = [
            (T("Corrections and road updates", "درستی اور سڑک کی خبریں"), T("Spotted a wrong price, closed road or outdated detail? Tell us the place and what changed. You can also post a road update on any place page.", "کوئی غلط قیمت، بند سڑک یا پرانی معلومات نظر آئی؟ جگہ کا نام اور تبدیلی بتائیں۔ آپ کسی بھی جگہ کے صفحے پر سڑک کی خبر بھی دے سکتے ہیں۔"), "KohNoor%20correction"),
            (T("Hotels, jeeps, guides and camps", "ہوٹل، جیپ، گائیڈ اور کیمپ"), T("Run a business in the north? Send your name, place and a few photos to get listed.", "شمال میں کاروبار ہے؟ لسٹنگ کے لیے نام، جگہ اور چند تصاویر بھیجیں۔"), "KohNoor%20listing"),
            (T("Partnerships and press", "شراکت اور میڈیا"), T("Tourism boards, travel brands, creators and journalists are welcome to get in touch.", "سیاحتی ادارے، ٹریول برانڈز، کریئیٹرز اور صحافی رابطہ کر سکتے ہیں۔"), "KohNoor%20partnership"),
        ]
        cards = "".join(f'<div class="tier"><h3>{e(a)}</h3><p>{e(b)}</p><p><a class="btn ghost" href="mailto:{mail}?subject={s}">{T("Email us", "ای میل کریں")}</a></p></div>' for a, b, s in rows)
        body = hero('<img src="/img/hunza.jpg" alt="">', T("Contact", "رابطہ"), T("Contact KohNoor", "کوہِ نور سے رابطہ"), "" if U else "رابطہ کریں",
                    T("Questions, corrections, business listings or partnerships: we read every message.", "سوال، درستی، کاروباری لسٹنگ یا شراکت: ہم ہر پیغام پڑھتے ہیں۔"), short=True,
                    extra=f'<div class="hero-cta"><a class="btn" href="mailto:{mail}?subject=KohNoor">{e(mail)}</a></div>')
        body += f'''<section class="block"><div class="wrap"><div class="tiers">{cards}</div></div></section>
<section class="block tight"><div class="wrap"><div class="layout"><div class="prose">
<h2>{T("How to reach us", "ہم تک کیسے پہنچیں")}</h2>
<p>{T("Email", "ای میل")}: <a href="mailto:{mail}">{e(mail)}</a><br>{T("Follow", "فالو کریں")}: {social_links(" · ")}</p>
<p>{T("We usually reply within two working days. KohNoor is an information guide: we do not take hotel or transport bookings, and we cannot help with emergencies. In an emergency call Rescue 1122 or the police on 15.", "ہم عام طور پر دو کاروباری دنوں میں جواب دیتے ہیں۔ کوہِ نور معلوماتی رہنما ہے: ہم ہوٹل یا ٹرانسپورٹ کی بکنگ نہیں کرتے اور ہنگامی مدد نہیں کر سکتے۔ ہنگامی صورت میں ریسکیو 1122 یا پولیس 15 پر کال کریں۔")}</p>
<p><a href="{pre}/privacy/">{T("Privacy policy", "رازداری کی پالیسی")}</a></p>
</div></div></div></section>'''
        ld = {"@context": "https://schema.org", "@type": "ContactPage", "url": f"{B.SITE}{pre}/contact/",
              "mainEntity": {"@type": "Organization", "name": "KohNoor", "url": B.SITE + "/", "email": mail, "sameAs": [u for _, u in SOCIAL]}}
        page(f"{pre}/contact/", T("Contact KohNoor", "کوہِ نور سے رابطہ"),
             T("Contact the KohNoor Northern Pakistan travel guide for corrections, road updates, business listings and partnerships.", "درستی، سڑک کی خبروں، کاروباری لسٹنگ اور شراکت کے لیے کوہِ نور سے رابطہ کریں۔"),
             body, active=f"{pre}/contact/", over=True, jsonld=ld, lang="ur" if U else "en")
