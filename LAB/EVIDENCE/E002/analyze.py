#!/usr/bin/env python3
"""MISSION-E002 — analise contra os criterios PRE-REGISTRADOS de MISSION-E002.md.

Nao ha escolha de janela nem de banda aqui: tudo vem do pre-registro.
Uso: python3 LAB/EVIDENCE/E002/analyze.py
"""
import numpy as np

GAMMA = 1.760859e11
Ms, d, ALPHA = 0.58e6, 0.4e-9, 0.02
FITWIN = 50.0          # ns finais usados no ajuste (>= 50 ciclos, pre-registro §4)

COLS = dict(t=0, X1=1, Y1=2, X2=3, Y2=4, l=5, Q1=6, Q2=7, Dd1=8, Dd2=9)

def load(tag):
    """Tolerante a arquivo AINDA EM ESCRITA: descarta a ultima linha incompleta."""
    rows = []
    with open(f"LAB/EVIDENCE/E002/prop_{tag}.dat") as fh:
        for line in fh:
            if line.startswith("#"):
                continue
            v = line.split()
            if len(v) == 16:
                rows.append([float(x) for x in v])
    if not rows:
        raise OSError("sem linhas completas")
    return np.array(rows)

def kinematics(D, fitwin=FITWIN):
    """v_par e v_perp no referencial da ligacao, ajuste linear na janela tardia.
    Devolve tambem o angulo da ligacao no INICIO e no FIM da janela: se a ligacao
    reorienta, um angulo medio unico borra as duas componentes e o estimador de
    referencial fixo e' o errado."""
    t = D[:, 0]
    sel = t >= t[-1] - fitwin * 1e-9
    bx, by = D[sel, 1] - D[sel, 3], D[sel, 2] - D[sel, 4]
    ang = np.arctan2(by.mean(), bx.mean())
    a0 = np.degrees(np.arctan2(by[:50].mean(), bx[:50].mean()))
    a1 = np.degrees(np.arctan2(by[-50:].mean(), bx[-50:].mean()))
    giro = (a1 - a0 + 180.0) % 360.0 - 180.0      # desdobra: -180 e +180 sao o MESMO angulo
    ep = np.array([np.cos(ang), np.sin(ang)])
    eo = np.array([-np.sin(ang), np.cos(ang)])
    Rx = 0.5 * (D[sel, 1] + D[sel, 3])
    Ry = 0.5 * (D[sel, 2] + D[sel, 4])
    tp = t[sel]
    vpar = np.polyfit(tp, Rx * ep[0] + Ry * ep[1], 1)[0]
    vperp = np.polyfit(tp, Rx * eo[0] + Ry * eo[1], 1)[0]
    # rota independente: projecao na ligacao INSTANTANEA, amostra a amostra
    bn = np.hypot(bx, by)
    px, py = bx / bn, by / bn
    dRx, dRy = np.diff(Rx), np.diff(Ry)
    dpar = (dRx * px[:-1] + dRy * py[:-1]).sum()
    dperp = (-dRx * py[:-1] + dRy * px[:-1]).sum()
    dur = tp[-1] - tp[0]
    lbar = D[sel, 5].mean()
    return vpar, vperp, np.degrees(ang), a0, giro, dpar / dur, dperp / dur, lbar


def vperp_of_t(D, win_ns=5.0):
    """v_perp(t) em janelas deslizantes — para comparar a FORMA do transiente
    com a Fig. 2(a)/(b). Direcao fixada pela ligacao media da janela tardia."""
    t = D[:, 0]
    sel = t >= t[-1] - FITWIN * 1e-9
    ang = np.arctan2((D[sel, 2] - D[sel, 4]).mean(), (D[sel, 1] - D[sel, 3]).mean())
    eo = np.array([-np.sin(ang), np.cos(ang)])
    R = 0.5 * (D[:, 1] + D[:, 3]) * eo[0] + 0.5 * (D[:, 2] + D[:, 4]) * eo[1]
    out = []
    w = win_ns * 1e-9
    t0 = t[0]
    while t0 + w <= t[-1]:
        s = (t >= t0) & (t < t0 + w)
        if s.sum() > 10:
            out.append((0.5 * (2 * t0 + w) * 1e9, np.polyfit(t[s], R[s], 1)[0] * 100))
        t0 += w
    return np.array(out)

