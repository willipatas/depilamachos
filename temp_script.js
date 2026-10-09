<script>
  (function() {
    // Data structures corresponding precisely to the user's Hostinger calculator logic
    const DYNAMIC_PRICES = {
      espalda: {
        completa: { cera: 46000, maquina: 23000, presto: 33000, label: 'Espalda Completa' },
        alta: { cera: 28000, maquina: 14000, presto: 20000, label: 'Espalda (Solo Alta)' },
        baja: { cera: 18000, maquina: 9000, presto: 13000, label: 'Espalda (Solo Baja)' }
      },
      brazos: {
        completos: { cera: 60000, maquina: 30000, presto: 42000, label: 'Brazos Completos' },
        mitad: { cera: 30000, maquina: 15000, presto: 21000, label: 'Mitad Brazo' }
      },
      piernas: {
        completas: { cera: 68000, maquina: 34000, presto: 48000, label: 'Piernas Completas' },
        mitad: { cera: 34000, maquina: 17000, presto: 24000, label: 'Media Pierna' }
      }
    };

    // Current variant state for dynamic zones
    const currentVariants = {
      espalda: 'completa',
      brazos: 'completos',
      piernas: 'completas'
    };

    // Format currency COP
    function formatCOP(num) {
      return '$' + Number(num).toLocaleString('es-CO');
    }

    // Refresh dynamic cards price text
    function updateDynamicCardsDisplay() {
      // Espalda
      const espPrices = DYNAMIC_PRICES.espalda[currentVariants.espalda];
      document.getElementById('price-espalda-cera').textContent = formatCOP(espPrices.cera);
      document.getElementById('price-espalda-maquina').textContent = formatCOP(espPrices.maquina);
      document.getElementById('price-espalda-presto').textContent = formatCOP(espPrices.presto);

      // Brazos
      const brzPrices = DYNAMIC_PRICES.brazos[currentVariants.brazos];
      document.getElementById('price-brazos-cera').textContent = formatCOP(brzPrices.cera);
      document.getElementById('price-brazos-maquina').textContent = formatCOP(brzPrices.maquina);
      document.getElementById('price-brazos-presto').textContent = formatCOP(brzPrices.presto);

      // Piernas
      const prnPrices = DYNAMIC_PRICES.piernas[currentVariants.piernas];
      document.getElementById('price-piernas-cera').textContent = formatCOP(prnPrices.cera);
      document.getElementById('price-piernas-maquina').textContent = formatCOP(prnPrices.maquina);
      document.getElementById('price-piernas-presto').textContent = formatCOP(prnPrices.presto);
    }

    // Elements
    const totalDisplay = document.getElementById('totalDisplay');
    const badgeCount = document.getElementById('badgeCount');
    const selectedItemsContainer = document.getElementById('selectedItemsContainer');
    const emptySummaryMessage = document.getElementById('emptySummaryMessage');
    const rawMessageTextarea = document.getElementById('rawMessageTextarea');
    const btnWhatsapp = document.getElementById('btnWhatsapp');
    const checkMasaje = document.getElementById('checkMasaje');
    const btnResetAll = document.getElementById('btnResetAll');
    const btnCopyClipboard = document.getElementById('copyText');
    const copyIcon = document.getElementById('copyIcon');
    const copyButton = document.getElementById('btnCopyClipboard');
    const btnToggleRawText = document.getElementById('btnToggleRawText');
    const rawTextContainer = document.getElementById('rawTextContainer');
    const toggleIcon = document.getElementById('toggleIcon');

    // Toggle logic for radio buttons (clicking an already selected radio unchecks it)
    const radioInputs = document.querySelectorAll('input[type="radio"]');
    radioInputs.forEach(radio => {
      radio.addEventListener('click', function(e) {
        if (this.dataset.waschecked === 'true') {
          this.checked = false;
          this.dataset.waschecked = 'false';
        } else {
          // Clear waschecked flag for others in same group
          const siblings = document.querySelectorAll(`input[name="${this.name}"]`);
          siblings.forEach(s => s.dataset.waschecked = 'false');
          this.dataset.waschecked = 'true';
        }
        recalculate();
      });
    });

    // Variant selector pill clicks
    document.querySelectorAll('[data-variant-btn]').forEach(btn => {
      btn.addEventListener('click', function() {
        const group = this.getAttribute('data-variant-btn');
        const variant = this.getAttribute('data-variant');
        
        // Update active class
        const siblings = document.querySelectorAll(`[data-variant-btn="${group}"]`);
        siblings.forEach(s => {
          s.classList.remove('bg-primary', 'text-on-primary', 'active');
          s.classList.add('text-on-surface-variant');
        });
        this.classList.add('bg-primary', 'text-on-primary', 'active');
        this.classList.remove('text-on-surface-variant');

        currentVariants[group] = variant;
        updateDynamicCardsDisplay();
        recalculate();
      });
    });

    // Masaje checkbox change
    if (checkMasaje) {
      checkMasaje.addEventListener('change', recalculate);
    }

    // Reset button
    if (btnResetAll) {
      btnResetAll.addEventListener('click', function() {
        radioInputs.forEach(r => {
          r.checked = false;
          r.dataset.waschecked = 'false';
        });
        if (checkMasaje) checkMasaje.checked = false;
        recalculate();
      });
    }

    // Toggle Raw Text
    if (btnToggleRawText) {
      btnToggleRawText.addEventListener('click', function() {
        const isHidden = rawTextContainer.classList.contains('hidden');
        if (isHidden) {
          rawTextContainer.classList.remove('hidden');
          toggleIcon.textContent = 'expand_less';
        } else {
          rawTextContainer.classList.add('hidden');
          toggleIcon.textContent = 'expand_more';
        }
      });
    }

    // Copy to clipboard
    if (copyButton) {
      copyButton.addEventListener('click', function() {
        const textToCopy = rawMessageTextarea.value;
        if (!textToCopy) return;

        navigator.clipboard.writeText(textToCopy).then(() => {
          const originalText = btnCopyClipboard.textContent;
          btnCopyClipboard.textContent = '¡Copiado con éxito!';
          copyIcon.textContent = 'check';
          copyButton.classList.add('bg-secondary-container', 'text-secondary-fixed');
          setTimeout(() => {
            btnCopyClipboard.textContent = originalText;
            copyIcon.textContent = 'content_copy';
            copyButton.classList.remove('bg-secondary-container', 'text-secondary-fixed');
          }, 2400);
        });
      });
    }

    // Main Recalculate Engine
    function recalculate() {
      let total = 0;
      let count = 0;

      const groupedByTechnique = {
        cera: [],
        maquina: [],
        presto: []
      };

      // 1. Process Dynamic Zones
      ['espalda', 'brazos', 'piernas'].forEach(key => {
        const checkedRadio = document.querySelector(`input[name="zona-${key}"]:checked`);
        if (checkedRadio) {
          count++;
          const tech = checkedRadio.value;
          const varObj = DYNAMIC_PRICES[key][currentVariants[key]];
          const price = varObj[tech];
          total += price;
          groupedByTechnique[tech].push({
            name: varObj.label,
            price: price
          });
        }
      });

      // 2. Process Static Zones
      ['axilas', 'pecho', 'abdomen', 'pubis', 'escroto', 'gluteos', 'perianal', 'manos', 'pies'].forEach(key => {
        const checkedRadio = document.querySelector(`input[name="zona-${key}"]:checked`);
        if (checkedRadio) {
          count++;
          const tech = checkedRadio.value;
          const zoneName = checkedRadio.getAttribute('data-zone');
          const price = Number(checkedRadio.getAttribute('data-price'));
          total += price;
          groupedByTechnique[tech].push({
            name: zoneName,
            price: price
          });
        }
      });

      // 3. Process Masaje
      const hasMasaje = checkMasaje && checkMasaje.checked;
      if (hasMasaje) {
        count++;
        total += 80000;
      }

      // Update counters y total
      totalDisplay.textContent = formatCOP(total);
      badgeCount.textContent = count === 1 ? '1 servicio' : `${count} servicios`;

      // Update dynamic summary HTML list
      renderSummaryCards(groupedByTechnique, hasMasaje);

      // Generate WhatsApp y Copy message
      generateMessage(groupedByTechnique, hasMasaje, total);
    }

    function renderSummaryCards(groups, hasMasaje) {
      selectedItemsContainer.innerHTML = '';
      const totalItems = groups.cera.length + groups.maquina.length + groups.presto.length + (hasMasaje ? 1 : 0);

      if (totalItems === 0) {
        if (emptySummaryMessage) {
          selectedItemsContainer.appendChild(emptySummaryMessage);
        }
        return;
      }

      const techTitles = {
        cera: 'Cera Tibia',
        maquina: 'Máquina al Ras / Eléctrica',
        presto: 'PrestoBarba'
      };

      ['cera', 'maquina', 'presto'].forEach(techKey => {
        const items = groups[techKey];
        if (items.length > 0) {
          items.forEach(item => {
            const card = document.createElement('div');
            card.className = 'flex items-center justify-between p-space-xs px-space-sm rounded-lg bg-surface-container text-body-sm';
            card.innerHTML = `
              <div class="flex flex-col">
                <span class="text-ivory-white font-label-md">${item.name}</span>
                <span class="text-outline text-label-sm">${techTitles[techKey]}</span>
              </div>
              <span class="relative z-10 font-label-md text-primary font-semibold">${formatCOP(item.price)}</span>
            `;
            selectedItemsContainer.appendChild(card);
          });
        }
      });

      if (hasMasaje) {
        const mCard = document.createElement('div');
        mCard.className = 'flex items-center justify-between p-space-xs px-space-sm rounded-lg bg-surface-overlay text-body-sm ring-1 ring-primary/20';
        mCard.innerHTML = `
          <div class="flex flex-col">
            <span class="text-ivory-white font-label-md">Masaje Relajante Integral</span>
            <span class="text-secondary text-label-sm">Sesión 60 Minutos</span>
          </div>
          <span class="relative z-10 font-label-md text-gold-light font-semibold">${formatCOP(80000)}</span>
        `;
        selectedItemsContainer.appendChild(mCard);
      }
    }

    function generateMessage(groups, hasMasaje, total) {
      let lines = [];
      let hasAny = false;
      lines.push('Hola, quiero agendar una cita con la siguiente cotización:');
      lines.push('');
      lines.push('*Zonas a depilar*');
      lines.push('──────────────────────');

      if (groups.cera.length > 0) {
        hasAny = true;
        lines.push('*Cera*');
        groups.cera.forEach(it => {
          lines.push(`• *${it.name}*: ${formatCOP(it.price)}`);
        });
        lines.push('');
      }

      if (groups.maquina.length > 0) {
        hasAny = true;
        lines.push('*Máquina eléctrica*');
        groups.maquina.forEach(it => {
          lines.push(`• *${it.name}*: ${formatCOP(it.price)}`);
        });
        lines.push('');
      }

      if (groups.presto.length > 0) {
        hasAny = true;
        lines.push('*Prestobarba*');
        groups.presto.forEach(it => {
          lines.push(`• *${it.name}*: ${formatCOP(it.price)}`);
        });
        lines.push('');
      }

      if (hasMasaje) {
        hasAny = true;
        lines.push('• *Masaje Relajante*:  $80.000');
        lines.push('');
      }

      if (!hasAny) {
        rawMessageTextarea.value = 'Hola DepilaMachos, me gustaría recibir asesoría sobre sus servicios de depilación masculina en Bogotá.';
        btnWhatsapp.href = 'https://wa.me/573138934136?text=' + encodeURIComponent(rawMessageTextarea.value);
        return;
      }
      
      if (lines[lines.length - 1] === '') {
        lines.pop();
      }

      lines.push('──────────────────────');
      lines.push(`💰 *TOTAL ESTIMADO:* ${formatCOP(total)} COP`);
      lines.push('──────────────────────');

      const fullMessage = lines.join('\n');
      rawMessageTextarea.value = fullMessage;
      btnWhatsapp.href = 'https://wa.me/573138934136?text=' + encodeURIComponent(fullMessage);
    }

      lines.push(`TOTAL ESTIMADO: ${formatCOP(total)} COP`);
      lines.push('Sede: Marsella, Bogotá D.C.');
      lines.push('¿Qué horarios tienen disponibles?');

      const fullMessage = lines.join('\n');
      rawMessageTextarea.value = fullMessage;
      btnWhatsapp.href = 'https://wa.me/573138934136?text=' + encodeURIComponent(fullMessage);
    }

    // Initial run
    updateDynamicCardsDisplay();
    recalculate();
  })();
