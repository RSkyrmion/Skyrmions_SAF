#!/usr/bin/env python3
"""E002 §2 — extrai os alvos v_perp(t) da Fig. 2(a),(b) do PRL 135, 086701.

Rodado ANTES de qualquer corrida de dinamica do E002. Calibracao pelos pixels
dos ticks dos eixos (detectados, nao chutados); curvas por mascara de cor.
Uso:  python3 LAB/EVIDENCE/E002/extract_fig2.py <pagina3.png>
"""
import sys
import numpy as np
from PIL import Image

im = np.array(Image.open(sys.argv[1]).convert("RGB")).astype(int)
R, G, B = im[:, :, 0], im[:, :, 1], im[:, :, 2]
orange = (R > 190) & (G > 80) & (G < 175) & (B < 90)     # v_perp
blue   = (R < 110) & (G > 90) & (G < 170) & (B > 140)    # v_par
dark   = (im.sum(2) < 450)

# --- calibracao: molduras e ticks, detectados na imagem -----------------------
# molduras: linhas escuras que atravessam a largura do painel
seg = dark[:1000, 213:692].sum(1)
frames = [y for y in range(120, 700) if seg[y] > 430]
# ticks do eixo x: marcas ABAIXO da moldura inferior do painel (b)
xt = dark[636:648, :].sum(0)
xticks = [x for x in range(200, 700) if xt[x] >= 5]
# ticks do eixo y: marcas a ESQUERDA do eixo
yt = dark[:1000, 203:213].sum(1)
yticks = [y for y in range(125, 700) if yt[y] >= 5]

print("molduras y =", frames)
print("ticks x    =", xticks)
print("ticks y    =", yticks)

X0, X1, T0, T1 = 213.5, 691.0, 0.0, 200.0          # eixo t: 0..200 ns
PANELS = {                                          # (ytop, ybot, ypix0, val0, ypix1, val1)
    "a_SBM_18GHz":   (132, 366, 339.0, 0.0, 159.0, 20.0),   # cm/s
    "b_ABM_19.24GHz": (401, 635, 616.5, 0.0, 429.0,  2.0),  # cm/s
}
MASK_INSET = {  # o inset de cada painel e' excluido do tracado
    "a_SBM_18GHz":    lambda x, y: (x > 320 and y < 250),
    "b_ABM_19.24GHz": lambda x, y: (x > 320 and 430 < y < 560),
}

def trace(mask, ytop, ybot, yp0, v0, yp1, v1, skip):
    out = []
    for x in range(214, 691):
        ys = [y for y in range(ytop + 1, ybot) if mask[y, x] and not skip(x, y)]
        if not ys:
            continue
        y = float(np.mean(ys))
        out.append((T0 + (x - X0) * (T1 - T0) / (X1 - X0),
                    v0 + (y - yp0) * (v1 - v0) / (yp1 - yp0)))
    return np.array(out)

for name, geo in PANELS.items():
    ytop, ybot, yp0, v0, yp1, v1 = geo
    px_per_unit = abs(yp1 - yp0) / abs(v1 - v0)
    for lab, mask in (("v_perp", orange), ("v_par", blue)):
        arr = trace(mask, ytop, ybot, yp0, v0, yp1, v1, MASK_INSET[name])
        tail = arr[arr[:, 0] > 180]
        print(f"{name:16s} {lab:6s}  n={len(arr):4d}  "
              f"plato(t>180ns) = {tail[:,1].mean():8.4f} cm/s  "
              f"[{tail[:,1].min():.4f}, {tail[:,1].max():.4f}]  "
              f"1px = {1/px_per_unit:.4f} cm/s")
        np.savetxt(f"LAB/EVIDENCE/E002/fig2_{name}_{lab}.dat", arr,
                   header="t[ns] v[cm/s]  (extraido da Fig.2 por extract_fig2.py)")
