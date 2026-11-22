"""Experimento reproducible de restauración circular con PSF gaussiana conocida."""
from pathlib import Path
import csv
import numpy as np
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
N = 256

def patron():
    im = Image.new('L', (N,N), 35)
    d = ImageDraw.Draw(im)
    d.rectangle((12,12,243,243), outline=190,width=2)
    for i in range(8):
        d.rectangle((22+i*26,26,47+i*26,65),fill=45+28*i)
    for r in range(52,1,-6):
        d.ellipse((75-r,135-r,75+r,135+r),fill=225 if ((52-r)//6)%2==0 else 50)
    for x in range(143,230,8):
        d.rectangle((x,91,x+3,174),fill=215)
    d.polygon([(27,222),(132,184),(231,222)], fill=180)
    return np.asarray(im)/255.

def guardar(nombre, a):
    Image.fromarray(np.uint8(np.rint(np.clip(a,0,1)*255))).save(ROOT/nombre)

def psnr(a,b):
    return 10*np.log10(1/np.mean((a-b)**2))

def main():
    for folder in ['Datos','Resultados']:
        (ROOT/folder).mkdir(exist_ok=True)
    original=patron()
    # El origen de la PSF está en la esquina para la convolución circular.
    d=np.minimum(np.arange(N), N-np.arange(N))
    kernel=np.exp(-(d[:,None]**2+d[None,:]**2)/(2*2**2))
    H=np.fft.fft2(kernel/kernel.sum())
    blur=np.fft.ifft2(H*np.fft.fft2(original)).real
    rng=np.random.default_rng(42)
    obs=np.rint(np.clip(blur+rng.normal(0,.01,blur.shape),0,1)*255)/255
    guardar('Datos/original.png',original)
    guardar('Datos/borrosa.png',obs)
    # La métrica usa los mismos niveles que las imágenes distribuidas.
    rows=[('Entrada','',psnr(original,obs))]
    for k in [.0001,.001,.01,.1]:
        restored=np.fft.ifft2(np.conj(H)*np.fft.fft2(obs)/(abs(H)**2+k)).real
        restored=np.rint(np.clip(restored,0,1)*255)/255
        guardar(f'Resultados/K_{k}.png',restored)
        rows.append(('Restaurada',k,psnr(original,restored)))
    with (ROOT/'Resultados/metricas.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.writer(f)
        w.writerow(['imagen','K','PSNR_dB'])
        w.writerows(rows)
    print(rows)

if __name__=='__main__':
    main()
