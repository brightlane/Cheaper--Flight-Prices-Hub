import os, subprocess, datetime, sys, re

BASE_URL  = "https://brightlane.github.io/Cheaper--Flight-Prices-Hub/"
AFFILIATE = "http://convert.ctypy.com/aff_c?offer_id=29465&aff_id=21885"

# 100 global destinations
DESTINATIONS = [
    ("London",          "LHR", "UK",             "$298"),
    ("Paris",           "CDG", "France",          "$312"),
    ("Tokyo",           "NRT", "Japan",           "$499"),
    ("Dubai",           "DXB", "UAE",             "$421"),
    ("Singapore",       "SIN", "Singapore",       "$412"),
    ("Rome",            "FCO", "Italy",           "$341"),
    ("Bangkok",         "BKK", "Thailand",        "$329"),
    ("Istanbul",        "IST", "Turkey",          "$387"),
    ("Seoul",           "ICN", "South Korea",     "$511"),
    ("Barcelona",       "BCN", "Spain",           "$287"),
    ("Amsterdam",       "AMS", "Netherlands",     "$279"),
    ("Madrid",          "MAD", "Spain",           "$302"),
    ("Berlin",          "BER", "Germany",         "$276"),
    ("Lisbon",          "LIS", "Portugal",        "$298"),
    ("Athens",          "ATH", "Greece",          "$344"),
    ("Prague",          "PRG", "Czech Republic",  "$267"),
    ("Vienna",          "VIE", "Austria",         "$289"),
    ("Munich",          "MUC", "Germany",         "$294"),
    ("Zurich",          "ZRH", "Switzerland",     "$381"),
    ("Brussels",        "BRU", "Belgium",         "$271"),
    ("Stockholm",       "ARN", "Sweden",          "$318"),
    ("Oslo",            "OSL", "Norway",          "$342"),
    ("Helsinki",        "HEL", "Finland",         "$329"),
    ("Copenhagen",      "CPH", "Denmark",         "$337"),
    ("Dublin",          "DUB", "Ireland",         "$261"),
    ("Edinburgh",       "EDI", "UK",              "$249"),
    ("Manchester",      "MAN", "UK",              "$239"),
    ("Warsaw",          "WAW", "Poland",          "$251"),
    ("Budapest",        "BUD", "Hungary",         "$259"),
    ("Reykjavik",       "KEF", "Iceland",         "$421"),
    ("Nice",            "NCE", "France",          "$309"),
    ("Florence",        "FLR", "Italy",           "$328"),
    ("Venice",          "VCE", "Italy",           "$334"),
    ("Santorini",       "JTR", "Greece",          "$612"),
    ("Ibiza",           "IBZ", "Spain",           "$341"),
    ("Bali",            "DPS", "Indonesia",       "$387"),
    ("Sydney",          "SYD", "Australia",       "$749"),
    ("Melbourne",       "MEL", "Australia",       "$731"),
    ("Auckland",        "AKL", "New Zealand",     "$812"),
    ("Osaka",           "KIX", "Japan",           "$487"),
    ("Hong Kong",       "HKG", "HK",              "$387"),
    ("Shanghai",        "PVG", "China",           "$521"),
    ("Taipei",          "TPE", "Taiwan",          "$489"),
    ("Manila",          "MNL", "Philippines",     "$461"),
    ("Kuala Lumpur",    "KUL", "Malaysia",        "$331"),
    ("Hanoi",           "HAN", "Vietnam",         "$337"),
    ("Phuket",          "HKT", "Thailand",        "$348"),
    ("Mumbai",          "BOM", "India",           "$341"),
    ("Delhi",           "DEL", "India",           "$328"),
    ("Maldives",        "MLE", "Maldives",        "$649"),
    ("New York",        "JFK", "USA",             "$299"),
    ("Los Angeles",     "LAX", "USA",             "$399"),
    ("Miami",           "MIA", "USA",             "$349"),
    ("Chicago",         "ORD", "USA",             "$349"),
    ("San Francisco",   "SFO", "USA",             "$449"),
    ("Toronto",         "YYZ", "Canada",          "$241"),
    ("Vancouver",       "YVR", "Canada",          "$319"),
    ("Cancun",          "CUN", "Mexico",          "$289"),
    ("Mexico City",     "MEX", "Mexico",          "$319"),
    ("Buenos Aires",    "EZE", "Argentina",       "$641"),
    ("Sao Paulo",       "GRU", "Brazil",          "$611"),
    ("Rio de Janeiro",  "GIG", "Brazil",          "$624"),
    ("Lima",            "LIM", "Peru",            "$698"),
    ("Bogota",          "BOG", "Colombia",        "$671"),
    ("Cape Town",       "CPT", "South Africa",    "$698"),
    ("Nairobi",         "NBO", "Kenya",           "$721"),
    ("Marrakech",       "RAK", "Morocco",         "$412"),
    ("Cairo",           "CAI", "Egypt",           "$489"),
    ("Johannesburg",    "JNB", "South Africa",    "$749"),
    ("Lagos",           "LOS", "Nigeria",         "$849"),
    ("Doha",            "DOH", "Qatar",           "$389"),
    ("Abu Dhabi",       "AUH", "UAE",             "$411"),
    ("Seychelles",      "SEZ", "Seychelles",      "$1,189"),
    ("Zanzibar",        "ZNZ", "Tanzania",        "$891"),
    ("Mauritius",       "MRU", "Mauritius",       "$921"),
    ("Fiji",            "NAN", "Fiji",            "$871"),
    ("Tahiti",          "PPT", "Fr Polynesia",    "$921"),
    ("Bora Bora",       "BOB", "Fr Polynesia",    "$949"),
    ("Queenstown",      "ZQN", "New Zealand",     "$1,012"),
    ("Colombo",         "CMB", "Sri Lanka",       "$421"),
    ("Tel Aviv",        "TLV", "Israel",          "$512"),
    ("Porto",           "OPO", "Portugal",        "$286"),
    ("Seville",         "SVQ", "Spain",           "$293"),
    ("Naples",          "NAP", "Italy",           "$319"),
    ("Palermo",         "PMO", "Italy",           "$329"),
    ("Casablanca",      "CMN", "Morocco",         "$489"),
    ("Accra",           "ACC", "Ghana",           "$821"),
    ("Fukuoka",         "FUK", "Japan",           "$511"),
    ("Busan",           "PUS", "South Korea",     "$521"),
    ("Jakarta",         "CGK", "Indonesia",       "$471"),
    ("Ho Chi Minh City","SGN", "Vietnam",         "$341"),
    ("Cusco",           "CUZ", "Peru",            "$741"),
    ("Santiago",        "SCL", "Chile",           "$821"),
    ("Mykonos",         "JMK", "Greece",          "$598"),
    ("Dubrovnik",       "DBV", "Croatia",         "$412"),
    ("Valletta",        "MLA", "Malta",           "$389"),
    ("Tallinn",         "TLL", "Estonia",         "$298"),
    ("Riga",            "RIX", "Latvia",          "$287"),
    ("Krakow",          "KRK", "Poland",          "$261"),
]

