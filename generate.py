import os
from jinja2 import Environment, FileSystemLoader

# 1. The Data Source (Global Standards)
data_sources = [
    # --- US Standards (Inches) ---
    {"name": "4x4x4 Cube", "l": 4, "w": 4, "h": 4, "type": "box_single", "wall": "single", "unit": "in"},
    {"name": "6x6x6 Cube", "l": 6, "w": 6, "h": 6, "type": "box_single", "wall": "single", "unit": "in"},
    {"name": "8x8x8 Cube", "l": 8, "w": 8, "h": 8, "type": "box_single", "wall": "single", "unit": "in"},
    {"name": "10x10x10 Cube", "l": 10, "w": 10, "h": 10, "type": "box_single", "wall": "single", "unit": "in"},
    {"name": "12x12x12 Cube", "l": 12, "w": 12, "h": 12, "type": "box_double", "wall": "double", "unit": "in"},
    {"name": "18x18x18 Large", "l": 18, "w": 18, "h": 18, "type": "box_double", "wall": "double", "unit": "in"},
    {"name": "FedEx Small Box", "l": 10.9, "w": 1.5, "h": 12.4, "type": "box_single", "wall": "single", "unit": "in"},
    {"name": "FedEx Medium Box", "l": 13.3, "w": 11.5, "h": 2.4, "type": "box_single", "wall": "single", "unit": "in"},
    {"name": "FedEx Large Box", "l": 17.9, "w": 12.4, "h": 3.0, "type": "box_single", "wall": "single", "unit": "in"},
    {"name": "FedEx Extra Large Box", "l": 11.9, "w": 10.8, "h": 11.0, "type": "box_double", "wall": "double", "unit": "in"},
    {"name": "USPS Small Flat Rate", "l": 8.6, "w": 5.4, "h": 1.6, "type": "box_single", "wall": "single", "unit": "in"},
    {"name": "USPS Medium Flat Rate (Top)", "l": 11.0, "w": 8.5, "h": 5.5, "type": "box_single", "wall": "single", "unit": "in"},
    {"name": "USPS Medium Flat Rate (Side)", "l": 13.6, "w": 11.9, "h": 3.4, "type": "box_single", "wall": "single", "unit": "in"},
    {"name": "USPS Large Flat Rate", "l": 12.0, "w": 12.0, "h": 5.5, "type": "box_single", "wall": "single", "unit": "in"},
    {"name": "10x13 Poly Mailer (T-Shirt)", "l": 10, "w": 13, "h": 0.1, "type": "poly", "wall": "n/a", "unit": "in"},
    {"name": "14.5x19 Poly Mailer (Jacket)", "l": 14.5, "w": 19, "h": 0.1, "type": "poly", "wall": "n/a", "unit": "in"},
    {"name": "19x24 Poly Mailer (Large)", "l": 19, "w": 24, "h": 0.1, "type": "poly", "wall": "n/a", "unit": "in"},
    {"name": "#0 Kraft Bubble Mailer", "l": 6, "w": 10, "h": 0.5, "type": "kraft", "wall": "n/a", "unit": "in"},
    {"name": "#2 Kraft Bubble Mailer", "l": 8.5, "w": 12, "h": 0.5, "type": "kraft", "wall": "n/a", "unit": "in"},
    {"name": "#5 Kraft Bubble Mailer", "l": 10.5, "w": 16, "h": 0.5, "type": "kraft", "wall": "n/a", "unit": "in"},

    # --- Germany: DHL Packsets (Centimeters) ---
    {"name": "DHL Packset XS", "l": 22.5, "w": 14.5, "h": 3.0, "type": "box_single", "wall": "single", "unit": "cm"},
    {"name": "DHL Packset S", "l": 25.0, "w": 17.5, "h": 10.0, "type": "box_single", "wall": "single", "unit": "cm"},
    {"name": "DHL Packset M", "l": 37.5, "w": 30.0, "h": 13.5, "type": "box_single", "wall": "single", "unit": "cm"},
    {"name": "DHL Packset L", "l": 45.0, "w": 35.0, "h": 20.0, "type": "box_single", "wall": "single", "unit": "cm"},
    {"name": "DHL Bottle Box (Packset F)", "l": 38.0, "w": 12.0, "h": 12.0, "type": "box_double", "wall": "double", "unit": "cm"},

    # --- France: Colissimo Ready-to-Ship (Centimeters) ---
    {"name": "Colissimo Box M", "l": 23.0, "w": 13.0, "h": 12.0, "type": "box_single", "wall": "single", "unit": "cm"},
    {"name": "Colissimo Box L", "l": 29.0, "w": 21.0, "h": 15.0, "type": "box_single", "wall": "single", "unit": "cm"},
    {"name": "Colissimo Box XL", "l": 40.0, "w": 27.5, "h": 19.5, "type": "box_double", "wall": "double", "unit": "cm"},
    {"name": "Colissimo Bottle Box", "l": 37.0, "w": 10.0, "h": 10.0, "type": "box_double", "wall": "double", "unit": "cm"},

    # --- UK: Royal Mail Limits (Centimeters) ---
    {"name": "Royal Mail Small Parcel (Max)", "l": 45.0, "w": 35.0, "h": 16.0, "type": "box_single", "wall": "single", "unit": "cm"},
    {"name": "Royal Mail Medium Parcel (Max)", "l": 61.0, "w": 46.0, "h": 46.0, "type": "box_double", "wall": "double", "unit": "cm"},

    # --- Amazon Standard Boxes (Inches) ---
    {"name": "Amazon Box A1", "l": 10.0, "w": 7.0, "h": 3.5, "type": "box_single", "wall": "single", "unit": "in"},
    {"name": "Amazon Box A3", "l": 12.5, "w": 10.0, "h": 4.0, "type": "box_single", "wall": "single", "unit": "in"},
    {"name": "Amazon Box 10", "l": 8.75, "w": 6.0, "h": 3.25, "type": "box_single", "wall": "single", "unit": "in"},
    {"name": "Amazon Box 20", "l": 8.5, "w": 6.0, "h": 4.0, "type": "box_single", "wall": "single", "unit": "in"},

    # --- Uline Best Sellers (Inches) ---
    {"name": "Uline S-4481 (Long)", "l": 4.0, "w": 4.0, "h": 12.0, "type": "box_single", "wall": "single", "unit": "in"},
    {"name": "Uline S-4193 (Cube)", "l": 36.0, "w": 36.0, "h": 36.0, "type": "box_single", "wall": "single", "unit": "in"},
    {"name": "Uline S-16568 (Indestructo)", "l": 7.0, "w": 5.0, "h": 3.0, "type": "box_single", "wall": "single", "unit": "in"},

    # --- Canada Post Flat Rate (Centimeters) ---
    {"name": "Canada Post Flat Rate XS", "l": 22.5, "w": 15.5, "h": 7.6, "type": "box_single", "wall": "single", "unit": "cm"},
    {"name": "Canada Post Flat Rate Small", "l": 35.0, "w": 26.0, "h": 5.0, "type": "box_single", "wall": "single", "unit": "cm"},
    {"name": "Canada Post Flat Rate Medium", "l": 37.9, "w": 26.0, "h": 12.0, "type": "box_single", "wall": "single", "unit": "cm"},
    {"name": "Canada Post Flat Rate Large", "l": 40.3, "w": 29.8, "h": 18.7, "type": "box_single", "wall": "single", "unit": "cm"},

    # --- RAJAPACK Europe Standards (Centimeters) ---
    {"name": "RAJA Single Wall (Ref 1)", "l": 20.0, "w": 15.0, "h": 10.0, "type": "box_single", "wall": "single", "unit": "cm"},
    {"name": "RAJA Single Wall (Ref 2)", "l": 30.0, "w": 20.0, "h": 15.0, "type": "box_single", "wall": "single", "unit": "cm"},
    {"name": "RAJA Double Wall (Heavy)", "l": 40.0, "w": 30.0, "h": 20.0, "type": "box_double", "wall": "double", "unit": "cm"},
    {"name": "RAJA Long Box (Posters)", "l": 61.0, "w": 10.5, "h": 10.5, "type": "box_single", "wall": "single", "unit": "cm"},

    # --- Product-Specific Standards (Use Case SEO) ---
    # Shoeboxes
    {"name": "Sneaker Box (Standard)", "l": 13.0, "w": 9.0, "h": 5.0, "type": "box_single", "wall": "single", "unit": "in"},
    {"name": "Boot Box (Large)", "l": 16.0, "w": 12.0, "h": 6.0, "type": "box_single", "wall": "single", "unit": "in"},

    # Media & Books
    {"name": "Vinyl Record Mailer (12-inch LP)", "l": 13.0, "w": 13.0, "h": 1.0, "type": "box_single", "wall": "single", "unit": "in"},
    {"name": "Book Wrap (Standard Paperback)", "l": 24.0, "w": 17.0, "h": 5.0, "type": "box_single", "wall": "single", "unit": "cm"}, # Common EU format
    {"name": "Poster Tube (24-inch)", "l": 24.0, "w": 3.0, "h": 3.0, "type": "box_double", "wall": "double", "unit": "in"},

    # Fragile / Retail
    {"name": "Mug Box (11oz Standard)", "l": 5.0, "w": 5.0, "h": 5.0, "type": "box_double", "wall": "double", "unit": "in"}, # Double wall for protection
    {"name": "Olive Oil Bottle Shipper (Single)", "l": 4.0, "w": 4.0, "h": 13.0, "type": "box_double", "wall": "double", "unit": "in"},
    {"name": "Candle Box (Standard Jar)", "l": 4.0, "w": 4.0, "h": 4.0, "type": "box_single", "wall": "single", "unit": "in"},

    # Apparel
    {"name": "Cap/Hat Box", "l": 8.0, "w": 8.0, "h": 6.0, "type": "box_single", "wall": "single", "unit": "in"},
    {"name": "Jeans/Denim Mailer Box", "l": 12.0, "w": 10.0, "h": 2.0, "type": "box_single", "wall": "single", "unit": "in"},

    # --- Artisan & Handmade (Etsy Niche) ---
    # Beauty & Scent
    {"name": "Soap Bar Box (Standard)", "l": 3.5, "w": 2.5, "h": 1.5, "type": "box_single", "wall": "single", "unit": "in"},
    {"name": "Perfume Bottle Box (Tall)", "l": 3.0, "w": 3.0, "h": 6.0, "type": "box_single", "wall": "single", "unit": "in"},

    # Jewelry & Accessories
    {"name": "Jewelry Shipping Box (Small)", "l": 6.0, "w": 4.0, "h": 2.0, "type": "box_single", "wall": "single", "unit": "in"}, # Indestructo style
    
    # Art & Stationery
    {"name": "Picture Frame Mailer (8x10)", "l": 13.0, "w": 10.0, "h": 2.0, "type": "box_single", "wall": "single", "unit": "in"},
    {"name": "Stationery Box (A5 Shallow)", "l": 9.0, "w": 6.5, "h": 1.0, "type": "box_single", "wall": "single", "unit": "in"},

    # --- Beauty & Cosmetics (High Volume) ---
    {"name": "Lipstick Box (Standard)", "l": 0.8, "w": 0.8, "h": 3.5, "type": "box_single", "wall": "single", "unit": "in"},
    {"name": "Eyeliner/Mascara Box", "l": 0.6, "w": 0.6, "h": 5.5, "type": "box_single", "wall": "single", "unit": "in"},
    {"name": "Compact Powder Box", "l": 3.0, "w": 3.0, "h": 1.0, "type": "box_single", "wall": "single", "unit": "in"},
    {"name": "Skincare Dropper Box (30ml)", "l": 1.5, "w": 1.5, "h": 4.5, "type": "box_single", "wall": "single", "unit": "in"},
    {"name": "Hair Extension Mailer (Long)", "l": 12.0, "w": 5.0, "h": 1.5, "type": "box_single", "wall": "single", "unit": "in"},

    # --- Consumer Tech ---
    {"name": "Smartphone Box (Standard)", "l": 7.0, "w": 4.0, "h": 2.0, "type": "box_single", "wall": "single", "unit": "in"},
    {"name": "Phone Case Mailer (Slim)", "l": 7.5, "w": 4.5, "h": 0.5, "type": "box_single", "wall": "single", "unit": "in"},
    {"name": "Earbuds / AirPods Box", "l": 4.0, "w": 4.0, "h": 2.0, "type": "box_single", "wall": "single", "unit": "in"},
    {"name": "Tablet Box (10 inch)", "l": 10.0, "w": 7.0, "h": 2.0, "type": "box_single", "wall": "single", "unit": "in"},
    {"name": "Laptop Box (15 inch)", "l": 16.0, "w": 11.0, "h": 3.0, "type": "box_single", "wall": "single", "unit": "in"},

    # --- Health & Supplements ---
    {"name": "Supplement Bottle Box (Small)", "l": 2.5, "w": 2.5, "h": 4.5, "type": "box_single", "wall": "single", "unit": "in"},
    {"name": "Protein Powder Tub Box (2lb)", "l": 6.0, "w": 6.0, "h": 10.0, "type": "box_single", "wall": "single", "unit": "in"},
    {"name": "Vitamin Blister Pack Mailer", "l": 6.0, "w": 4.0, "h": 1.0, "type": "box_single", "wall": "single", "unit": "in"},

    # --- Apparel & Accessories ---
    {"name": "T-Shirt Box (Rigid)", "l": 10.0, "w": 8.0, "h": 2.0, "type": "box_single", "wall": "single", "unit": "in"},
    {"name": "Hoodie Poly Mailer", "l": 15.0, "w": 12.0, "h": 2.0, "type": "poly", "wall": "n/a", "unit": "in"},
    {"name": "Sunglasses Box", "l": 7.0, "w": 3.0, "h": 2.5, "type": "box_single", "wall": "single", "unit": "in"},
    {"name": "Watch Box (Cube)", "l": 4.0, "w": 4.0, "h": 3.0, "type": "box_single", "wall": "single", "unit": "in"},

    # --- Home & Hobbies ---
    {"name": "Water Bottle Box (Standard)", "l": 3.0, "w": 3.0, "h": 10.0, "type": "box_single", "wall": "single", "unit": "in"},
    {"name": "Funko Pop Protector Box", "l": 4.5, "w": 3.5, "h": 6.25, "type": "box_single", "wall": "single", "unit": "in"},
    {"name": "Board Game Box (Standard)", "l": 12.0, "w": 12.0, "h": 3.0, "type": "box_double", "wall": "double", "unit": "in"},
]

