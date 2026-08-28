#!/usr/bin/env python3
"""Rotina de figuras do laboratorio SAF — espelha os paineis do PRL 135, 086701.

Regra de desenho: TODA figura carrega, no rodape, a missao que a produziu, o que ela
mostra e o LIMITE que viaja com ela — inclusive o L-G. Uma figura viaja sem o release
dela, e e' assim que um trabalho e' recontado (CLAUDE.md §7).

Le APENAS evidencia selada. Escreve APENAS em LAB/FIGURES/.
Uso:  python3 LAB/FIGURES/make_figures.py      (da raiz do projeto)
"""
import os
import textwrap
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = "LAB/FIGURES"
E = "LAB/EVIDENCE"
LG = ("L-G: l tem um solver independente (-0.30 %), mas leitura do modelo e inicializacao "
      "sao compartilhadas; o acordo e' menor que a sensibilidade de malha (1.0 %). "
      "A dinamica segue com um unico solver. Nao e' reproducao do artigo.")

plt.rcParams.update({
    "figure.dpi": 150, "font.size": 9, "axes.linewidth": 0.9,
    "xtick.direction": "out", "ytick.direction": "out",
    "legend.frameon": False, "axes.grid": False,
})
C = {"sbm": "#5B2C9E", "abm": "#D6336C", "alt": "#F08C2E", "ref": "#888888"}


def cols(path, n=16):
    return np.array([[float(x) for x in L.split()] for L in open(path)
                     if not L.startswith("#") and len(L.split()) == n])


def footer(fig, missao, mostra, limite):
    """Rodape com quebra de linha, DENTRO da tela — sem bbox tight, para nao estourar."""
    W, H = fig.get_size_inches()
    # largura de quebra derivada da largura REAL da figura, nao chutada
    def wrapw(fs):
        return max(28, int((W - 0.25) / (fs * 0.55 / 72.0)))
    linhas = textwrap.wrap(f"{missao}  |  {mostra}", wrapw(6.2))
    n0 = len(linhas)
    linhas += textwrap.wrap(f"LIMITE: {limite}", wrapw(5.6))
    linhas += textwrap.wrap(LG, wrapw(5.6))
    n = len(linhas)
    alt = 0.16 * n / 3.0
    fig.set_size_inches(W, H * (1 + alt))
    fig.subplots_adjust(bottom=0.14 + 0.030 * n)
    for i, L in enumerate(linhas):
        prim = i < n0
        fig.text(0.5, 0.012 + 0.027 * (n - 1 - i), L, ha="center",
                 fontsize=6.2 if prim else 5.6, color="#333" if prim else "#B33")


def save(fig, nome):
    fig.savefig(f"{OUT}/{nome}.png", facecolor="white")
    plt.close(fig)
    print(f"  escrito {OUT}/{nome}.png")


def vperp_series(D, win=5.0):
    """v_perp(t) em janelas deslizantes, referencial da ligacao da janela tardia."""
    t = D[:, 0]
    s = t >= t[-1] - 50e-9
    ang = np.arctan2((D[s, 2] - D[s, 4]).mean(), (D[s, 1] - D[s, 3]).mean())
    eo = np.array([-np.sin(ang), np.cos(ang)])
    R = 0.5 * (D[:, 1] + D[:, 3]) * eo[0] + 0.5 * (D[:, 2] + D[:, 4]) * eo[1]
    out, t0, w = [], t[0], win * 1e-9
    while t0 + w <= t[-1]:
        m = (t >= t0) & (t < t0 + w)
        if m.sum() > 10:
            out.append((t0 + w / 2, abs(np.polyfit(t[m], R[m], 1)[0]) * 100))
        t0 += w
    return np.array(out)


def vperp_win(D, lo, hi):
    t = D[:, 0]
    s = (t >= lo * 1e-9) & (t <= hi * 1e-9)
    vx = np.polyfit(t[s], 0.5 * (D[s, 1] + D[s, 3]), 1)[0]
    vy = np.polyfit(t[s], 0.5 * (D[s, 2] + D[s, 4]), 1)[0]
    return np.hypot(vx, vy) * 100


