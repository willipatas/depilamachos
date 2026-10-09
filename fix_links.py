import os
import glob

def process_file(filepath):
    if not os.path.exists(filepath):
        return
        
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    
    # 1. Replace all explicit english links first to avoid partial replacement bugs
    content = content.replace('en/calculadora-cliente.html', 'en/price-list.html')
    
    # 2. Replace the rest (Spanish links and general names)
    content = content.replace('calculadora-cliente.html', 'lista-de-precios.html')
    
    # 3. Replace data-path (used for active nav highlighting)
    content = content.replace('data-path="calculadora-y-precios"', 'data-path="lista-de-precios"')

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated links in {filepath}")

# Update HTML files
for f in glob.glob("*.html") + glob.glob("en/*.html"):
    process_file(f)

# Update sitemap
process_file('sitemap.xml')

