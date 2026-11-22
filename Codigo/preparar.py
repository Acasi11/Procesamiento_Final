"""Ensambla los recursos locales para el ejecutable. Ejecutar desde Codigo/."""
from pathlib import Path
from PIL import Image
import base64, json
from ejemplos import CASOS

base = Path(__file__).resolve().parent
def recurso(nombre):
    with Image.open(base.parent/'Datos'/f'{nombre}.png') as im:
        return base64.b64encode(im.convert('L').tobytes()).decode('ascii')
datos = [[recurso(ref), recurso(obs)] for _, ref, obs in CASOS]
html = (base/'interfaz.html').read_text(encoding='utf8').replace('/*FFT*/', (base/'filtro.js').read_text(encoding='utf8')).replace('/*DATA*/', json.dumps(datos))
pagina = html.encode('utf8')
# Cadenas contiguas en C, con bytes escapados en octal para conservar UTF-8.
def escapar(b):
    return chr(b) if 32<=b<127 and b not in (34,92,63) else f'\\{b:03o}'
lineas=['"'+''.join(escapar(b) for b in pagina[i:i+256])+'"' for i in range(0,len(pagina),256)]
(base/'interfaz.inc').write_text('static const char pagina[] =\n'+'\n'.join(lineas)+';\n',encoding='ascii')
