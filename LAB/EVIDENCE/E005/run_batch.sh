#!/usr/bin/env bash
# MISSION-E005 — Fig. S4(c). Rodar SEMPRE da raiz do projeto (ENVIRONMENT.md).
cd /home/rodrigo/pesquisa/SAF || exit 1
S=./LAB/EVIDENCE/E005/saf_amp
L=LAB/EVIDENCE/E005/RUN-LOG.txt
: > "$L"
echo "=== INICIO $(date -Is)  14 corridas de 300 ns, theta=0, SBM" >> "$L"
for A in 0.002 0.008; do
  for f in 17.00 17.25 17.50 17.75 18.00 18.25 18.50; do
    echo "=== $(date -Is)  dK/K0=$A  f=$f GHz" >> "$L"
    /usr/bin/time -f "WALL %e s" $S prop sbm "$f" 300 10 "sbm_A${A}_${f}GHz" 0.0 1.0 "$A" >> "$L" 2>&1
  done
done
echo "=== $(date -Is)  LOTE E005 COMPLETO" >> "$L"
