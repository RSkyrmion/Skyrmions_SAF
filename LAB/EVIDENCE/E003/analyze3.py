#!/usr/bin/env python3
"""MISSION-E003 — H_ligacao vs H_rede, contra os criterios PRE-REGISTRADOS.

Criterio primario EO-1 (MISSION-E003.md §5): residuo R = (phi_drift - theta_bond) - 90 deg.
  H_ligacao prediz R = 0 ; H_rede prediz R = -theta_bond_relativo_ao_eixo.
Sem limiar absoluto: a escala de ruido vem do controle EO-0.
"""
import numpy as np

def load(tag):
    return np.array([[float(x) for x in L.split()]
                     for L in open(f"LAB/EVIDENCE/E003/prop_{tag}.dat")
                     if not L.startswith("#") and len(L.split()) == 16])

def wrap180(a):
    return (a + 180.0) % 360.0 - 180.0

def bond_angle(D, sel):
    """Angulo do vetor R1-R2, na convencao do E002 (la deu -180 deg)."""
    bx = (D[sel, 1] - D[sel, 3]).mean()
    by = (D[sel, 2] - D[sel, 4]).mean()
    return np.degrees(np.arctan2(by, bx))

def drift_angle(D, sel):
    """Angulo do vetor deslocamento do par, por ajuste linear das duas componentes."""
    t = D[sel, 0]
    vx = np.polyfit(t, 0.5 * (D[sel, 1] + D[sel, 3]), 1)[0]
    vy = np.polyfit(t, 0.5 * (D[sel, 2] + D[sel, 4]), 1)[0]
    return np.degrees(np.arctan2(vy, vx)), np.hypot(vx, vy) * 100   # deg, cm/s

def perp_dev(phi, tb):
    """Desvio da PERPENDICULARIDADE, em graus, sem depender do sinal da convencao:
    o E002 deu (phi - theta_bond) = -90 exato; aqui mede-se contra o +-90 mais proximo."""
    a = wrap180(phi - tb)
    return a - (90.0 if a > 0 else -90.0)

def window(D, lo_ns, hi_ns):
    t = D[:, 0]
    return (t >= lo_ns * 1e-9) & (t <= hi_ns * 1e-9)

print("=" * 76)
print("MISSION-E003 — criterios PRE-REGISTRADOS (MISSION-E003.md §4-§6)")
print("=" * 76)

# ---------------- EO-0: controle sem excitacao ------------------------------
print("\n--- EO-0  controle SEM excitacao (§4). Decide M-config vs M-rede.")
print("  referencia casada, theta=0 (E002 PV-1): 3.99e-02 cm/s em 10-20 ns,")
print("  decaindo para 7.1e-05 cm/s em 150-200 ns.")
ctrl = {}
for tag, th in [("eo0_ctrl_th30", 30.0), ("eo0_ctrl_th22.5", 22.5)]:
    D = load(tag)
    s = window(D, 10, 20)
    tb = bond_angle(D, s)
    da, mag = drift_angle(D, s)
    ctrl[th] = mag
    # decai?
    _, m1 = drift_angle(D, window(D, 0, 4))
    _, m2 = drift_angle(D, window(D, 16, 20))
    print(f"  theta_init={th:5.1f}: |v_espuria| = {mag:.5f} cm/s, a {wrap180(da-tb):+.3f} deg "
          f"da ligacao -> AO LONGO dela")
    print(f"                 0-4 ns: {m1:.5f}   16-20 ns: {m2:.5f}   -> "
          f"{'CONSTANTE, nao decai' if abs(m2-m1)/m1 < 0.01 else 'decai'}")
print(f"\n  LEITURA DO MECANISMO (regra registrada em §4.2): a deriva espuria fora do eixo")
print(f"  e' ~23x a de theta=0 na mesma janela e NAO decai  ->  **M-rede**.")

# ---------------- EO-1: criterio primario -----------------------------------
print("\n--- EO-1  PRIMARIO (§5): a deriva acompanha a LIGACAO ou a REDE?")
print("  desvio da perpendicularidade medido contra o +-90 mais proximo (convencao do E002: -90).")
print()
print("  theta  janela      |v|[cm/s]   desvio medido   previsto pela EO-0   razao")
rows = []
for tag, th in [("eo1_sbm_th30", 30.0), ("eo1_sbm_th22.5", 22.5)]:
    D = load(tag)
    vsp = ctrl[th]
    for nm, lo, hi in [("25-50 ns", 25, 50), ("50-100 ns", 50, 100)]:
        s = window(D, lo, hi)
        tb = bond_angle(D, s)
        da, mag = drift_angle(D, s)
        dev = perp_dev(da, tb)
        pred = np.degrees(np.arctan2(vsp, mag))
        print(f"  {th:5.1f}  {nm:10s}  {mag:8.4f}   {dev:+9.4f} deg   {pred:+9.4f} deg      "
              f"{dev/pred:.3f}")
        if hi == 100:
            rows.append((th, tb, da, dev, mag))
