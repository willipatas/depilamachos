import os
import glob
import re

def fix_file(filepath):
    if not os.path.exists(filepath): return
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # We want to find: class="relative w-full aspect-[4/5] rounded-xl overflow-hidden bg-surface-container shadow-2xl"
    # and replace with: class="relative w-full aspect-[4/5] max-h-[500px] lg:max-h-none rounded-xl overflow-hidden bg-surface-container shadow-2xl"
    
    old_class = 'class="relative w-full aspect-[4/5] rounded-xl overflow-hidden bg-surface-container shadow-2xl"'
    new_class = 'class="relative w-full aspect-[4/5] max-h-[500px] lg:max-h-none rounded-xl overflow-hidden bg-surface-container shadow-2xl"'
    
    if old_class in content:
        content = content.replace(old_class, new_class)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed {filepath}")
    else:
        print(f"Class not found exactly in {filepath}, using regex...")
        # fallback regex
        pattern = re.compile(r'class="([^"]*aspect-\[4/5\][^"]*rounded-xl[^"]*)"')
        def replacer(match):
            cls = match.group(1)
            if 'max-h' not in cls:
                cls = cls.replace('aspect-[4/5]', 'aspect-[4/5] max-h-[500px] lg:max-h-none')
            return f'class="{cls}"'
        content = pattern.sub(replacer, content)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed {filepath} via regex")

fix_file('index.html')
fix_file('en/index.html')