# Setup Jinja2 Environment
env = Environment(loader=FileSystemLoader('.'))
template = env.get_template('template.html')

# Ensure output directory exists
output_dir = 'pages'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 2. The Logic
for item in data_sources:
    raw_l = item['l']
    raw_w = item['w']
    raw_h = item['h']
    unit = item['unit'] # 'in' or 'cm'
    
    # Determine Conversion Factor
    if unit == 'in':
        to_meters = 0.0254
    else: # 'cm'
        to_meters = 0.01
    
    # Convert to meters for physics calculation
    l_m = raw_l * to_meters
    w_m = raw_w * to_meters
    h_m = raw_h * to_meters
    
    weight_g = 0
    selected_value = ""

    # Calculate Weight
    if item['type'] == 'box_single':
        # Surface area = 2(lw+lh+wh)
        base_area = 2 * ((l_m * w_m) + (l_m * h_m) + (w_m * h_m))
        # Single Wall Box: 450 GSM. Area * 1.25
        weight_g = base_area * 1.25 * 450
        selected_value = "single_wall"
        
    elif item['type'] == 'box_double':
        # Surface area = 2(lw+lh+wh)
        base_area = 2 * ((l_m * w_m) + (l_m * h_m) + (w_m * h_m))
        # Double Wall Box: 750 GSM. Area * 1.35
        weight_g = base_area * 1.35 * 750
        selected_value = "double_wall"
            
    elif item['type'] == 'poly':
        # Poly Mailer: 120 GSM (2 layers). Area = 2*(l*w)
        area = 2 * (l_m * w_m)
        weight_g = area * 120
        selected_value = "poly_mailer"
        
    elif item['type'] == 'kraft':
        # Kraft Mailer: 250 GSM (Paper+Bubble). Area = 2*(l*w) * 1.10
        area = 2 * (l_m * w_m) * 1.10
        weight_g = area * 250
        selected_value = "kraft_mailer"

    weight_kg = weight_g / 1000
    
    # Slugify name for filename
    slug = item['name'].lower().replace('#', '').replace(' ', '-').replace('(', '').replace(')', '').replace('.', '-').replace('/', '-')
    filename = f"{slug}-weight-csrd.html"
    
    # SEO Title
    seo_title = f"CSRD Weight Data: {item['name']} ({raw_l}x{raw_w}x{raw_h} {unit}) - Compliance Code & Fees"
    
    # Render Template
    output_html = template.render(
        name=item['name'],
        type=item['type'], # for breadcrumb (can be raw type)
        l=raw_l,
        w=raw_w,
        h=raw_h,
        unit=unit, # Pass unit to template
        weight_g=round(weight_g),
        weight_kg=f"{weight_kg:.3f}",
        seo_title=seo_title,
        selected_value=selected_value
    )
    
    # Write File
    with open(os.path.join(output_dir, filename), 'w', encoding='utf-8') as f:
        f.write(output_html)
        print(f"Generated: {filename}")

print("Done generating pages.")

# 3. Generate Sitemap
def generate_sitemap():
    print("Generating sitemap.xml...")
    base_url = "https://tare.fyi"
    sitemap_content = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
"""

    # Add Home Page
    sitemap_content += f'  <url><loc>{base_url}/</loc></url>\n'

    # Scan pages directory
    if os.path.exists(output_dir):
        files = [f for f in os.listdir(output_dir) if f.endswith(".html")]
        files.sort()
        for filename in files:
            url = f"{base_url}/pages/{filename}"
            sitemap_content += f"  <url><loc>{url}</loc></url>\n"
    
    sitemap_content += '</urlset>'
    
    with open("sitemap.xml", "w", encoding="utf-8") as f:
        f.write(sitemap_content)
    print("sitemap.xml generated.")

# 4. Generate robots.txt
def generate_robots_txt():
    print("Generating robots.txt...")
    robots_content = """User-agent: *
Allow: /
Sitemap: https://tare.fyi/sitemap.xml
"""
    with open("robots.txt", "w", encoding="utf-8") as f:
        f.write(robots_content)
    print("robots.txt generated.")

# Call sitemap and robots.txt generation after pages are done
generate_sitemap()
generate_robots_txt()