import glob

def fix_client(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Revert client DYNAMIC_PRICES labels
    # We look for the specific lines to avoid replacing something else
    content = content.replace("label: 'Espalda' }", "label: 'Espalda Completa' }")
    content = content.replace("label: 'Brazos' }", "label: 'Brazos Completos' }")
    content = content.replace("label: 'Piernas' }", "label: 'Piernas Completas' }")
    # Just in case they used double quotes
    content = content.replace('label: "Espalda" }', 'label: "Espalda Completa" }')
    content = content.replace('label: "Brazos" }', 'label: "Brazos Completos" }')
    content = content.replace('label: "Piernas" }', 'label: "Piernas Completas" }')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

def fix_admin(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Revert the variant omiter in JS
    old_variant_txt = "const variantTxt = (z.variant && !['Completa', 'Completos', 'Completas', 'Full'].includes(z.variant)) ? ` (${z.variant})` : '';"
    new_variant_txt = "const variantTxt = z.variant ? ` (${z.variant})` : '';"
    content = content.replace(old_variant_txt, new_variant_txt)

    old_variant_text = "const variantText = (item.variant && !['Completa', 'Completos', 'Completas', 'Full'].includes(item.variant)) ? ` (${item.variant})` : '';"
    new_variant_text = "const variantText = item.variant ? ` (${item.variant})` : '';"
    content = content.replace(old_variant_text, new_variant_text)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

for f in glob.glob('*.html') + glob.glob('en/*.html'):
    if 'preciosadmin' in f:
        fix_admin(f)
    else:
        fix_client(f)

print("Reverted full variants")
