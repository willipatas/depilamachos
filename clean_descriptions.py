import re
import os
import glob

def clean_desc(filepath):
    if not os.path.exists(filepath): return
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Remove the <p> elements immediately following the zone headers
    
    # 1. Espalda
    content = re.sub(r'(<h4[^>]*>Espalda</h4>\s*)<p class="font-body-sm text-body-sm text-on-surface-variant[^"]*">.*?</p>', r'\1', content)
    
    # 2. Brazos y Extremidades Superiores
    content = re.sub(r'(<h4[^>]*>Brazos[^<]*</h4>\s*)<p class="font-body-sm text-body-sm text-on-surface-variant[^"]*">.*?</p>', r'\1', content)
    
    # 3. Piernas y Muslos
    content = re.sub(r'(<h4[^>]*>Piernas[^<]*</h4>\s*)<p class="font-body-sm text-body-sm text-on-surface-variant[^"]*">.*?</p>', r'\1', content)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Cleaned descriptions in {filepath}")

for f in ['lista-de-precios.html', 'en/price-list.html']:
    clean_desc(f)
