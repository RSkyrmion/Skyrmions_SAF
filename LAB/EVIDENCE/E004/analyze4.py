#!/usr/bin/env python3
"""MISSION-E004 — v_sp(f), contra os criterios PRE-REGISTRADOS (+ ADENDO-001).

ESCRITO ANTES DO LOTE. Nenhuma escolha de analise foi feita depois de ver o dado.
Uso: python3 LAB/EVIDENCE/E004/analyze4.py
"""
import numpy as np

FREQS = [16.5, 17.0, 17.5, 17.75, 18.00, 18.25, 18.5, 19.0, 19.5]
# 18.00 vem do E002 (mesma condicao, theta=0, mesma janela). Os outros sao do E004.
SRC = {18.00: "LAB/EVIDENCE/E002/prop_sbm_18.00GHz.dat"}

def path(f):
    return SRC.get(f, f"LAB/EVIDENCE/E004/prop_sbm_{f:.2f}GHz.dat")

def load(f):
    return np.array([[float(x) for x in L.split()] for L in open(path(f))
                     if not L.startswith("#") and len(L.split()) == 16])

def vperp(D, lo, hi):
    t = D[:, 0]
    s = (t >= lo * 1e-9) & (t <= hi * 1e-9)
    vx = np.polyfit(t[s], 0.5 * (D[s, 1] + D[s, 3]), 1)[0]
    vy = np.polyfit(t[s], 0.5 * (D[s, 2] + D[s, 4]), 1)[0]
    return np.hypot(vx, vy) * 100

def parab_peak(x, y):
    """Vertice da parabola pelos 3 pontos em torno do maximo."""
    k = int(np.argmax(y))
    if k == 0 or k == len(y) - 1:
        return None, k
    x0, x1, x2 = x[k-1], x[k], x[k+1]
    y0, y1, y2 = y[k-1], y[k], y[k+1]
    d = (x0-x1)*(x0-x2)*(x1-x2)
    A = (x2*(y1-y0) + x1*(y0-y2) + x0*(y2-y1)) / d
    B = (x2*x2*(y0-y1) + x1*x1*(y2-y0) + x0*x0*(y1-y2)) / d
    return (-B / (2*A) if A != 0 else None), k

print("=" * 74)
print("MISSION-E004 — criterios PRE-REGISTRADOS (+ ADENDO-001)")
print("=" * 74)

WIN = [("25-50 ns", 25, 50), ("50-100 ns", 50, 100)]
tab = {}
print("\n  f[GHz]   v_perp(25-50)   v_perp(50-100)   dispersao entre janelas")
for f in FREQS:
    try:
        D = load(f)
    except OSError:
        print(f"  {f:6.2f}   (ausente)")
        continue
    a, b = vperp(D, 25, 50), vperp(D, 50, 100)
    tab[f] = (a, b)
    print(f"  {f:6.2f}   {a:12.5f}   {b:13.5f}   {abs(a-b)/b*100:8.2f} %")

fs = np.array(sorted(tab))
va = np.array([tab[f][0] for f in fs])
vb = np.array([tab[f][1] for f in fs])

# ---- EF-0 revisto (ADENDO-001 A1): criterio RELATIVO, sem numero importado ----
print("\n--- EF-0 (revisto, ADENDO-001 A1): contraste vs dispersao entre janelas")
for nm, v in [("25-50 ns", va), ("50-100 ns", vb)]:
    contraste = (v.max() - v.min()) / v.max()
    disp = np.mean(np.abs(va - vb) / vb)      # dispersao relativa media entre janelas
    print(f"  {nm:10s} contraste = {contraste*100:.3f} %   dispersao media = {disp*100:.3f} %"
          f"   razao = {contraste/disp:.2f}x   (criterio: > 5x)")
contraste = (vb.max() - vb.min()) / vb.max()
disp = np.mean(np.abs(va - vb) / vb)
ef0 = contraste / disp > 5.0
print(f"  ==> {'curva TEM estrutura; EF-1 pode ter veredito' if ef0 else 'curva PLANA; EF-1 INDETERMINADO'}")

# ---- EF-1: posicao do pico, nas duas janelas, com incerteza (ADENDO-001 A2) ----
print("\n--- EF-1: posicao do pico nas duas janelas (convergencia da grandeza discriminante)")
pk = {}
for nm, v in [("25-50 ns", va), ("50-100 ns", vb)]:
    p, k = parab_peak(fs, v)
    pk[nm] = p
    print(f"  {nm:10s} maximo no ponto {fs[k]:.2f} GHz  ->  f_pico ajustado = "
          f"{'%.4f GHz' % p if p else 'no extremo da grade, sem ajuste'}")
if pk["25-50 ns"] and pk["50-100 ns"]:
    dif = abs(pk["25-50 ns"] - pk["50-100 ns"])
    print(f"  |f_pico(25-50) - f_pico(50-100)| = {dif:.4f} GHz   (criterio §3: <= 0.125)")
    conv = dif <= 0.125
    print(f"  ==> {'CONVERGIDA' if conv else 'NAO CONVERGIDA -> sem veredito; NAO estender (§3)'}")
    # incerteza de f_pico propagando a dispersao entre janelas de cada ponto (A2)
    rng = np.random.default_rng(20260825)
    sig = np.abs(va - vb) / 2.0
    sims = [parab_peak(fs, vb + rng.normal(0, sig))[0] for _ in range(2000)]
    sims = [x for x in sims if x is not None]
    s_pk = np.std(sims)
    print(f"\n  sigma(f_pico) por propagacao da dispersao = {s_pk:.4f} GHz   "
          f"(criterio A2: < 0.25 para haver veredito)")
    if ef0 and conv and s_pk < 0.25:
        d = abs(pk["50-100 ns"] - 18.00)
        print(f"\n  EF-1: |f_pico - 18.00| = {d:.4f} GHz   criterio <= 0.25   -> "
              f"{'PASSOU' if d <= 0.25 else 'FALHOU'}")
    else:
        print("\n  EF-1: INDETERMINADO (EF-0 plano, nao convergido, ou sigma grande)")

# ---- EF-2 ----
print("\n--- EF-2 largura (exploratorio; nao medido se EF-0 declarar plano)")
if ef0:
    half = vb.max() / 2
    above = fs[vb >= half]
    print(f"  pontos acima de meia altura: {above.min():.2f}..{above.max():.2f} GHz")
    print(f"  FWHM (limite inferior pela grade) >= {above.max()-above.min():.2f} GHz")
    print(f"  E001, espectro de breathing SBM: pico 18.00 GHz, resolucao 0.1 GHz")
else:
    print("  NAO MEDIDO: EF-0 declarou a curva plana.")

print("\n--- EF-3 (sem criterio): a curva inteira acima e' o remedio ao EP-3 do E002,")
print("    que tentou localizar ressonancia com dois pontos e falhou.")
