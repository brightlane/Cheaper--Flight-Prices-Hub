import os
import random

# ==========================================
# 1. SETTINGS & CONFIGURATION
# ==========================================
TOTAL_PAGES = 320000 
OUTPUT_DIR = "usa_skyscanner_pages_320k"
DOMAIN = "https://yourtravelsite.com" 

# Base Affiliate URL - logic kept intact
BASE_AFF_URL = "PASTE_YOUR_AFFILIATE_URL_HERE"

# ==========================================
# 2. DATA MATRICES
# ==========================================
hubs = [
    ("New York", "JFK", "NY"), ("Los Angeles", "LAX", "CA"), ("Chicago", "ORD", "IL"),
    ("Houston", "IAH", "TX"), ("Phoenix", "PHX", "AZ"), ("Philadelphia", "PHL", "PA"),
    ("San Antonio", "SAT", "TX"), ("San Diego", "SAN", "CA"), ("Dallas", "DFW", "TX"),
    ("San Jose", "SJC", "CA"), ("Austin", "AUS", "TX"), ("Jacksonville", "JAX", "FL"),
    ("San Francisco", "SFO", "CA"), ("Columbus", "CMH", "OH"), ("Charlotte", "CLT", "NC"),
    ("Indianapolis", "IND", "IN"), ("Seattle", "SEA", "WA"), ("Denver", "DEN", "CO"),
    ("Washington", "IAD", "DC"), ("Boston", "BOS", "MA"), ("Nashville", "BNA", "TN"),
    ("Miami", "MIA", "FL"), ("Atlanta", "ATL", "GA"), ("Detroit", "DTW", "MI"),
    ("Orlando", "MCO", "FL"), ("Las Vegas", "LAS", "NV"), ("Portland", "PDX", "OR")
]

destinations = ["London", "Tokyo", "Paris", "Rome", "Cancun", "Dubai", "Bangkok", "Berlin", "Barcelona", "Seoul", "Amsterdam", "Madrid", "Lisbon", "Singapore", "Sydney", "Vienna", "Prague", "Zurich"]
airlines = ["Delta", "United", "American", "Southwest", "JetBlue", "Spirit", "Frontier", "Alaska Airlines"]
hooks = ["Price Audit", "Inventory Reset", "Fare Discovery", "Hub Analysis", "Rate Shift", "Optimization", "Clear-out"]

# ==========================================
# 3. PAGE BUILDER ENGINE
# ==========================================

def get_aff_link(code):
    return f"{BASE_AFF_URL}?u=https://www.skyscanner.com/transport/flights-from/{code.lower()}"

def get_layout_one(city, code, state, i):
    price = random.randint(285, 990)
    airline = random.choice(airlines)
    aff_link = get_aff_link(code)
    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>{city} ({code}) {random.choice(hooks)} 2026</title><style>body{{font-family:sans-serif;margin:0;background:#f8fafc;}} .c{{max-width:800px;margin:50px auto;background:#fff;padding:40px;border-radius:15px;box-shadow:0 10px 25px rgba(0,0,0,0.05);}} .b{{display:block;background:#0071eb;color:#fff;text-align:center;padding:20px;text-decoration:none;border-radius:8px;font-weight:700;}}</style></head><body><div class="c"><h1>{city} Flight Dashboard</h1><p>Market update for {state}: {airline} frequency from {code} is up. Fares from ${price}.</p><a href="{aff_link}" class="b">EXPLORE {city.upper()} DEALS</a><p style="font-size:9px;color:#ccc;margin-top:30px;">ID: {i}-V320-A</p></div></body></html>"""

def get_layout_two(city, code, state, i):
    days = random.randint(14, 45)
    aff_link = get_aff_link(code)
    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>Direct from {city} {code} - Skyscanner 2026</title><style>body{{line-height:1.6;color:#2d3748;max-width:750px;margin:auto;padding:40px;background:#fff;}} .i{{background:#fffaf0;padding:25px;border-left:6px solid #ffd700;margin:30px 0;}} .a{{color:#0071eb;font-weight:bold;text-decoration:none;}}</style></head><body><h1>{city} ({code}) Intelligence</h1><p>Travelers in {state} are seeing a price floor reset.</p><div class="i"><strong>2026 Strategy:</strong> Book {code} departures {days} days out for maximum yield.</div><a href="{aff_link}" class="a">Check {city} Prices Now &rarr;</a><p style="font-size:9px;color:#ccc;margin-top:50px;">ID: {i}-V320-B</p></body></html>"""

# ==========================================
# 4. EXECUTION FLOW
# ==========================================

def run_vulture_engine():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    
    # We write sitemaps in chunks to prevent memory errors at 320k
    sitemap_count = 1
    generated_in_current_sitemap = 0
    s_file = open(f"sitemap_vulture_320k_{sitemap_count}.xml", "w", encoding="utf-8")
    s_file.write('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')

    print(f"🔥 VULTURE TITAN 320K: Generating massive SEO network...")
    
    for i in range(1, TOTAL_PAGES + 1):
        city, code, state = random.choice(hubs)
        file_name = f"sky-2026-{code.lower()}-{i}.html"
        
        content = get_layout_one(city, code, state, i) if random.random() > 0.5 else get_layout_two(city, code, state, i)
            
        with open(os.path.join(OUTPUT_DIR, file_name), "w", encoding="utf-8") as f:
            f.write(content)
        
        # Add to sitemap
        s_file.write(f'<url><loc>{DOMAIN}/{file_name}</loc><changefreq>weekly</changefreq></url>')
        generated_in_current_sitemap += 1

        # Rotate sitemap every 40,000 links for indexing safety
        if generated_in_current_sitemap >= 40000:
            s_file.write('</urlset>')
            s_file.close()
            sitemap_count += 1
            generated_in_current_sitemap = 0
            s_file = open(f"sitemap_vulture_320k_{sitemap_count}.xml", "w", encoding="utf-8")
            s_file.write('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')

        if i % 50000 == 0:
            print(f"✅ Progress: {i} pages indexed...")

    s_file.write('</urlset>')
    s_file.close()
    print(f"✨ MISSION COMPLETE. {TOTAL_PAGES} files and {sitemap_count} sitemaps ready.")

if __name__ == "__main__":
    run_vulture_engine()
