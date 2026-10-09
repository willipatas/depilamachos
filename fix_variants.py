import os
import glob
import re

def fix_admin(filepath):
    if not os.path.exists(filepath): return
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Admin JS variant fixes
    content = content.replace("const variantText = item.variant ? ` (${item.variant})` : '';", 
                              "const variantText = (item.variant && !['Completa', 'Completos', 'Completas', 'Full'].includes(item.variant)) ? ` (${item.variant})` : '';")
    content = content.replace("const variantTxt = z.variant ? ` (${z.variant})` : '';", 
                              "const variantTxt = (z.variant && !['Completa', 'Completos', 'Completas', 'Full'].includes(z.variant)) ? ` (${z.variant})` : '';")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
        
def fix_masaje():
    files = glob.glob('*.html') + glob.glob('en/*.html')
    for filepath in files:
        if not os.path.exists(filepath): continue
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Update Masaje Relajante text in UI
        content = content.replace("Masaje Relajante Integral (60 Min)", "Masaje Relajante")
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

for f in glob.glob('preciosadmin.html') + glob.glob('en/preciosadmin.html'):
    fix_admin(f)

fix_masaje()