# Multilingual intents — 7 languages × ~15 intents = 105 total
INTENTS = [
    # ── ENGLISH ──────────────────────────────────────────────────────────────
    ("cheap-flights-to-{d}",               "Cheap Flights to {D}",               "en"),
    ("cheapest-flights-to-{d}",            "Cheapest Flights to {D}",            "en"),
    ("budget-flights-to-{d}",              "Budget Flights to {D}",              "en"),
    ("low-cost-flights-to-{d}",            "Low Cost Flights to {D}",            "en"),
    ("affordable-flights-to-{d}",          "Affordable Flights to {D}",          "en"),
    ("discount-flights-to-{d}",            "Discount Flights to {D}",            "en"),
    ("bargain-flights-to-{d}",             "Bargain Flights to {D}",             "en"),
    ("flights-under-500-to-{d}",           "Flights Under $500 to {D}",          "en"),
    ("flights-under-300-to-{d}",           "Flights Under $300 to {D}",          "en"),
    ("cheapest-airfare-to-{d}",            "Cheapest Airfare to {D}",            "en"),
    ("best-flight-deals-to-{d}",           "Best Flight Deals to {D}",           "en"),
    ("flight-sale-to-{d}",                 "Flight Sale to {D}",                 "en"),
    ("last-minute-cheap-flights-to-{d}",   "Last Minute Cheap Flights to {D}",   "en"),
    ("cheapest-time-to-fly-to-{d}",        "Cheapest Time to Fly to {D}",        "en"),
    ("how-to-find-cheap-flights-to-{d}",   "How to Find Cheap Flights to {D}",   "en"),
    # ── SPANISH ──────────────────────────────────────────────────────────────
    ("vuelos-baratos-a-{d}",               "Vuelos Baratos a {D}",               "es"),
    ("vuelos-economicos-a-{d}",            "Vuelos Económicos a {D}",            "es"),
    ("vuelos-baratos-hacia-{d}",           "Vuelos Baratos Hacia {D}",           "es"),
    ("vuelos-low-cost-a-{d}",              "Vuelos Low Cost a {D}",              "es"),
    ("ofertas-de-vuelos-a-{d}",            "Ofertas de Vuelos a {D}",            "es"),
    ("vuelos-en-oferta-a-{d}",             "Vuelos en Oferta a {D}",             "es"),
    ("pasajes-baratos-a-{d}",              "Pasajes Baratos a {D}",              "es"),
    ("como-encontrar-vuelos-baratos-a-{d}","Cómo Encontrar Vuelos Baratos a {D}","es"),
    ("vuelos-con-descuento-a-{d}",         "Vuelos con Descuento a {D}",         "es"),
    ("billetes-baratos-a-{d}",             "Billetes Baratos a {D}",             "es"),
    # ── FRENCH ───────────────────────────────────────────────────────────────
    ("vols-pas-chers-pour-{d}",            "Vols Pas Chers pour {D}",            "fr"),
    ("vols-bon-marche-pour-{d}",           "Vols Bon Marché pour {D}",           "fr"),
    ("billets-avion-pas-cher-{d}",         "Billets Avion Pas Cher {D}",         "fr"),
    ("vols-low-cost-pour-{d}",             "Vols Low Cost pour {D}",             "fr"),
    ("vols-promo-pour-{d}",                "Vols Promo pour {D}",                "fr"),
    ("offres-vols-pour-{d}",               "Offres Vols pour {D}",               "fr"),
    ("vols-pas-chers-last-minute-{d}",     "Vols Pas Chers Last Minute {D}",     "fr"),
    ("comment-trouver-vols-pas-chers-{d}", "Comment Trouver Vols Pas Chers {D}", "fr"),
    ("tarifs-avion-pas-cher-{d}",          "Tarifs Avion Pas Cher {D}",          "fr"),
    ("reduction-vol-pour-{d}",             "Réduction Vol pour {D}",             "fr"),
    # ── GERMAN ───────────────────────────────────────────────────────────────
    ("guenstige-fluege-nach-{d}",          "Günstige Flüge nach {D}",            "de"),
    ("billigfluege-nach-{d}",              "Billigflüge nach {D}",               "de"),
    ("billige-fluege-nach-{d}",            "Billige Flüge nach {D}",             "de"),
    ("fluege-unter-500-nach-{d}",          "Flüge unter 500€ nach {D}",          "de"),
    ("preiswerte-fluege-nach-{d}",         "Preiswerte Flüge nach {D}",          "de"),
    ("flugangebote-nach-{d}",              "Flugangebote nach {D}",              "de"),
    ("guenstige-flugtickets-nach-{d}",     "Günstige Flugtickets nach {D}",      "de"),
    ("last-minute-fluege-nach-{d}",        "Last Minute Flüge nach {D}",         "de"),
    ("wie-findet-man-guenstige-fluege-{d}","Günstige Flüge Finden nach {D}",     "de"),
    ("flugschaeppchen-nach-{d}",           "Flugschnäppchen nach {D}",           "de"),
    # ── PORTUGUESE ───────────────────────────────────────────────────────────
    ("passagens-baratas-para-{d}",         "Passagens Baratas para {D}",         "pt"),
    ("voos-baratos-para-{d}",              "Voos Baratos para {D}",              "pt"),
    ("voos-economicos-para-{d}",           "Voos Econômicos para {D}",           "pt"),
    ("passagens-aereas-baratas-{d}",       "Passagens Aéreas Baratas {D}",       "pt"),
    ("ofertas-de-voos-para-{d}",           "Ofertas de Voos para {D}",           "pt"),
    ("voos-promocionais-para-{d}",         "Voos Promocionais para {D}",         "pt"),
    ("como-achar-passagens-baratas-{d}",   "Como Achar Passagens Baratas {D}",   "pt"),
    ("bilhetes-baratos-para-{d}",          "Bilhetes Baratos para {D}",          "pt"),
    ("voos-com-desconto-para-{d}",         "Voos com Desconto para {D}",         "pt"),
    ("passagem-aerea-barata-{d}",          "Passagem Aérea Barata {D}",          "pt"),
    # ── ITALIAN ──────────────────────────────────────────────────────────────
    ("voli-economici-per-{d}",             "Voli Economici per {D}",             "it"),
    ("voli-low-cost-per-{d}",              "Voli Low Cost per {D}",              "it"),
    ("voli-convenienti-per-{d}",           "Voli Convenienti per {D}",           "it"),
    ("biglietti-aerei-economici-{d}",      "Biglietti Aerei Economici {D}",      "it"),
    ("offerte-voli-per-{d}",               "Offerte Voli per {D}",               "it"),
    ("come-trovare-voli-economici-{d}",    "Come Trovare Voli Economici {D}",    "it"),
    ("voli-scontati-per-{d}",              "Voli Scontati per {D}",              "it"),
    ("tariffe-basse-voli-{d}",             "Tariffe Basse Voli {D}",             "it"),
    ("voli-last-minute-economici-{d}",     "Voli Last Minute Economici {D}",     "it"),
    ("promozioni-voli-per-{d}",            "Promozioni Voli per {D}",            "it"),
    # ── DUTCH ────────────────────────────────────────────────────────────────
    ("goedkope-vluchten-naar-{d}",         "Goedkope Vluchten naar {D}",         "nl"),
    ("budget-vluchten-naar-{d}",           "Budget Vluchten naar {D}",           "nl"),
    ("goedkope-tickets-naar-{d}",          "Goedkope Tickets naar {D}",          "nl"),
    ("voordelige-vluchten-naar-{d}",       "Voordelige Vluchten naar {D}",       "nl"),
    ("vluchten-aanbieding-naar-{d}",       "Vluchten Aanbieding naar {D}",       "nl"),
    ("goedkoopste-vlucht-naar-{d}",        "Goedkoopste Vlucht naar {D}",        "nl"),
    ("last-minute-vluchten-naar-{d}",      "Last Minute Vluchten naar {D}",      "nl"),
    ("kortingsvluchten-naar-{d}",          "Kortingsvluchten naar {D}",          "nl"),
    ("lowcost-vluchten-naar-{d}",          "Lowcost Vluchten naar {D}",          "nl"),
    ("hoe-goedkoop-vliegen-naar-{d}",      "Hoe Goedkoop Vliegen naar {D}",      "nl"),
]

