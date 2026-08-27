#!/usr/bin/env python3
"""MISSION-E005 — RA-0, RA-1, RA-2 exatamente como pre-registrados (MISSION-E005.md §4).

Definicoes fixadas no pre-registro. Semente do Monte Carlo: 20260827.
"""
import numpy as np

W_EARLY, W_LATE = (150, 225), (225, 300)
SEED = 20260827
F_SBM, S_FSBM = 17.9609, 0.0125          # C-11
ALVO = {0.002: 17.9176, 0.004: 17.7487, 0.008: 17.4649}   # RA-3, selado antes das corridas
SL_ART = np.polyfit(sorted(ALVO), [ALVO[k] for k in sorted(ALVO)], 1)[0]

FREQS_E005 = [17.00, 17.25, 17.50, 17.75, 18.00, 18.25, 18.50]
FREQS_E004R = [17.00, 17.50, 17.75, 18.00, 18.25]


def cols(path):
    return np.array([[float(x) for x in L.split()] for L in open(path)
                     if not L.startswith("#") and len(L.split()) == 16])


def vperp(D, lo, hi):
    t = D[:, 0]
    s = (t >= lo * 1e-9) & (t <= hi * 1e-9)
    vx = np.polyfit(t[s], 0.5 * (D[s, 1] + D[s, 3]), 1)[0]
    vy = np.polyfit(t[s], 0.5 * (D[s, 2] + D[s, 4]), 1)[0]
    return np.hypot(vx, vy) * 100


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


def serie(amp):
    """(freqs, v_early, v_late) para uma amplitude; E005 ou, para 0.005, o E004R."""
    if amp == 0.005:
        fs, path = FREQS_E004R, "LAB/EVIDENCE/E004R/prop_sbm_%.2fGHz.dat"
    else:
        fs, path = FREQS_E005, f"LAB/EVIDENCE/E005/prop_sbm_A{amp:.3f}_%.2fGHz.dat"
    F, A, B = [], [], []
    for f in fs:
        try:
            D = cols(path % f)
        except OSError:
            continue
        if len(D) == 0 or D[-1, 0] < W_LATE[1] * 1e-9 * 0.999:
            continue                      # corrida ainda em escrita: descarta
        F.append(f); A.append(vperp(D, *W_EARLY)); B.append(vperp(D, *W_LATE))
    return np.array(F), np.array(A), np.array(B)


print("=" * 76)
print("MISSION-E005 — criterios PRE-REGISTRADOS")
print("=" * 76)
print(f"\nALVO (RA-3, selado antes das corridas): " +
      "  ".join(f"{k}->{v:.4f}" for k, v in sorted(ALVO.items())))
print(f"  inclinacao do artigo = {SL_ART:+.3f} GHz por unidade de dK/K0")
print(f"  banda do RA-1 (fator 3): [{SL_ART*3:+.1f}, {SL_ART/3:+.1f}]")

print(f"\n--- RA-0  convergencia de f_pico (a SAIDA), por amplitude")
pk, sg, ok = {}, {}, {}
for amp in (0.002, 0.005, 0.008):
    F, A, B = serie(amp)
    if len(F) < 3:
        print(f"  dK/K0={amp:.3f}: apenas {len(F)} corridas — incompleta")
        continue
    pa, _ = parab(F, A)
    pb, kb = parab(F, B)
    if pa is None or pb is None:
        print(f"  dK/K0={amp:.3f}: maximo no extremo da grade, sem parabola")
        continue
    d = abs(pa - pb)
    ok[amp] = d <= 0.125
    pk[amp] = pb
    print(f"  dK/K0={amp:.3f}  ({len(F)} pts)  f_pico(150-225)={pa:.4f}  "
          f"f_pico(225-300)={pb:.4f}  dif={d:.4f} GHz  -> "
          f"{'PASSOU' if ok[amp] else 'FALHOU'}")
    rng = np.random.default_rng(SEED)
    rel = np.abs(B / A - 1)
    sims = [parab(F, B * (1 + rng.normal(0, rel)))[0] for _ in range(20000)]
    sims = np.array([x for x in sims if x is not None])
    sg[amp] = float(sims.std())
    print(f"                  dispersao entre janelas = {rel.mean()*100:.3f} %   "
          f"sigma(f_pico) = {sg[amp]:.4f} GHz  "
          f"({'ok' if sg[amp] < 0.10 else 'ACIMA de 0.10'})")

usa = [a for a in pk if ok.get(a) and sg.get(a, 9) < 0.10]
print(f"\n  amplitudes utilizaveis: {sorted(usa)}   (§4 exige >= 2)")

if len(usa) >= 2:
    xs = np.array(sorted(usa)); ys = np.array([pk[a] for a in xs])
    sl = np.polyfit(xs, ys, 1)[0]
    print(f"\n--- RA-1  PRIMARIO: df_pico/d(dK/K0)")
    for a in xs:
        print(f"     dK/K0={a:.3f}  f_pico = {pk[a]:.4f} +- {sg[a]:.4f} GHz    "
              f"(artigo: {ALVO.get(a, float('nan')):.4f})" if a in ALVO else
              f"     dK/K0={a:.3f}  f_pico = {pk[a]:.4f} +- {sg[a]:.4f} GHz    (artigo: interpolado)")
    print(f"  inclinacao medida = {sl:+.3f} GHz/unidade   artigo = {SL_ART:+.3f}")
    print(f"  razao medida/artigo = {sl/SL_ART:.3f}")
    neg = sl < 0
    dentro = (1/3) <= (sl / SL_ART) <= 3.0
    print(f"  H_amplitude exige: negativa E dentro do fator 3  -> "
          f"{'PASSOU' if (neg and dentro) else 'FALHOU'}")
    print(f"  H_fixo previa inclinacao ~0")
    print(f"\n--- RA-2  (exploratorio) pico de menor amplitude vs f_SBM")
    a0 = min(usa)
    print(f"  f_pico({a0:.3f}) = {pk[a0]:.4f} +- {sg[a0]:.4f}   f_SBM = {F_SBM} +- {S_FSBM}")
    sc = np.hypot(sg[a0], S_FSBM)
    print(f"  diferenca = {abs(pk[a0]-F_SBM):.4f} GHz = {abs(pk[a0]-F_SBM)/sc:.2f} sigma")
else:
    print("\n--- RA-1: menos de 2 amplitudes utilizaveis. SEM VEREDITO.")
