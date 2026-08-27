#!/usr/bin/env python3
"""Extracao mecanica da Fig. 5(c) do PRL 135, 086701 (2025).
Renderizar antes:
  pdftoppm -png -r 500 -f 8 -l 8 -x 2200 -y 3120 -W 1000 -H 1020 c2y9-3cc9.pdf fig5c_full
Metodo: deteccao por cor. Banda estavel = azul-acinzentado; tracejado = branco DENTRO do azul.
Rejeicao do texto branco da legenda: so colunas com EXATAMENTE UM run branco fino (3-13 px).
Calibracao: moldura em x=[149,807], y=[112(K0=1.0), 758(K0=0.0)]; ticks x em px 240..807 = 0.02..0.12.
Nenhum parametro foi ajustado para produzir concordancia; os valores do saf.cu ja estavam
publicados em RELEASE-R002.md antes desta extracao."""
import sys, numpy as np, matplotlib.image as mpimg
im=mpimg.imread(sys.argv[1] if len(sys.argv)>1 else 'fig5c_full-8.png')
im=(im[:,:,:3]*255).astype(np.uint8) if im.dtype!=np.uint8 else im[:,:,:3]
r,g,b=[im[:,:,i].astype(int) for i in range(3)]
X0,X1,YT,YB=149,807,112,758
K=lambda py:(YB-py)/(YB-YT); Ai=lambda px:0.000176233*px-0.0222286
blue=(b>r+18)&(b>110)&(b<205)&(r>80)&(r<160); white=(r>225)&(g>225)&(b>225)
pts=[];lows=[];ups=[]
for px in range(X0+2,X1-1):
    ys=np.where(blue[:,px])[0]
    if len(ys)<20: continue
    lows.append((Ai(px),K(ys.max()))); ups.append((Ai(px),K(ys.min())))
    w=[y for y in range(ys.min(),ys.max()+1) if white[y,px]]
    if not w: continue
    runs=[];cur=[w[0]]
    for y in w[1:]:
        if y-cur[-1]<=2: cur.append(y)
        else: runs.append(cur); cur=[y]
    runs.append(cur)
    thin=[q for q in runs if 3<=len(q)<=13]
    if len(runs)==1 and len(thin)==1: pts.append((Ai(px),K(int(np.mean(thin[0])))))
def fit(p):
    a=np.array([x[0] for x in p]); k=np.array([x[1] for x in p]); return np.polyfit(a,k,1),a
(cd,ad)=fit(pts); (cl,_)=fit(lows); (cu,_)=fit(ups)
print(f"tracejado    K0 = {cd[0]:+.3f}*Aint + {cd[1]:.4f}   ({len(pts)} pts, Aint {ad.min():.4f}..{ad.max():.4f})")
print(f"banda inf    K0 = {cl[0]:+.3f}*Aint + {cl[1]:.4f}")
print(f"banda sup    K0 = {cu[0]:+.3f}*Aint + {cu[1]:.4f}")
cc=[(cl[0]+cu[0])/2,(cl[1]+cu[1])/2]
print(f"centro       K0 = {cc[0]:+.3f}*Aint + {cc[1]:.4f}      Eq.(S1): -2.500*Aint + 0.6500")
print(f"ultimo dash desenhado em Aint = {ad.max():.4f}  (eixo vai ate 0.120)")