LANG_LABELS = {
    "en": "English",
    "es": "Español",
    "fr": "Français",
    "de": "Deutsch",
    "pt": "Português",
    "it": "Italiano",
    "nl": "Nederlands",
}

LANG_META = {
    "en": {"desc": "Find {label} to {D}. Compare 1,200+ airlines in real time. From {price} roundtrip. No booking fees.", "html_lang": "en"},
    "es": {"desc": "Encuentra {label} a {D}. Compara más de 1.200 aerolíneas en tiempo real. Desde {price} ida y vuelta.", "html_lang": "es"},
    "fr": {"desc": "Trouvez {label} pour {D}. Comparez plus de 1.200 compagnies aériennes en temps réel. Dès {price} aller-retour.", "html_lang": "fr"},
    "de": {"desc": "Finden Sie {label} nach {D}. Vergleichen Sie über 1.200 Airlines in Echtzeit. Ab {price} Hin- und Rückflug.", "html_lang": "de"},
    "pt": {"desc": "Encontre {label} para {D}. Compare mais de 1.200 companhias aéreas em tempo real. A partir de {price} ida e volta.", "html_lang": "pt"},
    "it": {"desc": "Trova {label} per {D}. Confronta oltre 1.200 compagnie aeree in tempo reale. Da {price} andata e ritorno.", "html_lang": "it"},
    "nl": {"desc": "Vind {label} naar {D}. Vergelijk meer dan 1.200 luchtvaartmaatschappijen in realtime. Vanaf {price} retour.", "html_lang": "nl"},
}

