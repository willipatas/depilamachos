import os
import glob

def remove_icon():
    files = glob.glob('*.html') + glob.glob('en/*.html')
    icon_html = '<div class="w-8 h-8 rounded-full bg-primary flex items-center justify-center"><span class="material-symbols-outlined text-on-primary text-[18px]">person</span></div>'
    
    for filepath in files:
        if not os.path.exists(filepath): continue
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        if icon_html in content:
            content = content.replace(icon_html, '')
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Removed icon from {filepath}")
        else:
            print(f"Icon not found in {filepath}")

remove_icon()
