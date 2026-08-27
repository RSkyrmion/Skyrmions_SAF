#!/usr/bin/env python3
"""E002 — diagnostico do PV-0 (que FALHOU: 19.43 contra a banda [13.5,16.5]e-15).

A taxonomia pre-registrada (§7) manda suspeitar primeiro do estimador/unidades.
Aqui o tensor D e' verificado contra a ENERGIA DE TROCA, que ja e' validada por
diferencas finitas (VL-1, R001 selado):

    E_ex = A d \\int |grad m|^2 d^2r     =>     Dxx+Dyy = (Ms d/gamma)*E_ex/(A d)

Se as duas rotas baterem, o estimador esta certo e a discrepancia nao e' de
unidade. Roda sobre o estado de equilibrio SELADO do R001, nao sobre dado novo.
"""
import sys
import numpy as np

GAMMA = 1.760859e11   # rad s^-1 T^-1  (convencao TESLA, fixada em MISSION-E001)
A, K, Ms, d, a = 15e-12, 0.6e6, 0.58e6, 0.4e-9, 1e-9
N = 100

SRC = sys.argv[1] if len(sys.argv) > 1 else "LAB/EVIDENCE/R001/mfinal_weak.dat"
print(f"estado: {SRC}")
raw = np.loadtxt(SRC)
m = np.empty((2, N, N, 3))
i, j = raw[:, 0].astype(int), raw[:, 1].astype(int)
m[0, j, i] = raw[:, 2:5]
m[1, j, i] = raw[:, 5:8]

pre = Ms * d / GAMMA
print(f"Ms*d/gamma = {pre:.6e} N s/m      (gamma em rad/s/T; e' o que fecha N s/m)")
print()

for L in range(2):
    u = m[L]
    # centrada (o que o dissip() do saf_prop.cu faz)
    dxc = (np.roll(u, -1, 0) - np.roll(u, 1, 0)) / (2 * a)   # eixo 0 = j = y
    dyc = (np.roll(u, -1, 1) - np.roll(u, 1, 1)) / (2 * a)   # eixo 1 = i = x
    # NOTA: eixo0=j=y, eixo1=i=x -> renomeia
    dY, dX = dxc, dyc
    Ixx = (dX * dX).sum() * a * a
    Iyy = (dY * dY).sum() * a * a
    Ixy = (dX * dY).sum() * a * a
    # avancada / de ligacao (a MESMA forma usada na energia de troca do kernel)
    fX = (np.roll(u, -1, 1) - u) / a
    fY = (np.roll(u, -1, 0) - u) / a
    Ixx_f = (fX * fX).sum() * a * a
    Iyy_f = (fY * fY).sum() * a * a
    # energia de troca pela forma de ligacao do kernel: A*d*sum|m(r+u)-m(r)|^2
    Eex = A * d * (((np.roll(u, -1, 1) - u) ** 2).sum() + ((np.roll(u, -1, 0) - u) ** 2).sum())

    Dxx, Dyy, Dxy = pre * Ixx, pre * Iyy, pre * Ixy
    det = np.sqrt(Dxx * Dyy - Dxy * Dxy)
    rota2 = pre * Eex / (A * d)          # = (Ms d/gamma) * int|grad m|^2
    print(f"--- camada {L+1}")
    print(f"  int|dx m|^2 d2r (centrada) = {Ixx:.6f}   (avancada) = {Ixx_f:.6f}")
    print(f"  int|dy m|^2 d2r (centrada) = {Iyy:.6f}   (avancada) = {Iyy_f:.6f}")
    print(f"  Dxx={Dxx:.6e}  Dyy={Dyy:.6e}  Dxy={Dxy:.3e}   sqrt(det)={det:.6e} N s/m")
    print(f"  ROTA 1 (tensor, centrada) Dxx+Dyy      = {Dxx+Dyy:.9e}")
    print(f"  ROTA 2 (energia de troca) Ms*Eex/(g*A) = {rota2:.9e}")
    print(f"  razao rota2/rota1 = {rota2/(Dxx+Dyy):.6f}   "
          f"(a diferenca esperada e' so o stencil: avancada vs centrada)")
    print(f"  E_ex = {Eex:.6e} J")

# --- tamanho do skyrmion: raio onde mz cruza zero, a partir da CTC ------------
u = m[0]
mz = u[:, :, 2]
jj, ii = np.mgrid[0:N, 0:N]
q = mz < 0                        # nucleo da camada 1 aponta para baixo
cy, cx = jj[q].mean(), ii[q].mean()
r = np.hypot(ii - cx, jj - cy).ravel()
z = mz.ravel()
o = np.argsort(r)
r, z = r[o], z[o]
k = np.argmax(z > 0)
R = np.interp(0.0, [z[k-1], z[k]], [r[k-1], r[k]])
print(f"\nraio do skyrmion (mz=0), camada 1 = {R:.4f} nm    area do nucleo = {q.sum()} celulas")
print(f"comprimento de parede  Delta = sqrt(A/K) = {np.sqrt(A/K)*1e9:.4f} nm")
