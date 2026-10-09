import os
import glob

def fix_files():
    for filepath in glob.glob('*.html') + glob.glob('en/*.html'):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Fix client calculator
        bad_client = "const fullMessage = lines.join('\n');"
        good_client = "const fullMessage = lines.join('\\n');"
        
        # Also could be:
        # const fullMessage = lines.join('
        # ');
        
        # A more robust regex:
        import re
        content = re.sub(r"lines\.join\('\n'\);", r"lines.join('\\n');", content)
        
        # Admin calculator
        content = re.sub(r"return lines\.join\('\n'\);", r"return lines.join('\\n');", content)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed syntax in {filepath}")

fix_files()
