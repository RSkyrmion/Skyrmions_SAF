#!/usr/bin/env python3
"""MISSION-E005 RA-3 — extrai f_pico das tres curvas da Fig. S4(c) do suplementar.

Rodado ANTES de qualquer corrida do E005. Procedimento do E002 §2: render a 200 dpi,
calibrar pelos ticks DETECTADOS, tracar por mascara de cor AMOSTRADA da propria figura.

O eixo y e' logaritmico, mas a posicao do pico nao precisa dele: em eixo log o pixel-y
e' linear em log(v), logo uma parabola em pixel-y E' uma parabola em log(v).
Uso: python3 LAB/EVIDENCE/E005/extract_figS4c.py
"""
import numpy as np
from PIL import Image

IMG = "LAB/EVIDENCE/E005/figS4_p5_rendered.png"
# moldura e ticks: DETECTADOS (ver RUN-LOG), nao chutados
X0, X1, Y0, Y1 = 523, 859, 517, 842
TICK_PX = [523.5, 597.5, 670.5, 745.5, 819.5]
TICK_F = [14.0, 16.0, 18.0, 20.0, 22.0]
CORES = {0.008: (106, 0, 168), 0.004: (195, 61, 128), 0.002: (246, 143, 68)}
LEGENDA = (624, 742, 719, 842)          # caixa a excluir: x0,x1,y0,y1

im = np.array(Image.open(IMG).convert("RGB")).astype(int)
cal = np.polyfit(TICK_PX, TICK_F, 1)
print(f"calibracao: f(x) = {cal[0]:.6f}*x + {cal[1]:.4f}   "
      f"({2/(TICK_PX[1]-TICK_PX[0]):.5f} GHz/px)")


def parab(x, y):
    k = int(np.argmax(y))
    if k == 0 or k == len(y) - 1:
        return None, k
    x0, x1, x2 = x[k-1], x[k], x[k+1]
    y0, y1, y2 = y[k-1], y[k], y[k+1]
    d = (x0-x1)*(x0-x2)*(x1-x2)
    A = (x2*(y1-y0) + x1*(y0-y2) + x0*(y2-y1)) / d
    B = (x2*x2*(y0-y1) + x1*x1*(y2-y0) + x0*x0*(y1-y2)) / d
    return (-B/(2*A) if A else None), k


print("\n  dK/K0   n col   f do pico (grade)   f_pico (parabola em log v)")
alvo = {}
for amp, c in CORES.items():
    m = (np.abs(im[:, :, 0]-c[0]) < 26) & (np.abs(im[:, :, 1]-c[1]) < 26) & \
        (np.abs(im[:, :, 2]-c[2]) < 26)
    m[:Y0, :] = False; m[Y1:, :] = False
    m[:, :X0] = False; m[:, X1:] = False
    m[LEGENDA[2]:LEGENDA[3], LEGENDA[0]:LEGENDA[1]] = False
    xs, ys = [], []
    for x in range(X0, X1):
        col = np.where(m[:, x])[0]
        if len(col):
            xs.append(x); ys.append(col.mean())
    xs = np.array(xs, float); ys = np.array(ys, float)
    f = np.polyval(cal, xs)
    v = -ys                                   # pixel-y invertido = log v crescente
    p, k = parab(f, v)
    alvo[amp] = p
    print(f"  {amp:.3f}   {len(xs):4d}      {f[k]:8.4f}          "
          f"{'%.4f' % p if p else 'no extremo'}")

print("\n--- ALVO SELADO (RA-3), extraido ANTES de qualquer corrida do E005 ---")
for a in sorted(alvo, reverse=True):
    print(f"  dK/K0 = {a:.3f}  ->  f_pico = {alvo[a]:.4f} GHz")
ks = sorted(alvo)
sl = np.polyfit(ks, [alvo[k] for k in ks], 1)[0]
print(f"\n  inclinacao do artigo  df_pico/d(dK/K0) = {sl:+.3f} GHz por unidade")
print(f"  ou seja {sl*(0.008-0.002):+.4f} GHz indo de dK/K0 = 0.002 a 0.008")
print(f"  linha de ressonancia marcada na figura: 18 GHz")
print(f"  nossa f_SBM medida (C-11): 17.9609 +- 0.0125 GHz")
