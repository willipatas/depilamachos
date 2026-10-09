import re
import os

def fix_admin(filepath):
    if not os.path.exists(filepath): return
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    new_fn = """function generateFormattedSummary(calculatedTotal) {
        let total = calculatedTotal !== undefined ? calculatedTotal : 0;
        if (calculatedTotal === undefined) {
          Object.values(state.zones).forEach(z => {
            if (z.active) total += (z.customPrice !== null ? z.customPrice : z.basePrice);
          });
          if (state.massage) total += 80000;
        }

        let lines = [];
        if (state.clientNote) {
          lines.push(`*Cliente:* ${state.clientNote}`);
          lines.push('');
        }
        
        lines.push('*Zonas a depilar*');
        lines.push('──────────────────────');

        const groups = {
            'Cera': [],
            'Máquina eléctrica': [],
            'Prestobarba': [],
            'Personalizado': []
        };

        let hasItems = false;
        Object.values(state.zones).forEach(z => {
          if (z.active) {
            hasItems = true;
            const price = z.customPrice !== null ? z.customPrice : z.basePrice;
            const variantTxt = z.variant ? ` (${z.variant})` : '';
            let t = z.technique ? z.technique : 'Personalizado';
            if (t === 'Máquina' || t === 'Máq.') t = 'Máquina eléctrica';
            if (t === 'Presto') t = 'Prestobarba';
            if (!groups[t]) groups[t] = [];
            groups[t].push(`• *${z.name}${variantTxt}*: ${formatCOP(price)}`);
          }
        });

        const order = ['Cera', 'Máquina eléctrica', 'Prestobarba', 'Personalizado'];
        order.forEach(tech => {
            if (groups[tech] && groups[tech].length > 0) {
                lines.push(`*${tech}*`);
                groups[tech].forEach(item => lines.push(item));
                lines.push('');
            }
        });
        
        Object.keys(groups).forEach(tech => {
            if (!order.includes(tech) && groups[tech] && groups[tech].length > 0) {
                lines.push(`*${tech}*`);
                groups[tech].forEach(item => lines.push(item));
                lines.push('');
            }
        });

        if (state.massage) {
          hasItems = true;
          lines.push('• *Masaje Relajante*:  $80.000');
          lines.push('');
        }

        if (!hasItems) {
          lines.push('• (Sin zonas seleccionadas)');
          lines.push('');
        }

        if (lines[lines.length - 1] === '') {
            lines.pop();
        }

        lines.push('──────────────────────');
        lines.push(`💰 *TOTAL ESTIMADO:* ${formatCOP(total)} COP`);
        lines.push('──────────────────────');

        return lines.join('\\n');
      }"""
      
    # Match the old function
    pattern = re.compile(r'function generateFormattedSummary\(calculatedTotal\).*?return lines\.join\(\'\\n\'\);\s*\}', re.DOTALL)
    
    if pattern.search(content):
        content = pattern.sub(new_fn, content)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {filepath}")
    else:
        print(f"Could not find generateFormattedSummary in {filepath}")

def fix_client(filepath):
    if not os.path.exists(filepath): return
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    new_fn = """function generateMessage(groups, hasMasaje, total) {
      let lines = [];
      let hasAny = false;
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

      const fullMessage = lines.join('\\n');
      rawMessageTextarea.value = fullMessage;
      btnWhatsapp.href = 'https://wa.me/573138934136?text=' + encodeURIComponent(fullMessage);
    }"""
    
    # Match the old function
    pattern = re.compile(r'function generateMessage\(groups, hasMasaje, total\).*?btnWhatsapp\.href = [^}]+\}\n', re.DOTALL)
    
    if pattern.search(content):
        content = pattern.sub(new_fn + '\n', content)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {filepath}")
    else:
        print(f"Could not find generateMessage in {filepath}")

fix_admin('preciosadmin.html')
fix_admin('en/preciosadmin.html')
fix_client('lista-de-precios.html')
fix_client('en/price-list.html')
