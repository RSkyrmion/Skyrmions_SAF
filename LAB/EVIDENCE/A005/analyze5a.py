#!/usr/bin/env python3
"""MISSION-A005 — AR-0 e AR-1, conforme MISSION-A005.md §3-§4."""
import sys, glob, re
import numpy as np
sys.path.insert(0, 'LAB/EVIDENCE/A005')
from ovf import read_ovf

S = '/tmp/claude-1000/-home-rodrigo-pesquisa-SAF/471574db-345c-43d2-a045-35b73207a394/scratchpad'
A = 1e-9


def tri(A_, B_, C_):
    num = (A_[..., 0]*(B_[..., 1]*C_[..., 2]-B_[..., 2]*C_[..., 1]) +
           A_[..., 1]*(B_[..., 2]*C_[..., 0]-B_[..., 0]*C_[..., 2]) +
           A_[..., 2]*(B_[..., 0]*C_[..., 1]-B_[..., 1]*C_[..., 0]))
    den = 1 + np.sum(A_*B_, -1) + np.sum(B_*C_, -1) + np.sum(C_*A_, -1)
    return 2*np.arctan2(num, den)


def ctc(u, a=A):
    """CTC de Berg-Luscher, desdobrada em torno do pico de |rho| (robusta a PBC)."""
    q = (tri(u, np.roll(u, -1, 1), np.roll(np.roll(u, -1, 0), -1, 1)) +
         tri(u, np.roll(np.roll(u, -1, 0), -1, 1), np.roll(u, -1, 0)))
    Q = q.sum()/(4*np.pi)
    ny, nx = q.shape
    jj, ii = np.mgrid[0:ny, 0:nx]
    k = np.unravel_index(np.argmax(np.abs(q)), q.shape)
    px, py = (k[1]+1)*a, (k[0]+1)*a
    L = nx*a
    dx = ((ii+1)*a - px + L/2) % L - L/2
    dy = ((jj+1)*a - py + L/2) % L - L/2
    return Q, px + (q*dx).sum()/q.sum(), py + (q*dy).sum()/q.sum()


def trajetoria(tag):
    fs = sorted(glob.glob(f'{S}/{tag}.out/m*.ovf'))
    T, X, Y, BX, BY = [], [], [], [], []
    for k, f in enumerate(fs):
        hdr, d = read_ovf(f)
        t = float(hdr.get('total simulation time', k*1e-9).split()[0]) \
            if 'total simulation time' in hdr else k*1e-9
        (q1, x1, y1), (q2, x2, y2) = ctc(d[0]), ctc(d[1])
        T.append(t); X.append(0.5*(x1+x2)); Y.append(0.5*(y1+y2))
        BX.append(x1-x2); BY.append(y1-y2)
    return (np.array(T), np.array(X), np.array(Y), np.array(BX), np.array(BY))


print("="*74); print("MISSION-A005 — o artefato de rede aparece no mumax3?"); print("="*74)
res = {}
for tag, nome, thn in (("ar0_no_eixo", "AR-0  theta=0 (no eixo)", 0.0),
                       ("ar1_fora_eixo", "AR-1  theta=30 (fora do eixo)", 30.0)):
    T, X, Y, BX, BY = trajetoria(tag)
    s = T >= T[0] + 5e-9                       # descarta os primeiros ~5 ns
    vx = np.polyfit(T[s], X[s], 1)[0]*100
    vy = np.polyfit(T[s], Y[s], 1)[0]*100
    ang = np.degrees(np.arctan2(BY[s].mean(), BX[s].mean()))
    px, py = np.cos(np.radians(ang)), np.sin(np.radians(ang))
    vpar, vperp = vx*px+vy*py, -vx*py+vy*px
    res[tag] = (np.hypot(vx, vy), vpar, vperp, ang)
    print(f"\n{nome}   ({len(T)} estados, t = {T[0]*1e9:.1f}..{T[-1]*1e9:.1f} ns)")
    print(f"   theta_ligacao = {ang:+.3f} deg   (inicial {thn:+.1f})")
    print(f"   |v| = {np.hypot(vx,vy):.5f} cm/s     v_par = {vpar:+.5f}   v_perp = {vperp:+.5f}")
    print(f"   angulo da deriva vs ligacao = {np.degrees(np.arctan2(vperp,vpar)):+.2f} deg")

print("\n--- AR-0  criterio: |v| < 0.05 cm/s (o mumax3 preserva estado estatico?)")
v0 = res['ar0_no_eixo'][0]
print(f"   |v| = {v0:.5f} cm/s   -> {'PASSOU' if v0 < 0.05 else 'FALHOU — A007 BLOQUEADA'}")
print(f"   referencia: o E003 mediu 7.1e-05 cm/s aqui com o saf.cu")

print("\n--- AR-1  PRIMARIO")
v1p = abs(res['ar1_fora_eixo'][1])
print(f"   |v_par| mumax3 = {v1p:.5f} cm/s")
print(f"   |v_par| saf.cu (E003, mesma condicao) = 0.91745 cm/s")
print(f"   razao mumax3/saf.cu = {v1p/0.91745:.4f}")
print(f"\n   H_comum previa ~0.9 cm/s ao longo da ligacao;  H_nosso previa ~0")
if v1p > 0.3:
    print("   ==> H_COMUM: o artefato aparece nos DOIS codigos. E' discretizacao, nao nosso.")
elif v1p < 0.1:
    print("   ==> H_NOSSO: o artefato NAO aparece no mumax3. ACHADO GRAVE — toca o C-8.")
else:
    print("   ==> intermediario; relatar sem escolher lado.")
