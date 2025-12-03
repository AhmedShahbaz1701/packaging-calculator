import os
from jinja2 import Environment, FileSystemLoader

# 1. The Data Source
data_sources = [
    # Common Cubes (The "Amazon Standards")
    {"name": "4x4x4 Cube", "l": 4, "w": 4, "h": 4, "type": "box", "wall": "single"},
    {"name": "6x6x6 Cube", "l": 6, "w": 6, "h": 6, "type": "box", "wall": "single"},
    {"name": "8x8x8 Cube", "l": 8, "w": 8, "h": 8, "type": "box", "wall": "single"},
    {"name": "10x10x10 Cube", "l": 10, "w": 10, "h": 10, "type": "box", "wall": "single"},
    {"name": "12x12x12 Cube", "l": 12, "w": 12, "h": 12, "type": "box", "wall": "double"},
    {"name": "18x18x18 Large", "l": 18, "w": 18, "h": 18, "type": "box", "wall": "double"},

    # FedEx Standard Sizes
    {"name": "FedEx Small Box", "l": 10.9, "w": 1.5, "h": 12.4, "type": "box", "wall": "single"},
    {"name": "FedEx Medium Box", "l": 13.3, "w": 11.5, "h": 2.4, "type": "box", "wall": "single"},
    {"name": "FedEx Large Box", "l": 17.9, "w": 12.4, "h": 3.0, "type": "box", "wall": "single"},
    {"name": "FedEx Extra Large Box", "l": 11.9, "w": 10.8, "h": 11.0, "type": "box", "wall": "double"},

    # USPS Flat Rate Sizes
    {"name": "USPS Small Flat Rate", "l": 8.6, "w": 5.4, "h": 1.6, "type": "box", "wall": "single"},
    {"name": "USPS Medium Flat Rate (Top)", "l": 11.0, "w": 8.5, "h": 5.5, "type": "box", "wall": "single"},
    {"name": "USPS Medium Flat Rate (Side)", "l": 13.6, "w": 11.9, "h": 3.4, "type": "box", "wall": "single"},
    {"name": "USPS Large Flat Rate", "l": 12.0, "w": 12.0, "h": 5.5, "type": "box", "wall": "single"},
    
    # Common Poly Mailers
    {"name": "10x13 Poly Mailer (T-Shirt)", "l": 10, "w": 13, "h": 0.1, "type": "poly", "wall": "n/a"},
    {"name": "14.5x19 Poly Mailer (Jacket)", "l": 14.5, "w": 19, "h": 0.1, "type": "poly", "wall": "n/a"},
    {"name": "19x24 Poly Mailer (Large)", "l": 19, "w": 24, "h": 0.1, "type": "poly", "wall": "n/a"},
    
    # Common Kraft Mailers
    {"name": "#0 Kraft Bubble Mailer", "l": 6, "w": 10, "h": 0.5, "type": "kraft", "wall": "n/a"},
    {"name": "#2 Kraft Bubble Mailer", "l": 8.5, "w": 12, "h": 0.5, "type": "kraft", "wall": "n/a"},
    {"name": "#5 Kraft Bubble Mailer", "l": 10.5, "w": 16, "h": 0.5, "type": "kraft", "wall": "n/a"},
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
    l_in = item['l']
    w_in = item['w']
    h_in = item['h']
    
    # Convert to meters
    l_m = l_in * 0.0254
    w_m = w_in * 0.0254
    h_m = h_in * 0.0254
    
    weight_g = 0
    selected_value = ""

    # Calculate Weight
    if item['type'] == 'box':
        # Surface area = 2(lw+lh+wh)
        base_area = 2 * ((l_m * w_m) + (l_m * h_m) + (w_m * h_m))
        
        if item['wall'] == 'single':
            # Single Wall Box: 450 GSM. Area * 1.25
            weight_g = base_area * 1.25 * 450
            selected_value = "single_wall"
        elif item['wall'] == 'double':
            # Double Wall Box: 750 GSM. Area * 1.35
            weight_g = base_area * 1.35 * 750
            selected_value = "double_wall"
            
    elif item['type'] == 'poly':
        # Poly Mailer: 120 GSM (2 layers). Area = 2*(l*w)
        # Note: The prompt says "Area = 2*(l*w)". It implies front and back.
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
    slug = item['name'].lower().replace(' ', '-').replace('(', '').replace(')', '').replace('.', '-')
    filename = f"{slug}-weight-csrd.html"
    
    # SEO Title
    seo_title = f"CSRD Weight Data: {item['name']} ({l_in}x{w_in}x{h_in}) - Compliance Code & Fees"
    
    # Render Template
    output_html = template.render(
        name=item['name'],
        type=item['type'], # for breadcrumb
        l=l_in,
        w=w_in,
        h=h_in,
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
    sitemap_content = """
<?xml version="1.0" encoding="UTF-8"?>
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
    robots_content = """
User-agent: *
Allow: /
Sitemap: https://tare.fyi/sitemap.xml
"""
    with open("robots.txt", "w", encoding="utf-8") as f:
        f.write(robots_content)
    print("robots.txt generated.")

# Call sitemap and robots.txt generation after pages are done
generate_sitemap()
generate_robots_txt()