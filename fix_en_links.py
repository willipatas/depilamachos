import os
import glob
import re

def fix_en_links(filepath):
    if not os.path.exists(filepath): return
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Fix root references to point to /en/
    content = content.replace('href="/"', 'href="/en/"')
    content = content.replace('href="/#servicios"', 'href="/en/#servicios"')
    content = content.replace('href="/#ubicacion"', 'href="/en/#ubicacion"')
    
    # Fix calculator link to use the English path
    content = content.replace('href="lista-de-precios"', 'href="price-list"')
    content = content.replace('href="lista-de-precios?select=', 'href="price-list?select=')
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print(f"Fixed links in {filepath}")

for f in glob.glob('en/*.html'):
    fix_en_links(f)