CTA_TEXT = {
    "en": "Search Flights →",
    "es": "Buscar Vuelos →",
    "fr": "Rechercher des Vols →",
    "de": "Flüge Suchen →",
    "pt": "Buscar Voos →",
    "it": "Cerca Voli →",
    "nl": "Vluchten Zoeken →",
}

BOOK_TEXT = {
    "en": "Compare & Book",
    "es": "Comparar y Reservar",
    "fr": "Comparer et Réserver",
    "de": "Vergleichen & Buchen",
    "pt": "Comparar e Reservar",
    "it": "Confronta e Prenota",
    "nl": "Vergelijk & Boek",
}

TRUST_TEXT = {
    "en": ["No booking fees", "1,200+ airlines compared", "Real-time prices", "Book direct with airline"],
    "es": ["Sin tarifas de reserva", "Más de 1.200 aerolíneas", "Precios en tiempo real", "Reserva directo"],
    "fr": ["Sans frais de réservation", "1.200+ compagnies comparées", "Prix en temps réel", "Réservez directement"],
    "de": ["Keine Buchungsgebühren", "1.200+ Airlines verglichen", "Echtzeit-Preise", "Direkt beim Anbieter buchen"],
    "pt": ["Sem taxas de reserva", "Mais de 1.200 companhias", "Preços em tempo real", "Reserve direto"],
    "it": ["Nessuna commissione", "Oltre 1.200 compagnie", "Prezzi in tempo reale", "Prenota direttamente"],
    "nl": ["Geen boekingskosten", "1.200+ airlines vergeleken", "Realtime prijzen", "Boek direct bij airline"],
}

def slug(s):
    replacements = {'á':'a','é':'e','í':'i','ó':'o','ú':'u','ã':'a','â':'a','ê':'e','ô':'o',
                    'ñ':'n','ü':'u','ç':'c','ä':'a','ö':'o','Á':'a','É':'e','Í':'i','Ó':'o',
                    'Ú':'u','ü':'u','ó':'o','é':'e','à':'a','è':'e','ù':'u','â':'a','ê':'e',
                    'î':'i','û':'u','ô':'o','ë':'e','ï':'i'}
    result = s
    for k, v in replacements.items():
        result = result.replace(k, v)
    return re.sub(r'[^a-z0-9-]', '', result.lower().replace(' ', '-').replace('/', '-'))

def make_slug(tpl, d_name):
    return tpl.format(d=slug(d_name))

def make_label(tpl, d_name):
    return tpl.format(D=d_name)

