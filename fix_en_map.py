import re
import os

filepath = 'en/index.html'
if os.path.exists(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update the outer container
    content = content.replace(
        '<div class="lg:col-span-6 relative">\n<div class="w-full h-96 rounded-xl overflow-hidden shadow-2xl relative bg-surface-card">',
        '<div class="lg:col-span-6 relative group">\n<a href="https://maps.app.goo.gl/CdFYkpgoT9hFDUYv6?g_st=ac" target="_blank" rel="noopener noreferrer" class="block w-full h-96 rounded-xl overflow-hidden shadow-2xl relative bg-surface-card transition-all duration-300 hover:-translate-y-1 hover:shadow-[0_15px_35px_rgba(212,175,55,0.2)]">'
    )

    # 2. Inject overlay and close tag
    hover_overlay = '''</div>
<!-- Hover CTA -->
<div class="absolute inset-0 bg-surface-base/40 opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex items-center justify-center pointer-events-none backdrop-blur-[2px]">
<span class="inline-flex items-center gap-2 px-space-lg py-space-sm rounded-full bg-primary text-on-primary font-label-md shadow-xl translate-y-4 group-hover:translate-y-0 transition-transform duration-300">
<span class="material-symbols-outlined text-[20px]">open_in_new</span>
Open in Google Maps
</span>
</div>
</a>
</div>'''

    old_ending = '<span class="">Close to main roads and TransMilenio</span>\n</div>\n</div>\n</div>'
    new_ending = f'<span class="">Close to main roads and TransMilenio</span>\n{hover_overlay}\n</div>'
    
    content = content.replace(old_ending, new_ending)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
