import os
import glob
import re

def fix_admin(filepath):
    if not os.path.exists(filepath): return
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # In preciosadmin.html, remove the separate Interglútea span
    pattern = re.compile(r'<h3 class="font-headline-sm text-headline-sm text-ivory-white">Zona Perianal / Interglútea</h3>\s*<span class="material-symbols-outlined text-primary text-\[16px\]">lock</span>\s*</div>\s*<span class="font-label-sm text-label-sm text-on-surface-variant group-\[\.bg-primary\]:text-on-primary">Interglútea</span>')
    replacement = r'<h3 class="font-headline-sm text-headline-sm text-ivory-white">Zona Perianal / Interglútea</h3>\n<span class="material-symbols-outlined text-primary text-[16px]">lock</span>\n</div>'
    
    content = pattern.sub(replacement, content)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

for f in glob.glob('preciosadmin.html') + glob.glob('en/preciosadmin.html'):
    fix_admin(f)