def build_page(d_name, d_code, d_country, d_price,
               i_slug, i_label, lang, date_str, sync_ts):
    html_lang = LANG_META[lang]["html_lang"]
    meta_desc = LANG_META[lang]["desc"].format(label=i_label, D=d_name, price=d_price)
    canonical = f"{BASE_URL}{i_slug}-1.html"
    cta = CTA_TEXT[lang]
    book = BOOK_TEXT[lang]
    trust = TRUST_TEXT[lang]

    # Related destinations (same lang, different dest)
    others = [d for d in DESTINATIONS if d[0] != d_name][:8]
    related_html = "\n          ".join(
        f'<a href="{make_slug(INTENTS[0][0], r[0])}-1.html">{make_label(INTENTS[0][1], r[0])}</a>'
        for r in others
    )

    # Alt intents same dest same lang
    alt = [(make_slug(it, d_name), make_label(il, d_name))
           for it, il, lg in INTENTS if lg == lang and make_slug(it, d_name) != i_slug][:5]
    alt_html = "\n          ".join(
        f'<a href="{s}-1.html">{l}</a>' for s, l in alt
    )

    lang_badge = LANG_LABELS[lang]

    return f"""<!DOCTYPE html>
<html lang="{html_lang}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{i_label} | from {d_price} | Cheaper Flight Prices Hub</title>
<meta name="description" content="{meta_desc}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="theme-color" content="#0a1628">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:title" content="{i_label} from {d_price}">
<meta property="og:description" content="{meta_desc}">
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"TravelAgency","name":"Cheaper Flight Prices Hub","url":"{BASE_URL}","description":"{i_label} — compare 1,200+ airlines worldwide."}}
</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=DM+Sans:wght@300;400;500&display=swap" rel="stylesheet">
<style>
:root{{--navy:#0a1628;--sky:#38b6ff;--sky-pale:#a8dcff;--gold:#f5c842;--white:#fff;--green:#28c76f;}}
*{{margin:0;padding:0;box-sizing:border-box;}}html{{scroll-behavior:smooth;}}
body{{font-family:'DM Sans',sans-serif;background:var(--navy);color:var(--white);overflow-x:hidden;}}
nav{{position:fixed;top:0;left:0;right:0;z-index:100;display:flex;align-items:center;justify-content:space-between;padding:18px 40px;background:rgba(10,22,40,0.92);backdrop-filter:blur(16px);border-bottom:1px solid rgba(56,182,255,0.1);}}
.logo{{font-family:'Syne',sans-serif;font-size:19px;font-weight:800;color:var(--white);text-decoration:none;letter-spacing:-0.3px;}}.logo span{{color:var(--sky);}}
.nav-right{{display:flex;align-items:center;gap:20px;}}
.nav-home{{color:rgba(255,255,255,0.6);text-decoration:none;font-size:14px;transition:color 0.2s;}}.nav-home:hover{{color:var(--white);}}
.nav-cta{{background:var(--sky);color:var(--navy);padding:10px 22px;border-radius:10px;font-weight:500;font-size:14px;text-decoration:none;}}.nav-cta:hover{{opacity:0.85;}}
.hero{{min-height:55vh;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:130px 24px 70px;position:relative;background:radial-gradient(ellipse 80% 60% at 50% 0%,rgba(56,182,255,0.16) 0%,transparent 70%),var(--navy);}}
.hero::before{{content:'';position:absolute;inset:0;background-image:radial-gradient(1px 1px at 15% 25%,rgba(255,255,255,0.35) 0%,transparent 100%),radial-gradient(1px 1px at 75% 18%,rgba(255,255,255,0.28) 0%,transparent 100%),radial-gradient(1.5px 1.5px at 50% 65%,rgba(255,255,255,0.2) 0%,transparent 100%);pointer-events:none;}}
.breadcrumb{{display:flex;align-items:center;gap:8px;font-size:12px;color:rgba(255,255,255,0.4);margin-bottom:20px;flex-wrap:wrap;justify-content:center;}}
.breadcrumb a{{color:var(--sky);text-decoration:none;}}.breadcrumb span{{color:rgba(255,255,255,0.2);}}
.lang-badge{{display:inline-flex;align-items:center;gap:8px;background:rgba(56,182,255,0.1);border:1px solid rgba(56,182,255,0.25);padding:8px 16px;border-radius:999px;font-size:13px;font-weight:600;color:var(--sky-pale);margin-bottom:20px;}}
.live-dot{{width:7px;height:7px;background:var(--green);border-radius:50%;animation:livePulse 2s infinite;display:inline-block;flex-shrink:0;}}
@keyframes livePulse{{0%,100%{{opacity:1;transform:scale(1);}}50%{{opacity:0.4;transform:scale(0.7);}}}}
.hero h1{{font-family:'Syne',sans-serif;font-size:clamp(28px,5vw,60px);font-weight:800;letter-spacing:-2px;line-height:1.05;max-width:820px;margin:0 auto 18px;}}
.hero h1 em{{font-style:normal;color:var(--sky);}}
.hero-sub{{font-size:clamp(15px,1.8vw,18px);color:rgba(255,255,255,0.55);max-width:540px;margin:0 auto 44px;line-height:1.7;font-weight:300;}}
.price-cta-row{{display:flex;align-items:center;justify-content:center;gap:32px;flex-wrap:wrap;}}
.price-block{{text-align:center;}}
.price-label{{font-size:11px;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:var(--sky);margin-bottom:6px;}}
.price-num{{font-family:'Syne',sans-serif;font-size:clamp(42px,6vw,70px);font-weight:800;color:var(--white);letter-spacing:-3px;line-height:1;}}
.price-sub{{font-size:13px;color:rgba(255,255,255,0.4);margin-top:4px;}}
.price-divider{{width:1px;height:52px;background:rgba(56,182,255,0.2);}}
.hero-cta{{display:inline-flex;align-items:center;gap:10px;background:var(--sky);color:var(--navy);text-decoration:none;padding:16px 30px;border-radius:14px;font-family:'Syne',sans-serif;font-size:16px;font-weight:700;transition:background 0.2s,transform 0.15s;box-shadow:0 0 40px rgba(56,182,255,0.22);white-space:nowrap;}}.hero-cta:hover{{background:#5cc8ff;transform:translateY(-2px);}}
.status-strip{{background:rgba(56,182,255,0.05);border-top:1px solid rgba(56,182,255,0.1);border-bottom:1px solid rgba(56,182,255,0.1);padding:14px 24px;text-align:center;}}
.status-inner{{display:flex;align-items:center;justify-content:center;gap:20px;flex-wrap:wrap;font-size:12px;color:rgba(255,255,255,0.4);font-weight:500;}}
.status-inner strong{{color:rgba(255,255,255,0.7);}}.sep{{color:rgba(255,255,255,0.15);}}
.price-strip{{display:grid;grid-template-columns:repeat(4,1fr);gap:1px;background:rgba(56,182,255,0.08);}}
.ps-cell{{background:var(--navy);padding:26px 20px;text-align:center;}}
.ps-cell .pn{{font-family:'Syne',sans-serif;font-size:26px;font-weight:800;color:var(--sky);letter-spacing:-1px;margin-bottom:4px;}}
.ps-cell .pl{{font-size:12px;color:rgba(255,255,255,0.4);text-transform:uppercase;letter-spacing:1px;}}
.main{{max-width:1100px;margin:0 auto;padding:70px 24px;}}
.two-col{{display:grid;grid-template-columns:1fr 340px;gap:28px;align-items:start;}}
.info-card{{background:rgba(255,255,255,0.04);border:1px solid rgba(56,182,255,0.12);border-radius:20px;padding:34px;margin-bottom:20px;}}
.section-tag{{font-size:11px;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:var(--sky);margin-bottom:12px;display:block;}}
.info-card h2{{font-family:'Syne',sans-serif;font-size:22px;font-weight:800;letter-spacing:-0.5px;margin-bottom:14px;}}
.info-card p{{color:rgba(255,255,255,0.6);font-size:15px;line-height:1.8;font-weight:300;margin-bottom:12px;}}
.info-card p:last-child{{margin-bottom:0;}}
.info-card strong{{color:var(--white);font-weight:500;}}
.tips-grid{{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:14px;}}
.tip-item{{background:rgba(56,182,255,0.05);border:1px solid rgba(56,182,255,0.1);border-radius:12px;padding:16px;}}
.tip-icon{{font-size:18px;margin-bottom:6px;}}
.tip-text{{font-size:13px;color:rgba(255,255,255,0.5);line-height:1.5;}}
.sidebar{{display:flex;flex-direction:column;gap:18px;}}
.book-card{{background:rgba(56,182,255,0.07);border:1px solid rgba(56,182,255,0.2);border-radius:20px;padding:26px;text-align:center;}}
.bc-label{{font-size:11px;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:var(--sky);margin-bottom:8px;}}
.bc-dest{{font-family:'Syne',sans-serif;font-size:22px;font-weight:800;margin-bottom:2px;}}
.bc-code{{font-size:13px;color:rgba(255,255,255,0.35);margin-bottom:18px;}}
.bc-price{{font-family:'Syne',sans-serif;font-size:50px;font-weight:800;color:var(--sky);letter-spacing:-2px;line-height:1;margin-bottom:4px;}}
.bc-note{{font-size:12px;color:rgba(255,255,255,0.35);margin-bottom:22px;}}
.big-book-btn{{display:block;background:var(--sky);color:var(--navy);text-decoration:none;padding:15px;border-radius:12px;font-family:'Syne',sans-serif;font-size:15px;font-weight:700;transition:background 0.2s,transform 0.15s;margin-bottom:14px;}}.big-book-btn:hover{{background:#5cc8ff;transform:translateY(-2px);}}
.trust-items{{display:flex;flex-direction:column;gap:7px;}}
.trust-item{{display:flex;align-items:center;gap:8px;font-size:12px;color:rgba(255,255,255,0.4);}}.trust-item::before{{content:'✓';color:var(--sky);font-weight:700;}}
.alt-card{{background:rgba(255,255,255,0.03);border:1px solid rgba(56,182,255,0.1);border-radius:18px;padding:22px;}}
.alt-card h4{{font-family:'Syne',sans-serif;font-size:14px;font-weight:700;margin-bottom:12px;}}
.alt-card a{{display:block;font-size:13px;color:rgba(255,255,255,0.5);text-decoration:none;padding:7px 0;border-bottom:1px solid rgba(255,255,255,0.05);line-height:1.4;}}.alt-card a:last-child{{border-bottom:none;}}.alt-card a:hover{{color:var(--sky);}}
.related-section{{margin-top:18px;}}
.related-section h3{{font-family:'Syne',sans-serif;font-size:18px;font-weight:800;letter-spacing:-0.3px;margin-bottom:14px;}}
.route-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(190px,1fr));gap:8px;}}
.route-grid a{{display:block;background:rgba(255,255,255,0.04);border:1px solid rgba(56,182,255,0.1);border-radius:10px;padding:12px 14px;text-decoration:none;color:rgba(255,255,255,0.65);font-size:12px;font-weight:500;transition:background 0.2s,color 0.2s;}}.route-grid a:hover{{background:rgba(56,182,255,0.08);color:var(--white);}}
.bottom-cta{{margin-top:18px;background:rgba(56,182,255,0.06);border:1px solid rgba(56,182,255,0.18);border-radius:22px;padding:54px 36px;text-align:center;}}
.bottom-cta h2{{font-family:'Syne',sans-serif;font-size:clamp(22px,3vw,36px);font-weight:800;letter-spacing:-1px;margin-bottom:10px;}}
.bottom-cta p{{color:rgba(255,255,255,0.5);font-size:15px;font-weight:300;line-height:1.7;max-width:440px;margin:0 auto 28px;}}
.cta-btn{{display:inline-flex;align-items:center;gap:10px;background:var(--sky);color:var(--navy);text-decoration:none;padding:15px 30px;border-radius:14px;font-family:'Syne',sans-serif;font-size:15px;font-weight:700;transition:background 0.2s,transform 0.15s;}}.cta-btn:hover{{background:#5cc8ff;transform:translateY(-2px);}}
footer{{border-top:1px solid rgba(255,255,255,0.06);padding:42px 24px;}}
.footer-inner{{max-width:1100px;margin:0 auto;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:14px;}}
.footer-logo{{font-family:'Syne',sans-serif;font-size:16px;font-weight:800;color:var(--white);text-decoration:none;}}.footer-logo span{{color:var(--sky);}}
.footer-copy{{color:rgba(255,255,255,0.3);font-size:12px;}}
@media(max-width:860px){{nav{{padding:16px 20px;}}.two-col{{grid-template-columns:1fr;}}.sidebar{{order:-1;}}.price-cta-row{{gap:20px;}}.price-divider{{display:none;}}.price-strip{{grid-template-columns:repeat(2,1fr);}}.tips-grid{{grid-template-columns:1fr;}}.bottom-cta{{padding:40px 22px;}}.footer-inner{{flex-direction:column;text-align:center;}}}}
</style>
</head>
<body>
<nav>
  <a href="{BASE_URL}" class="logo">Cheaper<span>Flights</span></a>
  <div class="nav-right">
    <a href="{BASE_URL}" class="nav-home">← Home</a>
    <a href="{AFFILIATE}" class="nav-cta" target="_blank" rel="sponsored noopener noreferrer">{cta}</a>
  </div>
</nav>
<section class="hero">
  <div class="breadcrumb"><a href="{BASE_URL}">Home</a><span>›</span><span>{i_label}</span></div>
  <div class="lang-badge"><span class="live-dot"></span>{lang_badge} · Live Pricing</div>
  <h1><em>{i_label}</em></h1>
  <p class="hero-sub">Compare 1,200+ airlines in real time. Updated every hour. No booking fees.</p>
  <div class="price-cta-row">
    <div class="price-block">
      <div class="price-label">Lowest fare</div>
      <div class="price-num">{d_price}</div>
      <div class="price-sub">roundtrip · taxes included</div>
    </div>
    <div class="price-divider"></div>
    <a href="{AFFILIATE}" class="hero-cta" target="_blank" rel="sponsored noopener noreferrer">
      <svg width="18" height="18" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg>
      {cta}
    </a>
  </div>
</section>
<div class="status-strip">
  <div class="status-inner">
    <span><span class="live-dot" style="margin-right:6px"></span><strong>LIVE</strong></span>
    <span class="sep">|</span>
    <span>Updated: <strong>{date_str}</strong></span>
    <span class="sep">|</span>
    <span>Destination: <strong>{d_name} ({d_code})</strong></span>
    <span class="sep">|</span>
    <span>Language: <strong>{lang_badge}</strong></span>
  </div>
</div>
<div class="price-strip">
  <div class="ps-cell"><div class="pn">{d_price}</div><div class="pl">Lowest fare</div></div>
  <div class="ps-cell"><div class="pn">{d_code}</div><div class="pl">Airport code</div></div>
  <div class="ps-cell"><div class="pn">{d_country}</div><div class="pl">Country</div></div>
  <div class="ps-cell"><div class="pn">1,200+</div><div class="pl">Airlines compared</div></div>
</div>
<div class="main">
  <div class="two-col">
    <div>
      <div class="info-card">
        <span class="section-tag">{i_label}</span>
        <h2>{i_label} — Live Market</h2>
        <p>The current lowest tracked fare to <strong>{d_name} ({d_code})</strong> is <strong>{d_price} roundtrip</strong> including all taxes. Prices on this route change multiple times daily — set an alert to be notified when fares drop.</p>
        <p>To find the best price: use flexible date search to see a full month of fares at once. Shifting your travel dates by 1-2 days can save $50-200 on flights to {d_name}. Compare all airlines — prices vary significantly between carriers on this route.</p>
        <p><strong>Tip:</strong> Book 4-8 weeks ahead for the best international fares to {d_name}. Tuesday and Wednesday departures are typically the cheapest days to fly.</p>
        <div class="tips-grid">
          <div class="tip-item"><div class="tip-icon">📅</div><div class="tip-text">Book 4-8 weeks ahead for best fares to {d_name}</div></div>
          <div class="tip-item"><div class="tip-icon">🌙</div><div class="tip-text">Fly Tuesday or Wednesday — cheapest departure days</div></div>
          <div class="tip-item"><div class="tip-icon">🔔</div><div class="tip-text">Set a price alert — fares to {d_name} drop frequently</div></div>
          <div class="tip-item"><div class="tip-icon">✈</div><div class="tip-text">Compare all airlines — prices vary significantly</div></div>
        </div>
      </div>
      <div class="related-section">
        <h3>More cheap flights</h3>
        <div class="route-grid">{related_html}</div>
      </div>
      <div class="bottom-cta">
        <h2>{i_label}</h2>
        <p>Compare every airline in one search. Find your lowest price right now.</p>
        <a href="{AFFILIATE}" class="cta-btn" target="_blank" rel="sponsored noopener noreferrer">
          <svg width="18" height="18" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg>
          {cta}
        </a>
      </div>
    </div>
    <div class="sidebar">
      <div class="book-card">
        <div class="bc-label">Best fare tracked</div>
        <div class="bc-dest">{d_name}</div>
        <div class="bc-code">{d_code} · {d_country}</div>
        <div class="bc-price">{d_price}</div>
        <div class="bc-note">roundtrip · all taxes included</div>
        <a href="{AFFILIATE}" class="big-book-btn" target="_blank" rel="sponsored noopener noreferrer">{book} →</a>
        <div class="trust-items">
          {"".join(f'<div class="trust-item">{t}</div>' for t in trust)}
        </div>
      </div>
      <div class="alt-card">
        <h4>More searches for {d_name}</h4>
        {alt_html}
      </div>
    </div>
  </div>
</div>
<footer>
  <div class="footer-inner">
    <a href="{BASE_URL}" class="footer-logo">Cheaper<span>Flights</span></a>
    <div class="footer-copy">© 2026 Cheaper Flight Prices Hub · Powered by Skyscanner</div>
  </div>
</footer>
</body>
</html>
<!-- sync:{sync_ts} -->"""

