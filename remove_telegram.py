import os
import glob
import re

def remove_telegram(filepath):
    if not os.path.exists(filepath): return
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Regex to capture the entire <a ...> ... </a> block containing t.me
    # Uses DOTALL to match across newlines
    pattern = re.compile(r'<a[^>]*href="https://t\.me/DepilaMachos"[^>]*>.*?</a>\n?', re.DOTALL)
    
    new_content = pattern.sub('', content)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"Removed Telegram from {filepath}")

for f in glob.glob('*.html') + glob.glob('en/*.html'):
    remove_telegram(f)