# ---------------------------------------------------------------- F1 ~ Fig 2(a,b)
def F1():
    fig, ax = plt.subplots(2, 1, figsize=(5.2, 4.4), sharex=True)
    for k, (tag, nome, cor, alvo, alvof) in enumerate([
            ("E002/prop_sbm_18.00GHz", "SBM  18.00 GHz", C["sbm"], 3.50,
             "E002/fig2_a_SBM_18GHz_v_perp"),
            ("E002/prop_abm_19.24GHz", "ABM  19.24 GHz", C["abm"], 2.03,
             "E002/fig2_b_ABM_19.24GHz_v_perp")]):
        v = vperp_series(cols(f"{E}/{tag}.dat"))
        ax[k].plot(v[:, 0] * 1e9, v[:, 1], color=cor, lw=1.6, label="nosso $v_\\perp$")
        try:
            p = np.loadtxt(f"{E}/{alvof}.dat")
            ax[k].plot(p[:, 0], p[:, 1], color=C["ref"], lw=1.0, ls="--",
                       label="Fig. 2 do artigo (extraida)")
        except OSError:
            pass
        ax[k].axhline(alvo, color=C["ref"], lw=0.6, ls=":")
        ax[k].set_ylabel("$v_{pair}$ (cm/s)")
        ax[k].set_title(nome, fontsize=8, loc="left")
        ax[k].legend(fontsize=6.5)
        ax[k].set_ylim(0, None)
    ax[1].set_xlabel("t (ns)")
    fig.suptitle("F1 — deriva do par (analogo a Fig. 2(a),(b))", fontsize=9)
    fig.tight_layout(rect=[0, 0.20, 1, 0.97])
    footer(fig, "E002 (C-7, WB-011)",
           "valores tardios: SBM 3.54 vs 3.50 ; ABM 2.03 vs 2.03 cm/s",
           "o TRANSIENTE nao reproduz. ABM chegou a valor tardio; SBM ainda cruzava o alvo e "
           "nao estacionou (L7.3).")
    save(fig, "F1_deriva_do_par")


# ---------------------------------------------------------------- F2 ~ Fig 2(c,d)
def F2():
    fig, ax = plt.subplots(1, 2, figsize=(7.2, 2.9))
    for k, (tag, nome, cor, sinal) in enumerate([
            ("E002/prop_sbm_18.00GHz", "SBM: $\\ell$ vs $\\frac{1}{2}(D_1+D_2)$", C["sbm"], +1),
            ("E002/prop_abm_19.24GHz", "ABM: $\\ell$ vs $\\frac{1}{2}(D_2-D_1)$", C["abm"], -1)]):
        D = cols(f"{E}/{tag}.dat")
        t = D[:, 0]
        s = t >= t[-1] - 5e-9
        l = (D[s, 5] - D[s, 5].mean()) * 1e12
        y = (0.5 * (D[s, 8] + D[s, 9]) if sinal > 0 else 0.5 * (D[s, 9] - D[s, 8])) * 1e15
        ax[k].plot(l, y, color=cor, lw=1.2)
        ax[k].set_xlabel("$\\ell - \\bar{\\ell}$ (pm)")
        ax[k].set_ylabel("$\\mathcal{D}$ ($10^{-15}$ N s/m)")
        ax[k].set_title(nome, fontsize=8)
    fig.suptitle("F2 — ciclos de nado (analogo a Fig. 2(c),(d))", fontsize=9)
    fig.tight_layout(rect=[0, 0.26, 1, 0.95])
    footer(fig, "E002 — EXPLORATORIO, NAO e' resultado",
           "o PV-1 declarou estes dois paineis MORTOS antes do dado (piso 0.868 pm)",
           "o eixo D do artigo omite o expoente (D-1). Autores fora de alcance; A004 apenas "
           "desloca plausibilidade e aguarda aceite.")
    save(fig, "F2_ciclos_de_nado")