# ── MAIN ──────────────────────────────────────────────────────────────────────
now      = datetime.datetime.utcnow()
DATE_STR = now.strftime("%a, %d %b %Y %H:%M UTC")
SYNC     = now.isoformat()
count    = 0
sitemap_urls = [BASE_URL]

total = len(DESTINATIONS) * len(INTENTS)
print(f"Building {len(DESTINATIONS)} destinations × {len(INTENTS)} intents ({len(set(i[2] for i in INTENTS))} languages) = {total:,} pages...")

for d_name, d_code, d_country, d_price in DESTINATIONS:
    for i_tpl, l_tpl, lang in INTENTS:
        i_slug  = make_slug(i_tpl, d_name)
        i_label = make_label(l_tpl, d_name)
        filename = f"{i_slug}-1.html"
        try:
            html = build_page(d_name, d_code, d_country, d_price,
                              i_slug, i_label, lang, DATE_STR, SYNC)
            with open(filename, "w", encoding="utf-8") as f:
                f.write(html)
            count += 1
        except Exception as e:
            print(f"  ERROR {filename}: {e}")
        sitemap_urls.append(f"{BASE_URL}{filename}")

print(f"✅ {count:,} pages written")

# Sitemap
iso = now.strftime("%Y-%m-%d")
sm  = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
sm += f'  <url><loc>{BASE_URL}</loc><changefreq>daily</changefreq><priority>1.0</priority><lastmod>{iso}</lastmod></url>\n'
for url in sitemap_urls[1:]:
    sm += f'  <url><loc>{url}</loc><changefreq>daily</changefreq><priority>0.8</priority><lastmod>{iso}</lastmod></url>\n'
