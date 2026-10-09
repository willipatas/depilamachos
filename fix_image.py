import re
import os

def remove_image(filepath):
    if not os.path.exists(filepath): return
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Match the image div block
    pattern = re.compile(r'<div class="w-full sm:w-44 h-32 rounded-lg overflow-hidden shrink-0">\s*<div class="bg-cover bg-center w-full h-full"[^>]+>\s*</div>\s*</div>', re.DOTALL)
    
    if pattern.search(content):
        content = pattern.sub('', content)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Removed image from {filepath}")
    else:
        print(f"Image not found in {filepath}")

remove_image('preciosadmin.html')
remove_image('en/preciosadmin.html')