# ---------------------------------------------------------------- F3 ~ Fig 3(c)/S4(c)
def F3():
    fig, ax = plt.subplots(figsize=(5.4, 3.2))
    f4 = [16.5, 17.0, 17.5, 17.75, 18.0, 18.25, 18.5, 19.0, 19.5]
    v4 = []
    for f in f4:
        p = (f"{E}/E002/prop_sbm_18.00GHz.dat" if f == 18.0
             else f"{E}/E004/prop_sbm_{f:.2f}GHz.dat")
        v4.append(vperp_win(cols(p), 50, 100))
    ax.plot(f4, v4, "o-", color=C["alt"], lw=1.3, ms=4, label="E004, janela 50-100 ns")
    fR = [17.0, 17.5, 17.75, 18.0, 18.25]
    vR = [vperp_win(cols(f"{E}/E004R/prop_sbm_{f:.2f}GHz.dat"), 225, 300) for f in fR]
    ax.plot(fR, vR, "s-", color=C["sbm"], lw=1.6, ms=5, label="E004R, janela 225-300 ns")
    ax.axvline(17.9609, color=C["ref"], ls="--", lw=1.0)
    ax.text(18.03, max(v4) * 0.60, "$f_{SBM}=17.96$\n(C-11)", fontsize=6.5, color="#555")
    ax.axvline(17.8255, color="#B33", ls=":", lw=1.0)
    ax.text(16.55, max(v4) * 0.38, "pico medido 17.83\n(EXPLORATORIO)", fontsize=6.5, color="#B33")
    ax.set_xlabel("frequencia (GHz)")
    ax.set_ylabel("$v_\\perp$ (cm/s)")
    ax.set_title("F3 — ressonancia da autopropulsao (analogo a Fig. 3(c)/S4(c))",
                 fontsize=8.5)
    ax.legend(fontsize=6.5, loc="upper right")
    fig.tight_layout(rect=[0, 0.24, 1, 1])
    footer(fig, "E004 (material aceito; EF-1 sem veredito) + E004R (C-10/C-11)",
           "contraste de 86 % (fator 7) entre pico e asas; o pico converge a 6 MHz entre janelas",
           "EF-1 e RF-1 ficaram SEM VEREDITO. E005 depois explicou o deslocamento como "
           "amolecimento de amplitude; isso nao aprova retroativamente estes criterios.")
    save(fig, "F3_ressonancia_autopropulsao")


# ---------------------------------------------------------------- F4 ~ Fig 6
def F4():
    fig, ax = plt.subplots(figsize=(5.4, 3.0))
    for path, lab, cor, ls in [
            (f"{E}/E004R/ev3_sbm_40ns.dat", "SBM, janela 40 ns (E004R)", C["sbm"], "-"),
            (f"{E}/E001/ev3_sbm_10ns.dat", "SBM, janela 10 ns (E001)", C["ref"], "--")]:
        d = np.loadtxt(path)
        y = d[:, 1] - d[:, 2]
        y = y - y.mean()
        P = np.abs(np.fft.rfft(y * np.hanning(len(y))))**2
        fq = np.fft.rfftfreq(len(y), d[1, 0] - d[0, 0]) / 1e9
        m = (fq > 12) & (fq < 26)
        ax.plot(fq[m], P[m] / P[m].max(), ls, color=cor, lw=1.4, label=lab)
    ax.axvline(17.9609, color="#B33", lw=0.9, ls=":")
    ax.text(18.1, 0.85, "$f_{SBM}=17.9609$\n$\\pm0.0125$ (C-11)", fontsize=6.5, color="#B33")
    ax.set_xlabel("frequencia (GHz)")
    ax.set_ylabel("potencia (normalizada)")
    ax.set_title("F4 — espectro do modo de breathing (analogo a Fig. 6)", fontsize=8.5)
    ax.legend(fontsize=6.5)
    fig.tight_layout(rect=[0, 0.24, 1, 1])
    footer(fig, "E001 (C-6) e E004R (C-11, WB-018)",
           "a janela de 40 ns resolve 0.025 GHz; a de 10 ns so 0.1 GHz",
           "o '18.00 GHz' do E001 era um BIN. Quem cita 18.00 cita um bin, nao uma linha.")
    save(fig, "F4_espectro_breathing")