</script></main><footer class="w-full bg-surface-container-lowest"><div class="max-w-7xl mx-auto px-margin-mobile lg:px-margin pt-space-xl pb-space-lg"><div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-gutter mb-space-xl"><div class="space-y-space-md"><div class="flex items-center gap-space-sm"><img alt="Logo DepilaMachos" class="h-8 w-auto object-contain" src="https://lh3.googleusercontent.com/aida/AEtjO1UJhzTLwJ634-E0KVv2zzx1P9-xjRXf8q27iJlV4h0JaxZkBDt128SlF7TPbP-V9hOURmkjL1o6XLRjN2i1EDTufpdreGUXjEXQxOi6UsVExhkvpUVW9Hy9QW5Qd8_nygXnI1ZF2f9m2zztATWHO_n8szi4QPqH3tG6L9kCn472IFSn4U9ba3QZfY8JFKYH477BX-0Hkj5WdhDnTw2AT19kSD6vg8aBsxSqeswQrZ_hug0ZRmYJjPhOjA"/><span class="font-headline-sm text-headline-sm text-ivory-white uppercase">DepilaMachos</span></div><p class="font-body-sm text-body-sm text-on-surface-variant">Estudio exclusivo de depilación masculina y bienestar y relajación. Discreción, maestría y confort absoluto en Marsella, Bogotá.</p><div class="inline-flex items-center gap-space-xs px-space-sm py-space-xs rounded-lg bg-emerald-accent/60 text-secondary"><span class="material-symbols-outlined text-[16px]">lock</span><span class="relative z-10 font-label-sm text-label-sm uppercase tracking-wider">Privacidad 100% Garantizada</span></div></div><div class="space-y-space-sm"><h3 class="font-label-lg text-label-lg uppercase tracking-wider text-primary">Estudio de Depilación Bogotá</h3><div class="flex items-start gap-space-sm text-on-surface-variant"><span class="material-symbols-outlined text-primary text-[20px]">location_on</span><div class="font-body-sm text-body-sm"><p class="text-ivory-white font-label-md text-label-md">Sede Marsella</p><p class="">Barrio Marsella, Bogotá D.C., Colombia</p><p class="text-outline font-label-sm text-label-sm mt-space-xs">Atención con cita previa</p></div></div><div class="flex items-center gap-space-sm text-on-surface-variant"><span class="material-symbols-outlined text-primary text-[20px]">schedule</span><span class="font-body-sm text-body-sm">Lun - Sáb: 10:00 AM - 6:00 PM</span></div></div><div class="space-y-space-sm"><h3 class="font-label-lg text-label-lg uppercase tracking-wider text-primary">Contacto Directo</h3><a class="flex items-center gap-space-sm text-on-surface-variant hover:text-primary transition-colors" href="https://api.whatsapp.com/send/?phone=573138934136&text=Hola%2C+estoy+interesado+en+los+servicios+vistos+en+la+web&type=phone_number&app_absent=0" rel="noopener noreferrer" target="_blank"><span class="material-symbols-outlined text-primary text-[20px]">chat</span><span class="font-body-sm text-body-sm">WhatsApp: +57 313 893 4136</span></a><div class="pt-space-xs"><a class="inline-flex items-center gap-space-xs px-space-md py-space-sm rounded-lg bg-surface-card hover:bg-surface-container text-ivory-white font-label-md text-label-md transition-colors" href="https://api.whatsapp.com/send/?phone=573138934136&text=Hola%2C+estoy+interesado+en+los+servicios+vistos+en+la+web&type=phone_number&app_absent=0" rel="noopener noreferrer" target="_blank"><span class="material-symbols-outlined text-primary text-[18px]">calendar_month</span><span class="">Reservar por Chat</span></a></div></div><div class="space-y-space-sm"><h3 class="font-label-lg text-label-lg uppercase tracking-wider text-primary">Enlaces y Confianza</h3><ul class="space-y-space-xs"><li class="font-body-sm text-body-sm text-on-surface-variant"><a class="hover:text-on-surface transition-colors" data-path="servicios" href="index.html#servicios">Menú de Servicios</a></li><li class="font-body-sm text-body-sm text-on-surface-variant"><a class="hover:text-on-surface transition-colors" data-path="lista-de-precios" href="lista-de-precios.html">Calculadora de Paquetes</a></li><li class="font-body-sm text-body-sm text-on-surface-variant"><a class="hover:text-on-surface transition-colors" data-path="condiciones" href="condiciones.html">Protocolo de Higiene y Citas</a></li><li class="font-body-sm text-body-sm text-on-surface-variant"><a class="hover:text-on-surface transition-colors" data-path="ubicacion" href="index.html#ubicacion">Cómo Llegar</a></li></ul><div class="flex items-center gap-space-sm pt-space-xs">
<script>
document.addEventListener('DOMContentLoaded', () => {
    const params = new URLSearchParams(window.location.search);
    const zones = params.get('select');
    if (zones) {
        const zoneList = zones.split(',');
        let scrolled = false;
        
        // Wait a small amount for UI to initialize
        setTimeout(() => {
            zoneList.forEach(z => {
                const radio = document.querySelector(`input[name="zona-${z}"][value="cera"]`) || 
                              document.querySelector(`input[name="zona-${z}"]`);
                if (radio) {
                    
                    radio.click();
                    if (!scrolled) {
                        radio.scrollIntoView({behavior: 'smooth', block: 'center'});
                        scrolled = true;
                    }
                }
            });
        }, 300);
    }
});
</script>
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
