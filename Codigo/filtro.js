// FFT radix 2 in situ. Las dos matrices contienen las partes real e imaginaria.
function fft(re, im, inversa) {
  const n = re.length;
  for (let i = 1, j = 0; i < n; i++) {
    let bit = n >> 1;
    while (j & bit) { j ^= bit; bit >>= 1; }
    j ^= bit;
    if (i < j) {
      [re[i], re[j]] = [re[j], re[i]];
      [im[i], im[j]] = [im[j], im[i]];
    }
  }
  for (let m = 2; m <= n; m *= 2) {
    for (let j = 0; j < m/2; j++) {
      const a = (inversa ? 2 : -2)*Math.PI*j/m;
      const c = Math.cos(a), s = Math.sin(a);
      for (let i = j; i < n; i += m) {
        const k = i+m/2, u = c*re[k]-s*im[k], v = s*re[k]+c*im[k];
        re[k]=re[i]-u; im[k]=im[i]-v; re[i]+=u; im[i]+=v;
      }
    }
  }
  if (inversa) for (let i=0;i<n;i++) {re[i]/=n; im[i]/=n;}
}
function fft2(re,im,n,inversa=false) {
  // Una pasada por filas y otra por columnas.
  for (const vertical of [false,true]) {
    for (let i=0;i<n;i++) {
      const indices=Array.from({length:n},(_,j)=>vertical?j*n+i:i*n+j);
      const r=indices.map(k=>re[k]), b=indices.map(k=>im[k]);
      fft(r,b,inversa);
      indices.forEach((k,j)=>{re[k]=r[j];im[k]=b[j];});
    }
  }
}
function restaurar(datos,n,K) {
  const g=Float64Array.from(datos,v=>v/255), gi=new Float64Array(n*n);
  const h=new Float64Array(n*n), hi=new Float64Array(n*n);
  let suma=0;
  for(let y=0;y<n;y++) for(let x=0;x<n;x++){
    const dx=Math.min(x,n-x),dy=Math.min(y,n-y);
    h[y*n+x]=Math.exp(-(dx*dx+dy*dy)/8); suma+=h[y*n+x];
  }
  for(let i=0;i<h.length;i++) h[i]/=suma;
  fft2(g,gi,n); fft2(h,hi,n);
  for(let i=0;i<g.length;i++) {
    const den=h[i]**2+hi[i]**2+K;
    const r=(g[i]*h[i]+gi[i]*hi[i])/den;
    gi[i]=(gi[i]*h[i]-g[i]*hi[i])/den; g[i]=r;
  }
  fft2(g,gi,n,true);
  return Uint8Array.from(g,v=>Math.round(255*Math.max(0,Math.min(1,v))));
}
