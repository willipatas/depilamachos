import re
import os
import glob

def process_client_files():
    for filepath in ['lista-de-precios.html', 'en/price-list.html']:
        if not os.path.exists(filepath): continue
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Refactor client cards
        # We need to change peer-checked:text-ivory-white -> peer-checked:text-on-primary
        # We need to add peer-checked:text-on-primary to the price divs.
        # We need to change peer-checked:bg-emerald-accent/25 -> peer-checked:bg-primary
        
        # 1. Label texts
        content = content.replace('peer-checked:text-ivory-white', 'peer-checked:text-on-primary')
        
        # 2. Price texts (text-primary -> text-primary peer-checked:text-on-primary)
        # Be careful not to replace it multiple times.
        if 'peer-checked:text-on-primary' not in content.replace('peer-checked:text-ivory-white', 'peer-checked:text-on-primary'):
            pass # just a check
        content = content.replace('text-primary font-bold', 'text-primary font-bold peer-checked:text-on-primary')
        content = content.replace('text-primary" id=', 'text-primary peer-checked:text-on-primary" id=')
        content = re.sub(r'text-primary">(\$[0-9.,]+)</div>', r'text-primary peer-checked:text-on-primary">\1</div>', content)
        
        # 3. Background rings
        content = content.replace('peer-checked:bg-emerald-accent/25', 'peer-checked:bg-primary')
        
        # 4. In case there is an absolute inset-0 without z-index, let's ensure the text is relative z-10 so it's above the bg
        content = content.replace('class="font-label-sm', 'class="relative z-10 font-label-sm')
        content = content.replace('class="font-label-md', 'class="relative z-10 font-label-md')
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated client calculator {filepath}")

def process_admin_files():
    for filepath in ['preciosadmin.html', 'en/preciosadmin.html']:
        if not os.path.exists(filepath): continue
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # JS Replacement: bg-primary-container -> bg-primary, text-on-primary-container -> text-on-primary
        content = content.replace("bg-primary-container", "bg-primary")
        content = content.replace("text-on-primary-container", "text-on-primary")
        
        # Add group class to tech-chip
        content = content.replace('class="tech-chip p-2', 'class="tech-chip group p-2')
        content = content.replace('class="tech-chip text-left p-space-sm', 'class="tech-chip group text-left p-space-sm')
        
        # Inner divs mapping
        content = content.replace('class="font-label-sm text-label-sm text-on-surface-variant"', 'class="font-label-sm text-label-sm text-on-surface-variant group-[.bg-primary]:text-on-primary"')
        content = content.replace('class="font-label-md text-label-md text-gold-light mt-0.5"', 'class="font-label-md text-label-md text-gold-light group-[.bg-primary]:text-on-primary mt-0.5"')
        content = content.replace('class="font-label-md text-label-md text-on-surface mt-0.5"', 'class="font-label-md text-label-md text-on-surface group-[.bg-primary]:text-on-primary mt-0.5"')
        
        # For the macro zones in admin, they have mt-1 instead of mt-0.5 and might not have explicit mt sometimes
        content = content.replace('class="font-label-sm text-label-sm text-on-surface-variant"', 'class="font-label-sm text-label-sm text-on-surface-variant group-[.bg-primary]:text-on-primary"')
        content = content.replace('class="font-label-md text-label-md text-gold-light mt-1"', 'class="font-label-md text-label-md text-gold-light group-[.bg-primary]:text-on-primary mt-1"')
        content = content.replace('class="font-label-md text-label-md text-on-surface mt-1"', 'class="font-label-md text-label-md text-on-surface group-[.bg-primary]:text-on-primary mt-1"')
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated admin calculator {filepath}")

process_client_files()
process_admin_files()
