import os

def fix_client(filepath):
    if not os.path.exists(filepath): return
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # The current string starts with:
    # let lines = [];
    # let hasAny = false;
    # lines.push('*Zonas a depilar*');
    
    target = "let lines = [];\n      let hasAny = false;\n      lines.push('*Zonas a depilar*');"
    replacement = "let lines = [];\n      let hasAny = false;\n      lines.push('Hola, quiero agendar una cita con la siguiente cotización:');\n      lines.push('');\n      lines.push('*Zonas a depilar*');"
    
    if target in content:
        content = content.replace(target, replacement)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Added greeting to {filepath}")
    else:
        print(f"Could not find target in {filepath}")

fix_client('lista-de-precios.html')
fix_client('en/price-list.html')
