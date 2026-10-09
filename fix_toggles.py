import os

def fix_toggle(filepath, correct_es_href):
    if not os.path.exists(filepath): return
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # The broken toggle looks like this in all 3 files:
    # <button class="px-space-xs py-space-xs rounded font-label-sm text-label-sm text-primary" type="button">ES</button><span class="text-outline-variant font-label-sm text-label-sm">/</span><a href="en/..." ...>EN</a>
    
    # Let's just find the whole <div> that contains it and replace it.
    import re
    # Match the entire div containing the ES/EN toggle
    pattern = re.compile(r'<div class="flex items-center bg-surface-container rounded-lg px-space-xs py-space-xs">.*?</div>')
    
    # We want it to be:
    replacement = f'<div class="flex items-center bg-surface-container rounded-lg px-space-xs py-space-xs"><a href="{correct_es_href}" class="px-space-xs py-space-xs rounded font-label-sm text-label-sm text-on-surface-variant hover:text-on-surface" style="cursor: pointer;">ES</a><span class="text-outline-variant font-label-sm text-label-sm">/</span><button class="px-space-xs py-space-xs rounded font-label-sm text-label-sm text-primary" type="button">EN</button></div>'

    new_content = pattern.sub(replacement, content)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Fixed {filepath} -> {correct_es_href}")


fix_toggle('en/index.html', '../')
fix_toggle('en/condiciones.html', '../condiciones')
fix_toggle('en/preciosadmin.html', '../preciosadmin')

