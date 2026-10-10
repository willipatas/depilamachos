import re
import os

filepath = 'en/price-list.html'
if os.path.exists(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Spanish text was literally used in the English file
    content = content.replace('¿Máquina al Ras?', 'Máquina eléctrica')
    content = content.replace('Recorte pulcro al ras dérmico sin tirones ni irritación folicular.', 'Se pueden usar guías para dejar algo de largo o hacer un recorte pulcro sin tirones ni irritación folicular.')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
