import re
import glob

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Client calc dynamic prices:
    # 'Espalda Completa' -> 'Espalda'
    content = content.replace("label: 'Espalda Completa'", "label: 'Espalda'")
    content = content.replace('label: "Espalda Completa"', 'label: "Espalda"')
    
    # 'Brazos Completos' -> 'Brazos'
    content = content.replace("label: 'Brazos Completos'", "label: 'Brazos'")
    content = content.replace('label: "Brazos Completos"', 'label: "Brazos"')
    
    # 'Piernas Completas' -> 'Piernas'
    content = content.replace("label: 'Piernas Completas'", "label: 'Piernas'")
    content = content.replace('label: "Piernas Completas"', 'label: "Piernas"')
    
    # Admin calc dynamic labels:
    # `data-zone-name="Espalda Masculina"` was previously stripped to `Espalda`
    # Let's ensure data-zone-name="Espalda" etc. is set.
    
    # Let's update Perianal to "Zona Perianal / Interglútea"
    content = content.replace('data-zone="Perianal"', 'data-zone="Zona Perianal / Interglútea"')
    content = content.replace('data-zone-name="Perianal"', 'data-zone-name="Zona Perianal / Interglútea"')
    content = content.replace('data-zone-name="Zona Perianal"', 'data-zone-name="Zona Perianal / Interglútea"')
    # If the UI has <h3 class="...">Zona Perianal</h3>
    content = content.replace('>Zona Perianal</h3>', '>Zona Perianal / Interglútea</h3>')
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

for f in glob.glob('*.html') + glob.glob('en/*.html'):
    fix_file(f)
    print(f"Fixed zone names in {f}")

