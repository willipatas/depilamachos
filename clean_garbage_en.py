import re

filepath = 'en/price-list.html'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Using regex to match from "ESTIMATED TOTAL" up to "encodeURIComponent(fullMessage);\n    }"
pattern = re.compile(r'\s+lines\.push\(`ESTIMATED TOTAL: \$\{formatCOP\(total\)\} COP`\);\s+lines\.push\(\'Location: Marsella, Bogota D\.C\.\'\);\s+lines\.push\(\'What times do you have available\?\'\);\s+const fullMessage = lines\.join\(\'\\n\'\);\s+rawMessageTextarea\.value = fullMessage;\s+btnWhatsapp\.href = \'https://wa\.me/573138934136\?text=\' \+ encodeURIComponent\(fullMessage\);\s+\}')

new_content = pattern.sub('', content)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(new_content)
print("Cleaned en/price-list.html")
