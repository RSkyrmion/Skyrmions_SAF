#!/usr/bin/env python3
"""A008 — gera o .mx3 de um degrau de malha. Convencoes herdadas do MV-0 do A003.

O acoplamento interlayer NAO depende da malha no plano: a energia de troca entre
vizinhos em z vale A_inter*Area*|dm|^2/dz, e Area e dz sao fixos. Logo A_inter =
-A_int*dz/2 = -4e-15 J/m vale em todas as malhas. (Verificado no MV-0.4 do A003.)
"""
import sys
a_nm, rodada, prev = float(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
n = int(round(100.0 / a_nm))
a = a_nm * 1e-9
tag = f"a{a_nm:g}nm_r{rodada}"
ini = (f'm.SetRegion(1, neelskyrmion( 1, -1).Transl(-5e-9, 0, 0))\n'
       f'm.SetRegion(2, neelskyrmion( 1,  1).Transl( 5e-9, 0, 0))\nrelax()')  \
      if prev == "NONE" else f'm.LoadFile("{prev}")'
print(f"""// A008 — malha {a_nm} nm, rodada {rodada}. cwd fixo: /home/rodrigo/pesquisa/SAF
SetGridSize({n}, {n}, 2)
SetCellSize({a:.6e}, {a:.6e}, 0.4e-9)
SetPBC(2, 2, 0)
EnableDemag = false
Msat = 0.58e6
Aex  = 15e-12
Ku1  = 0.6e6
anisU = vector(0, 0, 1)
defregion(1, zrange(-1e-9, 0))
defregion(2, zrange(0, 1e-9))
Dind.SetRegion(1,  3.05e-3)
Dind.SetRegion(2, -3.05e-3)
ext_InterDind(1, 2, 0)
ext_InterExchange(1, 2, -4e-15)
MinimizerStop = 1e-8
{ini}
minimize()
print("A008 {tag}  MaxTorque =", MaxTorque, "  E_total =", E_total, "  <m> =", m.average())
save(m)""")