def spectrum_l(D, fdrive, fitwin=FITWIN):
    """EP-4: espectro de potencia de l(t) no estacionario, sem tendencia lenta."""
    t = D[:, 0]
    sel = t >= t[-1] - fitwin * 1e-9
    tt, ll = t[sel], D[sel, 5]
    ll = ll - np.polyval(np.polyfit(tt, ll, 1), tt)      # remove baseline linear
    dt = np.diff(tt).mean()
    f = np.fft.rfftfreq(len(ll), dt)
    P = np.abs(np.fft.rfft(ll * np.hanning(len(ll)))) ** 2
    k = np.argmax(P[1:]) + 1
    return f[k], f, P, ll.max() - ll.min()

def eq4(D, fdrive, fitwin=FITWIN, ncyc_frac=1.0):
    """EP-5: v_sp = -(w/4pi) \\oint (G/(alpha*Dd)) dl, por ciclo.
    G = 4pi(Ms d/gamma)|Q| e Dd = (Ms d/gamma)*I  =>  o prefator CANCELA:
    v_sp = -(w/alpha) \\oint (|Q|/I) dl .  Insensivel a leitura R1/R2 do PV-0.
    Usa um numero INTEIRO de ciclos; |Q| descarta o sinal, logo isto compara
    MAGNITUDE apenas."""
    t = D[:, 0]
    sel = t >= t[-1] - fitwin * 1e-9
    tt = t[sel]
    per = 1.0 / fdrive
    ncyc = int(np.floor((tt[-1] - tt[0]) / per) * ncyc_frac)
    if ncyc < 1:
        return np.nan
    keep = tt <= tt[0] + ncyc * per                 # janela de ciclos INTEIROS
    idx = np.where(sel)[0][keep]
    ll = D[idx, 5]
    pre = Ms * d / GAMMA
    I = 0.5 * (D[idx, 8] + D[idx, 9]) / pre
    Q = 0.5 * (np.abs(D[idx, 6]) + np.abs(D[idx, 7]))
    integ = np.trapz(Q / I, ll)                     # integral de contorno
    return -(2 * np.pi * fdrive / ALPHA) * integ / ncyc


# ------------------------------- alvos (§2) ----------------------------------
RUNS = [
    ("sbm_18.00GHz",  "SBM  18.00 GHz", 18.00e9, 3.50, (2.45, 4.55), 1),
    ("abm_19.24GHz",  "ABM  19.24 GHz", 19.24e9, 2.03, (1.02, 3.05), 2),
    ("abm_19.40GHz",  "ABM  19.40 GHz", 19.40e9, None, None,         2),
]

print("=" * 78)
print("MISSION-E002 — criterios PRE-REGISTRADOS (MISSION-E002.md §5, §6)")
print("=" * 78)

# ---- PV-1 -------------------------------------------------------------------
try:
    N = load("pv1_noise200ns")
    t = N[:, 0] * 1e9
    lp = N[:, 5] * 1e12
    pp_raw = lp.max() - lp.min()
    sel = t >= t[-1] - FITWIN
    lt = lp[sel] - np.polyval(np.polyfit(t[sel], lp[sel], 1), t[sel])
    pp_det = lt.max() - lt.min()
    vpar, vperp, _, _, _, _, _, _ = kinematics(N)
    print("\n--- PV-1  piso de ruido (excitacao DESLIGADA, 200 ns)")
    print(f"  pp(l) na corrida inteira (o numero PRE-REGISTRADO) = {pp_raw:.4f} pm")
    print(f"    Fig.2(c) SBM exige < 0.40 pm  -> {'PASSOU' if pp_raw<0.40 else 'FALHOU'}")
    print(f"    Fig.2(d) ABM exige < 0.02 pm  -> {'PASSOU' if pp_raw<0.02 else 'FALHOU'}")
    print(f"  [exploratorio, NAO repara criterio] pp(l) sem tendencia, "
          f"ultimos {FITWIN:.0f} ns = {pp_det:.4f} pm")
    print(f"  deriva espuria na janela de ajuste: v_perp = {vperp*100:+.6f} cm/s  "
          f"v_par = {vpar*100:+.6f} cm/s")
except OSError:
    print("\n--- PV-1  (ainda nao rodou)")

