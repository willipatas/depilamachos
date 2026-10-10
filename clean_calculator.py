import re
import os

def clean_file(filepath, is_en=False):
    if not os.path.exists(filepath): return
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update "Máquina" section
    if not is_en:
        content = content.replace('¿Máquina al Ras?', 'Máquina eléctrica')
        content = content.replace('Recorte pulcro al ras dérmico sin tirones ni irritación folicular.', 'Se pueden usar guías para dejar algo de largo o hacer un recorte pulcro sin tirones ni irritación folicular.')
    else:
        content = content.replace('Close Shave Machine?', 'Electric Clipper')
        content = content.replace('Clean close shave without pulling or follicular irritation.', 'Guards can be used to leave some length or provide a clean trim without pulling or follicular irritation.')

    # 2. Remove Section Headers
    # Matches <div ...> ... <h3>1. ...</h3> ... </div> (the entire flex header container)
    pattern_header1 = re.compile(r'<div class="flex items-center justify-between mb-space-md">\s*<div class="flex items-center gap-space-sm">\s*<span class="w-1\.5 h-4 rounded-full bg-primary"></span>\s*<h3 class="font-headline-md[^>]*>.*?</h3>\s*</div>\s*<span[^>]*>.*?</span>\s*</div>', re.DOTALL)
    content = pattern_header1.sub('', content)

    pattern_header2 = re.compile(r'<div class="flex items-center justify-between">\s*<div class="flex items-center gap-space-sm">\s*<span class="w-1\.5 h-4 rounded-full bg-primary"></span>\s*<h3 class="font-headline-md[^>]*>.*?</h3>\s*</div>\s*<span[^>]*>.*?</span>\s*</div>', re.DOTALL)
    content = pattern_header2.sub('', content)

    # 3. Remove descriptions under the dynamic zones (Espalda, Brazos, Piernas)
    pattern_desc_espalda = re.compile(r'<p class="font-body-sm text-body-sm text-on-surface-variant max-w-sm mt-space-sm">\s*Selecciona si deseas abarcar la espalda en su totalidad, o solo una parte\.\s*</p>', re.DOTALL)
    content = pattern_desc_espalda.sub('', content)
    
    pattern_desc_brazos = re.compile(r'<p class="font-body-sm text-body-sm text-on-surface-variant max-w-sm mt-space-sm">\s*Opción para brazo entero o solo media zona\.\s*</p>', re.DOTALL)
    content = pattern_desc_brazos.sub('', content)
    
    pattern_desc_piernas = re.compile(r'<p class="font-body-sm text-body-sm text-on-surface-variant max-w-sm mt-space-sm">\s*Incluye muslos, rodillas y pantorrillas en la opción completa\.\s*</p>', re.DOTALL)
    content = pattern_desc_piernas.sub('', content)
    
    # EN descriptions
    pattern_desc_espalda_en = re.compile(r'<p class="font-body-sm text-body-sm text-on-surface-variant max-w-sm mt-space-sm">\s*Select if you want to cover the entire back, or just a part\.\s*</p>', re.DOTALL)
    content = pattern_desc_espalda_en.sub('', content)
    
    pattern_desc_brazos_en = re.compile(r'<p class="font-body-sm text-body-sm text-on-surface-variant max-w-sm mt-space-sm">\s*Option for full arm or just half zone\.\s*</p>', re.DOTALL)
    content = pattern_desc_brazos_en.sub('', content)
    
    pattern_desc_piernas_en = re.compile(r'<p class="font-body-sm text-body-sm text-on-surface-variant max-w-sm mt-space-sm">\s*Includes thighs, knees and calves in the full option\.\s*</p>', re.DOTALL)
    content = pattern_desc_piernas_en.sub('', content)

    # 4. Remove informative blocks inside the calculator if any
    pattern_info = re.compile(r'<div class="col-span-1 md:col-span-2 p-space-md rounded-xl bg-surface-container-high flex items-start gap-space-sm border-l-2 border-primary mt-space-md">\s*<span class="material-symbols-outlined text-primary">info</span>.*?</div>', re.DOTALL)
    content = pattern_info.sub('', content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Cleaned {filepath}")

clean_file('lista-de-precios.html', is_en=False)
clean_file('en/price-list.html', is_en=True)
