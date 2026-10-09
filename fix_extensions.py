import os
import glob

def strip_html_extension():
    files = glob.glob('*.html') + glob.glob('en/*.html') + ['sitemap.xml']
    for filepath in files:
        if not os.path.exists(filepath): continue
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Replace specific links
        replacements = [
            ('lista-de-precios.html', 'lista-de-precios'),
            ('condiciones.html', 'condiciones'),
            ('preciosadmin.html', 'preciosadmin'),
            ('price-list.html', 'price-list'),
            ('en/index.html', 'en/'),
            ('href="index.html"', 'href="/"'),
            ('href="index.html#', 'href="/#')
        ]
        
        for old, new in replacements:
            content = content.replace(old, new)
            
        # Re-fix potential double replacements if something got mangled, but the above is pretty safe.
        # Ensure we didn't break things like `en/price-list` becoming `en/price-list` instead of `en/price-list.html` which is what we want.
        
        # However, Canonical tags and OG tags in the <head> need the exact URL. They should just end in the extensionless version too.
        # E.g. <link rel="canonical" href="https://depilamachos.com.co/lista-de-precios">
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Stripped .html from links in {filepath}")

strip_html_extension()
