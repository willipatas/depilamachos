import os
import glob

def update_file(filepath):
    if not os.path.exists(filepath): return
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Calculators (lista-de-precios.html, en/price-list.html) - Máquina eléctrica
    # "algo de largo o" -> "algo de largo el vello o"
    content = content.replace('dejar algo de largo o', 'dejar algo de largo el vello o')
    
    # 2. Condiciones (condiciones.html, en/condiciones.html) and Footer
    # Spanish
    content = content.replace('Línea Concierge:', 'Escribe a nuestro WhatsApp:')
    content = content.replace('Suite con aislamiento visual acústico y acceso restringido.', 'Estudio con aislamiento visual y acceso restringido.')
    content = content.replace('desinfección total de la suite', 'desinfección total del estudio')
    content = content.replace('o combinaciones de paquetes con la máxima discreción.', 'con la máxima discreción.')
    content = content.replace('Calculadora de Paquetes', 'Calculadora de Precios')
    
    # English
    content = content.replace('Concierge Line:', 'Write to our WhatsApp:')
    content = content.replace('Suite with visual and acoustic isolation', 'Studio with visual isolation')
    content = content.replace('disinfection of the suite', 'disinfection of the studio')
    content = content.replace('ingrown hairs, or package combinations with', 'ingrown hairs with')
    content = content.replace('Package Calculator', 'Pricing Calculator')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Updated {filepath}")

for f in glob.glob('*.html') + glob.glob('en/*.html'):
    update_file(f)