# ---------------------------------------------------------------- F5 ~ Fig 5(c)
def F5():
    import csv
    A, K, cl = [], [], []
    with open(f"{E}/R002/scan_full.csv") as fh:
        for r in csv.DictReader(fh):
            A.append(float(r["Aint"])); K.append(float(r["K0"])); cl.append(r["classe"])
    A, K = np.array(A), np.array(K)
    cl = np.array(cl)
    fig, ax = plt.subplots(figsize=(5.4, 3.2))
    est = {"NONCOAXIAL": ("o", C["sbm"], "nao-coaxial"),
           "COAXIAL": ("s", C["alt"], "coaxial")}
    for c in np.unique(cl):
        m = cl == c
        mk, cor, lab = est.get(c, ("x", "#CCC", c.lower()))
        ax.plot(A[m], K[m], mk, color=cor, ms=4, mew=0.8,
                mfc=cor if c in est else "none", label=lab, ls="none")
    x = np.linspace(A.min(), A.max(), 50)
    ax.plot(x, 0.65 - 2.5 * x, "--", color="#B33", lw=1.2, label="Eq. (S1) do artigo")
    ax.set_xlabel("$A_{int}$ (mJ/m$^2$)")
    ax.set_ylabel("$K_0$ (MJ/m$^3$)")
    ax.set_title("F5 — regiao de estabilidade (analogo a Fig. 5(c))", fontsize=8.5)
    ax.set_ylim(0.05, 0.95)
    ax.legend(fontsize=6.2, ncol=4, loc="upper center", bbox_to_anchor=(0.5, 1.14))
    fig.tight_layout(rect=[0, 0.24, 1, 0.93])
    footer(fig, "R002 (C-2, WB-007) + ADDENDUM-001",
           "165 pontos; os dois pontos publicados caem na regiao estavel",
           "L2.3 ABERTA: em A_int=0.12 o artigo preve ramo coaxial e nos nao o encontramos; "
           "A006 esta autorizada, ainda sem pre-registro lido.")
    save(fig, "F5_regiao_estabilidade")


# ---------------------------------------------------------------- F6 (nosso, sem analogo)
def F6():
    fig, ax = plt.subplots(figsize=(5.2, 3.0))
    pts = []
    for tag in ["eo1_sbm_th30", "eo1_sbm_th22.5"]:
        D = cols(f"{E}/E003/prop_{tag}.dat")
        t = D[:, 0]
        s = (t >= 50e-9) & (t <= 100e-9)
        tb = np.degrees(np.arctan2((D[s, 2] - D[s, 4]).mean(), (D[s, 1] - D[s, 3]).mean()))
        vx = np.polyfit(t[s], 0.5 * (D[s, 1] + D[s, 3]), 1)[0]
        vy = np.polyfit(t[s], 0.5 * (D[s, 2] + D[s, 4]), 1)[0]
        pts.append((abs((tb + 180 + 180) % 360 - 180), np.degrees(np.arctan2(vy, vx))))
    pts.append((0.0, 90.0))          # ancora do E002: ligacao em x, deriva em y
    pts = np.array(sorted(pts))
    ax.plot(pts[:, 0], pts[:, 1], "o", color=C["sbm"], ms=6, label="medido")
    x = np.linspace(-2, 30, 10)
    ax.plot(x, x + 90, "-", color="#B33", lw=1.2, label="$H_{ligacao}$: inclinacao +1")
    ax.plot(x, 0 * x + 90, "--", color=C["ref"], lw=1.2, label="$H_{rede}$: inclinacao 0")
    ax.set_xlabel("$\\theta_{ligacao}$ (graus)")
    ax.set_ylabel("$\\varphi_{deriva}$ (graus)")
    ax.set_title("F6 — a deriva segue a ligacao, nao a rede", fontsize=8.5)
    ax.legend(fontsize=6.5)
    fig.tight_layout(rect=[0, 0.24, 1, 1])
    footer(fig, "E003 (C-8, WB-015)",
           "inclinacao medida = +1.0201, estavel em tres janelas (1.007-1.026)",
           "testado em DOIS angulos alem de zero, so no modo SBM; os estados fora do eixo "
           "nao estavam plenamente relaxados. Nao e' 'qualquer angulo'.")
    save(fig, "F6_deriva_segue_ligacao")