# ---- EP-1, EP-2, EP-3, EP-4, EP-5 ------------------------------------------
res = {}
for tag, name, fd, alvo, banda, harm in RUNS:
    try:
        D = load(tag)
    except OSError:
        print(f"\n--- {name}: (ainda nao rodou)")
        continue
    vpar, vperp, ang, a0, giro, ipar, iperp, lbar = kinematics(D)
    vpar, vperp = vpar * 100, vperp * 100                 # m/s -> cm/s
    ipar, iperp = ipar * 100, iperp * 100
    ratio = abs(vpar) / abs(vperp)
    theta = np.degrees(np.arctan2(vperp, vpar))
    fpk, f, P, lpp = spectrum_l(D, fd)
    v4 = eq4(D, fd) * 100
    v4h = eq4(D, fd, ncyc_frac=0.5) * 100
    res[tag] = dict(vperp=vperp, vpar=vpar, fpk=fpk, v4=v4, lpp=lpp * 1e12)
    print(f"\n--- {name}   (ligacao a {ang:+.2f} deg)")
    print(f"  EP-1  |v_par|/|v_perp| = {ratio:.4f}   criterio < 0.05   "
          f"-> {'PASSOU' if ratio<0.05 else 'FALHOU'}")
    print(f"        v_perp = {vperp:+.4f} cm/s      v_par = {vpar:+.6f} cm/s")
    print(f"        angulo da deriva vs ligacao = {theta:+.3f} deg  (esperado +-90)")
    print(f"        ligacao no inicio da janela {a0:+.3f} deg, giro na janela {giro:+.4f} deg")
    print(f"        rota independente (projecao instantanea): "
          f"v_perp = {iperp:+.4f}  v_par = {ipar:+.6f} cm/s")
    if banda:
        ok = banda[0] <= abs(vperp) <= banda[1]
        print(f"  EP-2  |v_perp| = {abs(vperp):.4f} cm/s   alvo {alvo} cm/s   "
              f"banda [{banda[0]}, {banda[1]}]  -> {'PASSOU' if ok else 'FALHOU'}")
        print(f"        desvio do alvo = {100*(abs(vperp)-alvo)/alvo:+.1f} %")
    print(f"  EP-4  pico de l(t) em {fpk/1e9:.4f} GHz;  f_drive = {fd/1e9:.4f}, "
          f"2*f_drive = {2*fd/1e9:.4f}")
    print(f"        esperado: {'f_drive (SBM)' if harm==1 else '2*f_drive (ABM)'}   "
          f"-> {'PASSOU' if abs(fpk-harm*fd)<0.06*fd else 'FALHOU'}")
    print(f"        amplitude pp de l no estacionario = {lpp*1e12:.4f} pm")
    print(f"  [exploratorio, NAO pre-registrado] l_barra no estacionario = {lbar*1e9:.4f} nm")
    print(f"  EP-5  |v_sp| pela Eq.(4) = {abs(v4):.4f} cm/s   vs |CTC| {abs(vperp):.4f} cm/s"
          f"   razao = {abs(v4)/abs(vperp):.4f}   (EXPLORATORIO, so magnitude:")
    print(f"        |Q| descarta o sinal.)  estabilidade: com metade dos ciclos = "
          f"{abs(v4h):.4f} cm/s  (desvio {100*abs(abs(v4h)-abs(v4))/abs(v4):.2f} %)")

if "abm_19.24GHz" in res and "abm_19.40GHz" in res:
    a, b = abs(res["abm_19.24GHz"]["vperp"]), abs(res["abm_19.40GHz"]["vperp"])
    print(f"\n--- EP-3  dessintonia:  v(19.40) = {b:.4f}  vs  v(19.24) = {a:.4f} cm/s")
    print(f"        predicao registrada v(19.40) > v(19.24)  -> "
          f"{'PASSOU' if b>a else 'FALHOU'}   razao = {b/a:.4f}")

# ---- PV-2  controle de passo de tempo ---------------------------------------
# Compara v_perp na MESMA janela (a corrida de 5 fs so tem 20 ns) entre dt=10 fs
# e dt=5 fs. Pre-registro §5: passa se difere < 2 % e max||m|-1| < 1e-9.
try:
    A = load("sbm_18.00GHz")
    B = load("pv2_sbm_dt5fs")
    tmax = B[-1, 0]
    lo = 0.5 * tmax                       # segunda metade da janela curta
    out = []
    for D in (A, B):
        s = (D[:, 0] >= lo) & (D[:, 0] <= tmax)
        Y = 0.5 * (D[s, 2] + D[s, 4])
        out.append(np.polyfit(D[s, 0], Y, 1)[0] * 100)
    dif = 100 * abs(out[1] - out[0]) / abs(out[0])
    print(f"\n--- PV-2  controle de passo (janela {lo*1e9:.1f}-{tmax*1e9:.1f} ns)")
    print(f"  dt = 10 fs: v_perp = {out[0]:+.5f} cm/s")
    print(f"  dt =  5 fs: v_perp = {out[1]:+.5f} cm/s")
    print(f"  diferenca = {dif:.3f} %   criterio < 2 %   -> "
          f"{'PASSOU' if dif < 2.0 else 'FALHOU'}")
except OSError:
    print("\n--- PV-2  (ainda nao rodou)")
