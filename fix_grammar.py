import os
import glob

def fix_file(filepath):
    if not os.path.exists(filepath): return
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    content = content.replace('umbral de sensibilidad, vellos encarnados con', 'umbral de sensibilidad o vellos encarnados con')
    content = content.replace('sensitivity thresholds, ingrown hairs with', 'sensitivity thresholds, or ingrown hairs with')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

for f in glob.glob('*.html') + glob.glob('en/*.html'):
    fix_file(f)
