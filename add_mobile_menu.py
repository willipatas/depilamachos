import re
import os
import glob

def process_file(filepath):
    if not os.path.exists(filepath):
        return
        
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Don't add if already added
    if 'id="mobileMenuBtn"' in content:
        print(f"Skipping {filepath}, menu already exists")
        return

    is_en = "en/" in filepath
    
    # 1. Inject Hamburger Button
    # Find the closing tag of the right-side header controls
    # Usually: <div class="w-8 h-8 rounded-full bg-primary flex items-center justify-center"><span class="material-symbols-outlined text-on-primary text-[18px]">person</span></div></div>
    
    btn_html = '''<button id="mobileMenuBtn" class="xl:hidden flex items-center justify-center p-2 text-ivory-white ml-2 rounded-lg bg-surface-container hover:bg-surface-container-high transition-colors">
<span class="material-symbols-outlined text-[24px]">menu</span>
</button></div></div>'''
    
    # Replace the last two closing divs of the header content
    content = re.sub(r'person</span></div></div></div></header>', r'person</span></div>' + btn_html + '</header>', content)

    # 2. Inject Mobile Menu Panel
    # Right after </header>
    if is_en:
        menu_html = '''</header>
<!-- Mobile Menu Overlay -->
<div id="mobileMenu" class="fixed inset-0 z-40 bg-surface-base/98 backdrop-blur-3xl transform translate-x-full transition-transform duration-300 xl:hidden flex flex-col pt-24 px-margin-mobile pb-space-lg overflow-y-auto">
  <div class="flex justify-between items-center mb-space-xl">
    <span class="font-headline-sm text-headline-sm tracking-wider uppercase text-ivory-white">Menu</span>
    <button id="closeMenuBtn" class="p-2 text-on-surface-variant hover:text-ivory-white rounded-lg bg-surface-container">
      <span class="material-symbols-outlined text-[24px]">close</span>
    </button>
  </div>
  <nav class="flex flex-col gap-space-lg" data-active-classes="text-primary font-label-lg">
    <a class="font-headline-md text-headline-md uppercase tracking-wider text-on-surface-variant hover:text-primary transition-colors mobile-link" href="index.html">Home</a>
    <a class="font-headline-md text-headline-md uppercase tracking-wider text-on-surface-variant hover:text-primary transition-colors mobile-link" href="index.html#servicios">Services</a>
    <a class="font-headline-md text-headline-md uppercase tracking-wider text-on-surface-variant hover:text-primary transition-colors mobile-link" href="calculadora-cliente.html">Calculator & Prices</a>
    <a class="font-headline-md text-headline-md uppercase tracking-wider text-on-surface-variant hover:text-primary transition-colors mobile-link" href="condiciones.html">Conditions</a>
    <a class="font-headline-md text-headline-md uppercase tracking-wider text-on-surface-variant hover:text-primary transition-colors mobile-link" href="index.html#ubicacion">Location</a>
  </nav>
  <div class="mt-auto pt-space-xl">
    <a class="w-full inline-flex items-center justify-center px-space-md py-space-sm rounded-lg bg-gradient-to-r from-gold-light via-primary-container to-gold-muted text-on-primary font-label-lg text-label-lg shadow-xl" href="https://api.whatsapp.com/send/?phone=573138934136&text=Hola%2C+estoy+interesado+en+los+servicios+vistos+en+la+web&type=phone_number&app_absent=0" target="_blank">Book Appointment</a>
  </div>
</div>
'''
    else:
        menu_html = '''</header>
<!-- Mobile Menu Overlay -->
<div id="mobileMenu" class="fixed inset-0 z-40 bg-surface-base/98 backdrop-blur-3xl transform translate-x-full transition-transform duration-300 xl:hidden flex flex-col pt-24 px-margin-mobile pb-space-lg overflow-y-auto">
  <div class="flex justify-between items-center mb-space-xl">
    <span class="font-headline-sm text-headline-sm tracking-wider uppercase text-ivory-white">Menú</span>
    <button id="closeMenuBtn" class="p-2 text-on-surface-variant hover:text-ivory-white rounded-lg bg-surface-container">
      <span class="material-symbols-outlined text-[24px]">close</span>
    </button>
  </div>
  <nav class="flex flex-col gap-space-lg" data-active-classes="text-primary font-label-lg">
    <a class="font-headline-md text-headline-md uppercase tracking-wider text-on-surface-variant hover:text-primary transition-colors mobile-link" href="index.html">Inicio</a>
    <a class="font-headline-md text-headline-md uppercase tracking-wider text-on-surface-variant hover:text-primary transition-colors mobile-link" href="index.html#servicios">Servicios</a>
    <a class="font-headline-md text-headline-md uppercase tracking-wider text-on-surface-variant hover:text-primary transition-colors mobile-link" href="calculadora-cliente.html">Calculadora y Precios</a>
    <a class="font-headline-md text-headline-md uppercase tracking-wider text-on-surface-variant hover:text-primary transition-colors mobile-link" href="condiciones.html">Condiciones</a>
    <a class="font-headline-md text-headline-md uppercase tracking-wider text-on-surface-variant hover:text-primary transition-colors mobile-link" href="index.html#ubicacion">Ubicación</a>
  </nav>
  <div class="mt-auto pt-space-xl">
    <a class="w-full inline-flex items-center justify-center px-space-md py-space-sm rounded-lg bg-gradient-to-r from-gold-light via-primary-container to-gold-muted text-on-primary font-label-lg text-label-lg shadow-xl" href="https://api.whatsapp.com/send/?phone=573138934136&text=Hola%2C+estoy+interesado+en+los+servicios+vistos+en+la+web&type=phone_number&app_absent=0" target="_blank">Agendar Cita</a>
  </div>
</div>
'''
    
    content = content.replace("</header>", menu_html)

    # 3. Inject JS Logic
    js_code = '''
<!-- Mobile Menu Script -->
<script>
  document.addEventListener('DOMContentLoaded', () => {
    const mobileMenuBtn = document.getElementById('mobileMenuBtn');
    const closeMenuBtn = document.getElementById('closeMenuBtn');
    const mobileMenu = document.getElementById('mobileMenu');
    const mobileLinks = document.querySelectorAll('.mobile-link');
    
    if (mobileMenuBtn && closeMenuBtn && mobileMenu) {
      mobileMenuBtn.addEventListener('click', () => {
        mobileMenu.classList.remove('translate-x-full');
      });
      
      closeMenuBtn.addEventListener('click', () => {
        mobileMenu.classList.add('translate-x-full');
      });
      
      mobileLinks.forEach(link => {
        link.addEventListener('click', () => {
          mobileMenu.classList.add('translate-x-full');
        });
      });
    }
  });
</script>
</body>'''
    content = content.replace("</body>", js_code)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Added mobile menu to {filepath}")

for f in glob.glob("*.html") + glob.glob("en/*.html"):
    process_file(f)
