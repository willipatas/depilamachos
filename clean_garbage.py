import os

def clean(filepath):
    if not os.path.exists(filepath): return
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    garbage = """
      lines.push(`TOTAL ESTIMADO: ${formatCOP(total)} COP`);
      lines.push('Sede: Marsella, Bogotá D.C.');
      lines.push('¿Qué horarios tienen disponibles?');

      const fullMessage = lines.join('\\n');
      rawMessageTextarea.value = fullMessage;
      btnWhatsapp.href = 'https://wa.me/573138934136?text=' + encodeURIComponent(fullMessage);
    }
"""
    if garbage in content:
        content = content.replace(garbage, "")
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Cleaned garbage in {filepath}")
    else:
        print(f"Garbage not found in {filepath} (Might have literal newlines instead of \\n)")
        
        # fallback regex if newline is different
        import re
        content = re.sub(r"\s+lines\.push\(`TOTAL ESTIMADO: \$\{formatCOP\(total\)\} COP`\);\s+lines\.push\('Sede: Marsella, Bogotá D\.C\.'\);\s+lines\.push\('¿Qué horarios tienen disponibles\?'\);\s+const fullMessage = lines\.join\('\\n'\);\s+rawMessageTextarea\.value = fullMessage;\s+btnWhatsapp\.href = 'https://wa\.me/573138934136\?text=' \+ encodeURIComponent\(fullMessage\);\s+\}", "", content)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

clean('lista-de-precios.html')
clean('en/price-list.html')
