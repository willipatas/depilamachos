import os
import glob
import re

def fix_terms(filepath):
    if not os.path.exists(filepath): return
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Spanish body parts + masculino/a(s)
    # E.g. "Espalda Masculina", "Pecho Masculino", "espalda masculina", "pecho masculino"
    replacements = [
        (r'(?i)(Espalda)\s+Masculina', r'\1'),
        (r'(?i)(Pecho)\s+Masculino', r'\1'),
        (r'(?i)(Glúteos?)\s+Masculinos?', r'\1'),
        (r'(?i)(Gluteos?)\s+Masculinos?', r'\1'),
        (r'(?i)(Axilas?)\s+Masculinas?', r'\1'),
        (r'(?i)(Abdomen)\s+Masculino', r'\1'),
        (r'(?i)(Pubis)\s+Masculino', r'\1'),
        (r'(?i)(Brazos?)\s+Masculinos?', r'\1'),
        (r'(?i)(Piernas?)\s+Masculinas?', r'\1'),
        (r'(?i)(Escroto)\s+Masculino', r'\1'),
        (r'(?i)(Manos?)\s+Masculinas?', r'\1'),
        (r'(?i)(Pies?)\s+Masculinos?', r'\1'),
        (r'(?i)(Perianal)\s+Masculino', r'\1'),
        
        # English body parts (Male Back, Male Chest, etc.)
        (r'(?i)Male\s+(Back)', r'\1'),
        (r'(?i)Male\s+(Chest)', r'\1'),
        (r'(?i)Male\s+(Buttocks?)', r'\1'),
        (r'(?i)Male\s+(Arms?)', r'\1'),
        (r'(?i)Male\s+(Legs?)', r'\1'),
        (r'(?i)Male\s+(Abdomen)', r'\1'),
        (r'(?i)Male\s+(Pubis)', r'\1'),
    ]

    for old, new in replacements:
        content = re.sub(old, new, content)

    # Some might be "Zonas masculinas" -> "Zonas" ? 
    # Let's check if the user said specifically body parts. Yes.

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Fixed gender terms in {filepath}")

for f in glob.glob('*.html') + glob.glob('en/*.html'):
    fix_terms(f)
