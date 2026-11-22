"""Reconstruye las entradas adicionales y los indicadores para los tres casos."""
from pathlib import Path
import csv
import numpy as np
from PIL import Image
from restaurar import psnr

ROOT = Path(__file__).resolve().parents[1]
CASOS = [('carta', 'original', 'borrosa'), ('estrella', 'estrella', 'estrella_entrada'),
         ('retrato', 'retrato', 'retrato_entrada')]
def leer(nombre):
    return np.asarray(Image.open(ROOT/'Datos'/f'{nombre}.png').convert('L')) / 255
def cuantizar(a):
    return np.rint(np.clip(a, 0, 1)*255)/255
def guardar(nombre, a):
    Image.fromarray(np.uint8(np.rint(a*255))).save(ROOT/'Datos'/f'{nombre}.png')
def respuesta():
    d=np.minimum(np.arange(256),256-np.arange(256))
    h=np.exp(-(d[:,None]**2+d[None,:]**2)/8)
    return np.fft.fft2(h/h.sum())
def restaurada(obs,H,k):
    return cuantizar(np.fft.ifft2(H.conj()*np.fft.fft2(obs)/(abs(H)**2+k)).real)
def main():
    y,x=np.mgrid[-128:128,-128:128]
    estrella=np.where(np.hypot(x,y)<107,np.where(np.cos(24*np.arctan2(y,x))>0,.84,.16),.5)
    guardar('estrella',cuantizar(estrella))
    H=respuesta()
    rows=[]
    for caso,ref,entrada in CASOS:
        a=leer(ref)
        if caso!='carta':
            ruido=np.random.default_rng(42).normal(0,.01,a.shape)
            guardar(entrada,cuantizar(np.fft.ifft2(H*np.fft.fft2(a)).real+ruido))
        b=leer(entrada)
        for k in (.0001,.001,.01,.1):
            c=restaurada(b,H,k)
            rows.append([caso,k,psnr(a,b),psnr(a,c),psnr(a,c)-psnr(a,b)])
    with (ROOT/'Resultados'/'comparacion.csv').open('w',newline='',encoding='utf-8') as f:
        writer=csv.writer(f)
        writer.writerow(['caso','K','entrada_dB','restaurada_dB','cambio_dB'])
        writer.writerows(rows)
if __name__=='__main__':
    main()