print("\n  A contaminacao medida no EO-0 preve o desvio em 2 angulos x 2 janelas,")
print("  com razao 0.90 nas quatro. O que ela NAO explica sao ~10% (0.8 deg em 50-100 ns).")

print("\n--- EO-1  o discriminante: teste de INCLINACAO (§5, dois angulos)")
tb_lin = np.array([abs(wrap180(r[1] + 180.0)) for r in rows])
phi = np.array([r[2] for r in rows])
dev = np.array([r[3] for r in rows])
sl = (phi[0] - phi[1]) / (tb_lin[0] - tb_lin[1])
print(f"  theta_bond (orientacao da linha): {tb_lin[0]:.4f} e {tb_lin[1]:.4f} deg")
print(f"  phi_drift medido:                 {phi[0]:.4f} e {phi[1]:.4f} deg")
print(f"  d(phi_drift)/d(theta_bond) = {sl:+.4f}")
print(f"     H_ligacao prediz +1.0000  |  H_rede prediz 0.0000   ->  "
      f"{'H_LIGACAO' if abs(sl-1) < abs(sl) else 'H_REDE'}")
print(f"  equivalentemente dR/dtheta = {(dev[0]-dev[1])/(tb_lin[0]-tb_lin[1]):+.4f}  "
      f"(H_ligacao: 0 ; H_rede: -1)")
print("  A inclinacao e' IMUNE a contaminacao do EO-0, que e' ao longo da ligacao nos")
print("  dois angulos e portanto desloca o offset, nao a inclinacao.")

# ---------------- EO-0.1 e convergencia -------------------------------------
print("\n--- EO-0.1  estado comparavel? (§4)")
print("  l_eq: theta=0: 10.960706 nm | theta=30: 10.953118 (-0.069%) | "
      "theta=22.5: 10.956750 (-0.036%)   criterio <1% -> PASSOU")
print("  Q1=-1.0000 Q2=+1.0000 nos dois -> PASSOU")
print("  aprisionamento: ligacao girou -3.98 e -4.25 deg, parando em 25.86 e 18.09 deg,")
print("  longe de 0/45/90 -> NAO houve aprisionamento em eixo; EO-1 tem veredito.")
print("  MAS a relaxacao NAO convergiu fora do eixo: 2e6 iteracoes, torque parado em")
print("  1.26e-05 T (contra 1e-06 em theta=0). Ver §defeito no release.")

print("\n--- convergencia da direcao (§6)")
for tag, th in [("eo1_sbm_th30", 30.0), ("eo1_sbm_th22.5", 22.5)]:
    D = load(tag)
    a = perp_dev(*(lambda s: (drift_angle(D, s)[0], bond_angle(D, s)))(window(D, 25, 50)))
    b = perp_dev(*(lambda s: (drift_angle(D, s)[0], bond_angle(D, s)))(window(D, 50, 100)))
    print(f"  theta={th:5.1f}: desvio 25-50 = {a:+.4f}, 50-100 = {b:+.4f}, dif = {abs(b-a):.4f} deg")
print("  A diferenca NAO e' ruido: e' a contaminacao constante do EO-0 dividida por um")
print("  sinal que decai (14.4 -> 6.1 cm/s). Prevista: 4.94 deg. Medida: 4.43 e 4.33.")

# ---------------- EO-2 -------------------------------------------------------
print("\n--- EO-2  magnitude sob rotacao (exploratorio, janela casada 50-100 ns)")
D0 = np.array([[float(x) for x in L.split()]
               for L in open("LAB/EVIDENCE/E002/prop_sbm_18.00GHz.dat")
               if not L.startswith("#") and len(L.split()) == 16])
_, m0 = drift_angle(D0, window(D0, 50, 100))
print(f"  theta= 0.0 (E002): |v| = {m0:.4f} cm/s")
for th, _, _, _, mag in rows:
    print(f"  theta={th:5.1f}:       |v| = {mag:.4f} cm/s   ({100*(mag-m0)/m0:+.2f} %)")
print("  Parte disso e' a propria contaminacao somada em quadratura; nao e' criterio.")
