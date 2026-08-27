#!/usr/bin/env python3
"""MISSION-R002 — analise da varredura (Aint, K0).
Aplica os criterios PRE-REGISTRADOS em MISSION-R002.md. Nao inventa criterio novo."""
import sys, csv
from collections import defaultdict

rows=list(csv.DictReader(open(sys.argv[1] if len(sys.argv)>1
                              else 'LAB/EVIDENCE/R002/scan_full.csv')))
by=defaultdict(dict)
for r in rows: by[float(r['Aint'])][float(r['K0'])]=r

# Sobreposicao dos pontos AMBIGUOUS reexecutados com orcamento maior.
# O scan_full.csv NAO e' reescrito (INV-07): a resolucao vive em arquivo separado.
import os
RES='LAB/EVIDENCE/R002/ambiguous_resolved.csv'
if os.path.exists(RES):
    for r in csv.DictReader(open(RES)):
        A,K=float(r['Aint']),float(r['K0'])
        old=by[A].get(K,{}).get('classe','?')
        by[A][K]=r
        print(f"[resolucao] (Aint={A}, K0={K}): {old} -> {r['classe']} "
              f"(orcamento maior, l={float(r['l_nm']):.4f} nm). scan_full.csv preservado.")

STABLE={'COAXIAL','NONCOAXIAL'}
print("="*78); print("MISSION-R002 — resultado contra criterios pre-registrados"); print("="*78)

# ---- criterio PRIMARIO (binario, e' o que discrimina) ----
print("\n[PRIMARIO] pontos publicados dentro da regiao STABLE")
prim=True
for A,K in [(0.02,0.60),(0.12,0.35)]:
    r=by.get(A,{}).get(K)
    if r is None: print(f"  (Aint={A}, K0={K}): AUSENTE da varredura"); prim=False; continue
    ok=r['classe'] in STABLE
    prim&=ok
    print(f"  (Aint={A:.2f}, K0={K:.2f}) -> {r['classe']:<11} l={float(r['l_nm']):7.4f} nm   {'PASSA' if ok else '** FALHA **'}")
print(f"  => PRIMARIO: {'PASSOU' if prim else 'FALHOU'}")

# ---- janelas, centro, fronteira ----
print("\n[estrutura por coluna]")
print(f"  {'Aint':>6} {'janela STABLE':>18} {'semi-larg':>10} {'centro':>8} {'S1 preve':>9} {'fronteira cox/nao':>18}")
cent={}; bound={}
for A in sorted(by):
    ks=sorted(by[A]); st=[k for k in ks if by[A][k]['classe'] in STABLE]
    if not st: print(f"  {A:6.2f}  (nenhum ponto estavel)"); continue
    lo,hi=min(st),max(st); c=(lo+hi)/2; cent[A]=c
    # fronteira: maior K0 COAXIAL seguido de NONCOAXIAL
    b=None
    for i in range(len(ks)-1):
        if by[A][ks[i]]['classe']=='COAXIAL' and by[A][ks[i+1]]['classe']=='NONCOAXIAL':
            b=(ks[i]+ks[i+1])/2
    if b is not None: bound[A]=b
    print(f"  {A:6.2f}  [{lo:.3f}, {hi:.3f}]   {(hi-lo)/2:9.3f} {c:8.3f} {0.65-2.5*A:9.3f}   "
          f"{('%.4f'%b) if b is not None else 'ausente':>18}")

# ---- criterio TERCIARIO (qualitativo, robusto) ----
print("\n[TERCIARIO] janela desce em K0 monotonicamente com Aint")
As=sorted(cent); mono=all(cent[As[i+1]]<cent[As[i]] for i in range(len(As)-1))
print(f"  centros: {[f'{cent[a]:.3f}' for a in As]}")
print(f"  => TERCIARIO: {'PASSOU (monotono decrescente)' if mono else 'FALHOU (nao monotono)'}")

# ---- criterio SECUNDARIO: declarado morto na checagem de poder ----
print("\n[SECUNDARIO] ajuste da linha de centro")
hw=[(max(k for k in by[A] if by[A][k]['classe'] in STABLE)
     -min(k for k in by[A] if by[A][k]['classe'] in STABLE))/2 for A in As]
print(f"  semi-larguras: {[f'{h:.3f}' for h in hw]}  (media {sum(hw)/len(hw):.3f})")
print("  => NAO-DISCRIMINANTE por pre-registro (janela >= +-0.15). Nao usado como evidencia.")
if len(As)>1:
    n=len(As); sx=sum(As); sy=sum(cent[a] for a in As)
    sxx=sum(a*a for a in As); sxy=sum(a*cent[a] for a in As)
    m=(n*sxy-sx*sy)/(n*sxx-sx*sx); b0=(sy-m*sx)/n
    print(f"  (so para registro, NAO como sucesso) inclinacao={m:+.3f} (S1: -2.5), intercepto={b0:.3f} (S1: 0.65)")

# ---- teste NOVO: fronteira coaxial/nao-coaxial (origem post-hoc declarada) ----
print("\n[ramo COAXIAL: largura por coluna]")
for A in sorted(by):
    ks=[k for k in by[A] if by[A][k]['classe']=='COAXIAL']
    if ks: print(f"  Aint={A:.2f}  coaxial em [{min(ks):.3f}, {max(ks):.3f}]  largura {max(ks)-min(ks):.3f}  ({len(ks)} pontos)")
    else:  print(f"  Aint={A:.2f}  ramo coaxial AUSENTE na faixa varrida")

print("\n[TESTE NOVO] fronteira coaxial<->nao-coaxial  (DISCOVERY_ONLY em Aint=0.02)")
Ab=sorted(bound)
print(f"  existe em {len(Ab)}/{len(by)} colunas: {[f'{a:.2f}' for a in Ab]}")
if len(Ab)>1:
    mo=all(bound[Ab[i+1]]<bound[Ab[i]] for i in range(len(Ab)-1))
    print(f"  valores: {[f'{bound[a]:.4f}' for a in Ab]}")
    print(f"  desce monotonicamente com Aint: {'SIM' if mo else 'NAO'}")
    n=len(Ab); sx=sum(Ab); sy=sum(bound[a] for a in Ab)
    sxx=sum(a*a for a in Ab); sxy=sum(a*bound[a] for a in Ab)
    mb=(n*sxy-sx*sy)/(n*sxx-sx*sx)
    print(f"  inclinacao da fronteira: {mb:+.3f}  (linha de centro: ver acima) -> observaveis NAO redundantes")
    print("  NOTA: teste estrutural/qualitativo. Nao ha valores numericos extraiveis da")
    print("        linha tracejada da Fig. 5(c); isto pode REFUTAR a leitura, nao confirma-la")
    print("        com precisao numerica.")
