#!/usr/bin/env python3
"""MISSION-E004R — RF-0, RF-0.1, RF-1 exatamente como pre-registrados.

Definicoes fixadas em MISSION-E004R.md §4. Nenhuma escolhida depois do dado.
"""
import numpy as np

FREQS = [17.00, 17.50, 17.75, 18.00, 18.25]
W_EARLY = (150, 225)     # §4 RF-0
W_LATE  = (225, 300)
SEED    = 20260826       # §4 RF-1, fixada no pre-registro
F_SBM, S_FSBM = None, 0.0125   # RF-2; f_SBM medido abaixo

def load(f):
    return np.array([[float(x) for x in L.split()]
                     for L in open(f"LAB/EVIDENCE/E004R/prop_sbm_{f:.2f}GHz.dat")
                     if not L.startswith("#") and len(L.split()) == 16])

def vperp(D, lo, hi):
    t = D[:, 0]
    s = (t >= lo * 1e-9) & (t <= hi * 1e-9)
    vx = np.polyfit(t[s], 0.5 * (D[s, 1] + D[s, 3]), 1)[0]
    vy = np.polyfit(t[s], 0.5 * (D[s, 2] + D[s, 4]), 1)[0]
    return np.hypot(vx, vy) * 100

def parab_peak(x, y):
    k = int(np.argmax(y))
    if k == 0 or k == len(y) - 1:
        return None, k
    x0, x1, x2 = x[k-1], x[k], x[k+1]
    y0, y1, y2 = y[k-1], y[k], y[k+1]
    d = (x0-x1)*(x0-x2)*(x1-x2)
    A = (x2*(y1-y0) + x1*(y0-y2) + x0*(y2-y1)) / d
    B = (x2*x2*(y0-y1) + x1*x1*(y2-y0) + x0*x0*(y1-y2)) / d
    return (-B/(2*A) if A != 0 else None), k

# ---- RF-2: f_SBM do espectro de 40 ns (convencao do spectra.py selado do E001) ----
d = np.loadtxt("LAB/EVIDENCE/E004R/ev3_sbm_40ns.dat")
t, a, b = d[:, 0], d[:, 1], d[:, 2]
y = (a - b); y = y - y.mean()
P = np.abs(np.fft.rfft(y * np.hanning(len(y))))**2
fq = np.fft.rfftfreq(len(y), t[1]-t[0])
m = (fq > 10e9) & (fq < 26e9)
ff, PP = fq[m], P[m]
k = int(np.argmax(PP)); w = PP >= 0.5*PP[k]
F_SBM = float(np.sum(ff[w]*PP[w])/np.sum(PP[w])/1e9)

print("=" * 74)
print("MISSION-E004R — criterios PRE-REGISTRADOS (MISSION-E004R.md §4)")
print("=" * 74)
print(f"\n--- RF-2  ressonancia de breathing SBM, janela de 40 ns")
print(f"  pico = {ff[k]/1e9:.4f} GHz   centroide (>= meia altura) = f_SBM = {F_SBM:.4f} GHz")
print(f"  resolucao {1/(t[-1]-t[0])/1e9:.4f} GHz  ->  sigma(f_SBM) = {S_FSBM:.4f} GHz")
print(f"  [E001, janela de 10 ns, resolucao 0.1 GHz, dava 18.00 — era um BIN]")

print(f"\n--- RF-0  estacionariedade por frequencia (criterio: |razao-1| < 1%)")
va, vb, ok = {}, {}, {}
for f in FREQS:
    D = load(f)
    va[f], vb[f] = vperp(D, *W_EARLY), vperp(D, *W_LATE)
    dev = abs(vb[f]/va[f] - 1)
    ok[f] = dev < 0.01
    print(f"  {f:6.2f} GHz  v(150-225)={va[f]:8.5f}  v(225-300)={vb[f]:8.5f}  "
          f"|razao-1|={dev*100:6.3f} %  -> {'PASSOU' if ok[f] else 'FALHOU'}")
usa = [f for f in FREQS if ok[f]]
print(f"  frequencias estacionarias: {len(usa)} de 5   "
      f"(criterio §4: >=3 para haver parabola)")

sig_rel = float(np.mean([abs(vb[f]/va[f]-1) for f in FREQS]))
print(f"\n--- RF-0.1  escala de ruido GENUINA (media dos desvios) = {sig_rel*100:.4f} %")
print(f"  [no E004 essa mesma quantidade dava 129.5 %, porque media o TRANSIENTE]")

if len(usa) >= 3:
    fs = np.array(usa); v = np.array([vb[f] for f in usa])
    print(f"\n--- RF-1  PRIMARIO  (janela {W_LATE[0]}-{W_LATE[1]} ns)")
    for f in usa: print(f"     {f:6.2f} GHz  v_perp = {vb[f]:.5f} cm/s")
    p, kk = parab_peak(fs, v)
    print(f"  maximo na grade em {fs[kk]:.2f} GHz  ->  f_pico = "
          f"{'%.4f GHz' % p if p else 'no extremo, sem ajuste'}")
    rng = np.random.default_rng(SEED)
    sims = [parab_peak(fs, v*(1+rng.normal(0, sig_rel, len(v))))[0] for _ in range(20000)]
    sims = np.array([x for x in sims if x is not None])
    s_pk = float(sims.std())
    print(f"  sigma(f_pico) por Monte Carlo de sig_rel (semente {SEED}) = {s_pk:.4f} GHz")
    print(f"  criterio §4: veredito somente se sigma < 0.10 GHz  -> "
          f"{'HA VEREDITO' if s_pk < 0.10 else 'INDETERMINADO'}")
    if s_pk < 0.10:
        sc = np.hypot(s_pk, S_FSBM)
        d_ = abs(p - F_SBM)
        print(f"\n  f_pico = {p:.4f} +- {s_pk:.4f} GHz")
        print(f"  f_SBM  = {F_SBM:.4f} +- {S_FSBM:.4f} GHz")
        print(f"  |f_pico - f_SBM| = {d_:.4f} GHz     2*sigma_combinado = {2*sc:.4f} GHz")
        print(f"\n  ==> {'PICO COINCIDE com a ressonancia do modo (afirmacao do artigo SOBREVIVE)' if d_ <= 2*sc else 'PICO DESLOCADO — DISCREPANCIA REAL'}")
        print(f"      separacao = {d_/sc:.2f} sigma")
    print(f"\n  [predicao registrada: o E004 a 100 ns deu f_pico = 17.78 GHz]")
    if p: print(f"   deslocamento entre 100 ns e 300 ns = {abs(p-17.7642):.4f} GHz")
else:
    print("\n--- RF-1: sem parabola (menos de 3 frequencias estacionarias). Sem veredito.")
