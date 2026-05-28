# ✈️ Cheaper Flight Prices Hub — Multilingual pSEO Flight Comparison Platform

Cheaper Flight Prices Hub is a programmatic SEO platform targeting budget and price-anchored flight search queries across 7 languages. It generates 7,425 keyword-optimized landing pages across 99 global destinations and 75 multilingual intent patterns, powered by a Python build engine and deployed via GitHub Pages.

---

## 🏗 Architecture

| File | Role |
|------|------|
| `build.py` | Master build engine — generates all pages, sitemap, robots.txt, and handles git |
| `index.html` | Homepage — 7 language sections, each showing 12 sample destinations in native language |
| `.github/workflows/vulture-heartbeat.yml` | Runs `build.py` every 4 hours and on demand |
| `sitemap.xml` | Auto-generated sitemap with all page URLs |
| `robots.txt` | Search engine crawl directives |
| `.nojekyll` | Prevents GitHub Pages from running Jekyll on HTML files |

---

## 📈 SEO Strategy

**Scale:** 99 destinations × 75 intents (7 languages) = **7,425 landing pages**

**Why multilingual budget keywords?**
Price-anchored flight queries like "cheap flights to London", "vuelos baratos a París", "vols pas chers pour Tokyo" and "billigflüge nach Dubai" are among the highest-volume travel searches globally. By targeting these queries in 7 languages, this site reaches travellers searching in their native language on Google across Europe, Latin America, and beyond — an audience not covered by any of the other sites in this network.

**7 languages × intent counts:**

| Language | Intents | Sample slug pattern |
|----------|---------|-------------------|
| English | 15 | `cheap-flights-to-{d}`, `budget-flights-to-{d}`, `flights-under-500-to-{d}` |
| Spanish | 10 | `vuelos-baratos-a-{d}`, `vuelos-economicos-a-{d}`, `pasajes-baratos-a-{d}` |
| French | 10 | `vols-pas-chers-pour-{d}`, `billets-avion-pas-cher-{d}`, `vols-promo-pour-{d}` |
| German | 10 | `guenstige-fluege-nach-{d}`, `billigfluege-nach-{d}`, `flugangebote-nach-{d}` |
| Portuguese | 10 | `passagens-baratas-para-{d}`, `voos-baratos-para-{d}`, `ofertas-de-voos-para-{d}` |
| Italian | 10 | `voli-economici-per-{d}`, `voli-low-cost-per-{d}`, `offerte-voli-per-{d}` |
| Dutch | 10 | `goedkope-vluchten-naar-{d}`, `budget-vluchten-naar-{d}`, `kortingsvluchten-naar-{d}` |

**Language-native pages:** Every page has the correct HTML `lang` attribute (en/es/fr/de/pt/it/nl), a native-language meta description, native CTA text, and native trust signals — so Google serves the right language version to the right searcher.

**Freshness signal:** Every page includes a sync timestamp updated on each build run.

**Affiliate:** Skyscanner via LinkConnector (ID: 21885)

---

## 🚀 Deployment

### Requirements
- GitHub Pages enabled on `main` branch
- Actions permissions set to **Read and write**

### Running the build manually
1. Go to **Actions** tab
2. Select **CheaperFlights Vulture-Heartbeat**
3. Click **Run workflow**

### Scheduled runs
- **Page sync:** Every 4 hours

---

## 📂 Page Structure

All pages follow this URL pattern:

```
/{intent-slug}-1.html
```

Examples by language:
- `/cheap-flights-to-london-1.html` (English)
- `/vuelos-baratos-a-paris-1.html` (Spanish)
- `/vols-pas-chers-pour-tokyo-1.html` (French)
- `/guenstige-fluege-nach-berlin-1.html` (German)
- `/passagens-baratas-para-bali-1.html` (Portuguese)
- `/voli-economici-per-rome-1.html` (Italian)
- `/goedkope-vluchten-naar-amsterdam-1.html` (Dutch)

---

## 🌍 Destinations (99)

London, Paris, Tokyo, Dubai, Singapore, Rome, Bangkok, Istanbul, Seoul, Barcelona, Amsterdam, Madrid, Berlin, Lisbon, Athens, Prague, Vienna, Munich, Zurich, Brussels, Stockholm, Oslo, Helsinki, Copenhagen, Dublin, Edinburgh, Manchester, Warsaw, Budapest, Reykjavik, Nice, Florence, Venice, Santorini, Ibiza, Bali, Sydney, Melbourne, Auckland, Osaka, Hong Kong, Shanghai, Taipei, Manila, Kuala Lumpur, Hanoi, Phuket, Mumbai, Delhi, Maldives, New York, Los Angeles, Miami, Chicago, San Francisco, Toronto, Vancouver, Cancún, Mexico City, Buenos Aires, São Paulo, Rio de Janeiro, Lima, Bogotá, Cape Town, Nairobi, Marrakech, Cairo, Johannesburg, Lagos, Doha, Abu Dhabi, Seychelles, Zanzibar, Mauritius, Fiji, Tahiti, Bora Bora, Queenstown, Colombo, Tel Aviv, Porto, Seville, Naples, Palermo, Casablanca, Accra, Fukuoka, Busan, Jakarta, Ho Chi Minh City, Cusco, Santiago, Mykonos, Dubrovnik, Valletta, Tallinn, Riga, Kraków

---

## 🛠 Adding Destinations, Languages, or Intents

**Add a destination:** Edit the `DESTINATIONS` list in `build.py` — add a tuple of `(City Name, IATA, Country, Base Price)`.

**Add an intent:** Edit the `INTENTS` list in `build.py` — add a tuple of `("{slug-tpl}", "{Label tpl}", "lang_code")`. The `{d}` and `{D}` placeholders are replaced automatically.

**Add a language:** Add intent tuples with your new language code, then add the language code to `LANG_LABELS`, `LANG_META`, `CTA_TEXT`, `BOOK_TEXT`, and `TRUST_TEXT` dictionaries.

Re-run the build to generate all new pages automatically.

---

## 🔗 Related Sites

| Site | URL | Focus |
|------|-----|-------|
| FlightHub | brightlane.github.io/skyscannerflighthub/ | Flights TO global cities (20,942 pages) |
| SkyHub | brightlane.github.io/SkyscannerHub/ | Flights FROM US cities (2,673 pages) |
| SkyScanner | brightlane.github.io/SkyScanner/ | US→global route pairs (49,372 pages) |
| SkyDeals | brightlane.github.io/SkyDeals/ | Non-US→global route pairs (55,472 pages) |
| CheaperFlights | brightlane.github.io/Cheaper--Flight-Prices-Hub/ | Budget/multilingual (7,425 pages) |

---

*Built and maintained with GitHub Actions. Powered by Skyscanner.*
