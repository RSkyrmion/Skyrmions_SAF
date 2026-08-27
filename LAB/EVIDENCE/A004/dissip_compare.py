#!/usr/bin/env python3
"""MISSION-A004 — AD-0 e AD-1: 𝒟 do estado do mumax3 contra o do saf.cu.

Grandeza: I = sqrt(det \\int d_u m . d_v m d2r), ADIMENSIONAL — imune ao prefator
Ms*d/gamma, que e' justamente a ambiguidade do D-1. Le APENAS evidencia selada.
"""
import numpy as np

GAMMA, Ms, d, a = 1.760859e11, 0.58e6, 0.4e-9, 1e-9
PRE = Ms * d / GAMMA


def tensor(u, a=a):
    """I_uv = \\int d_u m . d_v m d2r, diferencas CENTRADAS (o mesmo estencil do E002)."""
    dX = (np.roll(u, -1, 1) - np.roll(u, 1, 1)) / (2 * a)     # eixo 1 = i = x
    dY = (np.roll(u, -1, 0) - np.roll(u, 1, 0)) / (2 * a)     # eixo 0 = j = y
    Ixx = (dX * dX).sum() * a * a
    Iyy = (dY * dY).sum() * a * a
    Ixy = (dX * dY).sum() * a * a
    return Ixx, Iyy, Ixy, np.sqrt(Ixx * Iyy - Ixy * Ixy)


def bond(m1, m2, a=a):
    """l pela CTC de Berg-Luscher, so para o AD-0 (estado comparavel?)."""
    def tri(A, B, C):
        num = A[..., 0]*(B[..., 1]*C[..., 2]-B[..., 2]*C[..., 1]) + \
              A[..., 1]*(B[..., 2]*C[..., 0]-B[..., 0]*C[..., 2]) + \
              A[..., 2]*(B[..., 0]*C[..., 1]-B[..., 1]*C[..., 0])
        den = 1 + np.sum(A*B, -1) + np.sum(B*C, -1) + np.sum(C*A, -1)
        return 2*np.arctan2(num, den)
    out = []
    for u in (m1, m2):
        q = tri(u, np.roll(u, -1, 1), np.roll(np.roll(u, -1, 0), -1, 1)) + \
            tri(u, np.roll(np.roll(u, -1, 0), -1, 1), np.roll(u, -1, 0))
        Q = q.sum()/(4*np.pi)
        ny, nx = q.shape
        jj, ii = np.mgrid[0:ny, 0:nx]
        k = np.unravel_index(np.argmax(np.abs(q)), q.shape)
        px, py = (k[1]+1)*a, (k[0]+1)*a
        L = nx*a
        dx = ((ii+1)*a - px + L/2) % L - L/2
        dy = ((jj+1)*a - py + L/2) % L - L/2
        out.append((Q, px + (q*dx).sum()/q.sum(), py + (q*dy).sum()/q.sum()))
    (Q1, x1, y1), (Q2, x2, y2) = out
    L = m1.shape[0]*a
    dx = ((x1-x2) + L/2) % L - L/2
    dy = ((y1-y2) + L/2) % L - L/2
    return Q1, Q2, np.hypot(dx, dy)


def ler(path, cols):
    raw = np.loadtxt(path)
    m1 = np.empty((100, 100, 3)); m2 = np.empty((100, 100, 3))
    i = raw[:, 0].astype(int); j = raw[:, 1].astype(int)
    m1[j, i] = raw[:, cols[0]:cols[0]+3]
    m2[j, i] = raw[:, cols[1]:cols[1]+3]
    return m1, m2


print("=" * 74)
print("MISSION-A004 — 𝒟 do mumax3 contra 𝒟 do saf.cu (ambos SELADOS)")
print("=" * 74)

est = {}
for nome, path in (("saf.cu ", "LAB/EVIDENCE/R001/mfinal_weak.dat"),
                   ("mumax3 ", "LAB/EVIDENCE/A003/mfinal_par_mumax3.dat")):
    m1, m2 = ler(path, (2, 5))
    Q1, Q2, l = bond(m1, m2)
    t1, t2 = tensor(m1), tensor(m2)
    Im = 0.5*(t1[3] + t2[3])
    est[nome] = dict(l=l*1e9, Q1=Q1, Q2=Q2, I=Im, D=PRE*Im,
                     aniso=abs(t1[0]-t1[1])/t1[0], offd=abs(t1[2])/t1[0])
    print(f"\n{nome}  ({path.split('/')[-1]})")
    print(f"   l = {l*1e9:.4f} nm   Q1 = {Q1:+.6f}   Q2 = {Q2:+.6f}")
    print(f"   I (adimensional) = {Im:.6f}      𝒟 = {PRE*Im*1e15:.4f} e-15 N s/m")
    print(f"   |Ixx-Iyy|/Ixx = {est[nome]['aniso']:.5f}   |Ixy|/Ixx = {est[nome]['offd']:.2e}")

s, mu = est["saf.cu "], est["mumax3 "]
print("\n--- AD-0  os estados sao comparaveis?")
print(f"   l: {s['l']:.4f} vs {mu['l']:.4f} nm  ->  {100*(mu['l']-s['l'])/s['l']:+.3f} %")
print("   (registrado ANTES: a comparacao de 𝒟 herda essa diferenca; abaixo de ~1 %")
print("    uma diferenca de 𝒟 nao e' distinguivel dela)")

r = mu['I']/s['I']
print(f"\n--- AD-1  PRIMARIO: razao I_mumax3 / I_saf.cu = {r:.6f}  ({100*(r-1):+.3f} %)")
print(f"   referencia medida: o MV-1 deu 0.019 % de diferenca no raio;")
print(f"   o C-12 mediu que 3.2 % de diferenca de tamanho ja e' detectavel.")
if abs(r-1) < 0.01:
    v = "as duas formas sao as MESMAS -> sob R1 seriam OS DOIS codigos a diferir do artigo em ~30 %.\n   R1 fica MENOS PLAUSIVEL. O D-1 segue ABERTO."
elif abs(r-1) > 0.05:
    v = "as formas DIFEREM -> o PV-0 media peculiaridade nossa. R1 volta a ser a leitura natural."
else:
    v = "entre 1 % e 5 %: INCONCLUSIVO. Sem escolher lado."
print(f"   ==> {v}")

print("\n--- para o registro: as duas leituras do eixo da Fig. 2(c)")
print(f"   R1 (eixo em 1e-15): artigo I = {15.0/(PRE*1e15):.3f}   nosso {s['I']:.3f}  -> {100*(s['I']/(15.0/(PRE*1e15))-1):+.1f} %")
g0 = 4*np.pi*1e-7*GAMMA
print(f"   R2 (gamma0={g0:.5e}, eixo em 1e-9): artigo I = {15.0e-9/(Ms*d/g0):.3f}   nosso {s['I']:.3f}  -> {100*(s['I']/(15.0e-9/(Ms*d/g0))-1):+.1f} %")
print("\n   NENHUMA das duas e' fechada por esta missao. So os autores fechariam.")