sm += '</urlset>\n'
with open("sitemap.xml","w",encoding="utf-8") as f: f.write(sm)
print(f"✅ sitemap.xml — {len(sitemap_urls):,} URLs")

with open("robots.txt","w",encoding="utf-8") as f:
    f.write(f"User-agent: *\nAllow: /\nDisallow: /generator.html\nDisallow: /seo-engine-onefile.html\nDisallow: /generator.js\nDisallow: /social-post-generator.js\nDisallow: /vulture_titan_320k.py\nDisallow: /build.py\nDisallow: /llms.txt\nDisallow: /travel-network-map.txt\nCrawl-delay: 1\nSitemap: {BASE_URL}sitemap.xml\n")
print("✅ robots.txt")

with open(".nojekyll","w") as f: f.write("")
print("✅ .nojekyll")

def run(cmd):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if r.stdout.strip(): print(r.stdout.strip())
    return r.returncode

print("\n── Git ──")
run("git add -A")
n = int(subprocess.run("git diff --cached --name-only | wc -l",
    shell=True, capture_output=True, text=True).stdout.strip())
print(f"Staged: {n:,} files")
if n == 0:
    print("Nothing to commit"); sys.exit(0)
run(f'git commit -m "vulture sync {SYNC}"')
import time
for i in range(1, 6):
    print(f"Push attempt {i}...")
    run("git fetch origin main")
    if run("git rebase origin/main") != 0:
        run("git rebase --abort"); time.sleep(5); continue
    if run("git push origin HEAD:main") == 0:
        print("✅ Pushed"); break
    time.sleep(5)
else:
    print("❌ Push failed"); sys.exit(1)