# ---------------------------------------------------------------- F7 (E005) ~ Fig S4(c)
def F7():
    """O resultado do E005: f_pico contra amplitude, nosso e o do artigo."""
    ALVO = {0.002: 17.9176, 0.004: 17.7487, 0.008: 17.4649}      # RA-3, selado antes
    NOSSO = {0.002: (17.9664, 0.0061), 0.005: (17.8255, 0.0108), 0.008: (17.5796, 0.0336)}
    fig, ax = plt.subplots(1, 2, figsize=(7.4, 3.1))

    # (a) as curvas medidas
    for amp, cor in [(0.002, C["alt"]), (0.005, C["abm"]), (0.008, C["sbm"])]:
        if amp == 0.005:
            fs = [17.00, 17.50, 17.75, 18.00, 18.25]
            pat = f"{E}/E004R/prop_sbm_%.2fGHz.dat"
        else:
            fs = [17.00, 17.25, 17.50, 17.75, 18.00, 18.25, 18.50]
            pat = f"{E}/E005/prop_sbm_A{amp:.3f}_%.2fGHz.dat"
        v = [vperp_win(cols(pat % f), 225, 300) for f in fs]
        ax[0].semilogy(fs, v, "o-", color=cor, ms=4, lw=1.3,
                       label=f"$\\Delta K/K_0$ = {amp}")
        ax[0].axvline(NOSSO[amp][0], color=cor, ls=":", lw=0.8)
    ax[0].axvline(17.9609, color="#333", ls="--", lw=1.0)
    ax[0].text(17.99, ax[0].get_ylim()[0] * 2.2, "$f_{SBM}$\n17.96", fontsize=6.3, color="#333")
    ax[0].set_xlabel("frequencia (GHz)")
    ax[0].set_ylabel("$v_\\perp$ (cm/s)")
    ax[0].set_title("(a) nossas curvas, janela 225-300 ns", fontsize=8, loc="left")
    ax[0].legend(fontsize=6.3)

    # (b) f_pico vs amplitude — nosso contra o artigo
    ka = sorted(ALVO); kn = sorted(NOSSO)
    ax[1].plot(ka, [ALVO[k] for k in ka], "s--", color=C["ref"], ms=5, lw=1.2,
               label="artigo (Fig. S4(c), extraida)")
    ax[1].errorbar(kn, [NOSSO[k][0] for k in kn], yerr=[NOSSO[k][1] for k in kn],
                   fmt="o-", color=C["sbm"], ms=5, lw=1.5, capsize=3, label="nosso")
    ax[1].axhline(17.9609, color="#B33", ls=":", lw=1.0)
    ax[1].text(0.0055, 17.972, "$f_{SBM}=17.96$ (C-11)", fontsize=6.3, color="#B33")
    ax[1].set_xlabel("$\\Delta K/K_0$")
    ax[1].set_ylabel("$f_{pico}$ (GHz)")
    ax[1].set_title("(b) amolecimento: inclinacao -64.5 vs -74.8", fontsize=8, loc="left")
    ax[1].legend(fontsize=6.3)

    fig.suptitle("F7 — amolecimento do pico com a amplitude (analogo a Fig. S4(c))",
                 fontsize=9)
    fig.tight_layout(rect=[0, 0.24, 1, 0.94])
    footer(fig, "E005 (RA-1 PASSOU, gate passou)",
           "inclinacao medida/artigo = 0.862; o pico DESCE quando a amplitude sobe",
           "os nossos picos ficam +0.05 a +0.12 GHz ACIMA dos do artigo: o nosso amolecimento "
           "e' ~14 % mais fraco, e isso NAO esta explicado. RA-2 (coincidencia com f_SBM a "
           "0.40 sigma) e' EXPLORATORIO, nao criterio.")
    save(fig, "F7_amolecimento_amplitude")


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    print("Gerando figuras a partir de evidencia SELADA:")
    for fn in (F1, F2, F3, F4, F5, F6, F7):
        try:
            fn()
        except Exception as ex:
            print(f"  [FALHOU] {fn.__name__}: {type(ex).__name__}: {ex}")
