#!/usr/bin/env bash
cd /home/rodrigo/pesquisa/SAF || exit 1
S=./LAB/EVIDENCE/I002/saf_inst2
L=LAB/EVIDENCE/I002/RUN-LOG.txt
: > "$L"
for K in 0.55 0.60 0.65 0.70; do
  echo "=== $(date -Is)  K0=$K MJ/m3, theta=30, SEM excitacao" >> "$L"
  /usr/bin/time -f "WALL %e s" $S prop none 18.00 20 10 "il_K${K}_th30" 30.0 1.0 "$K" >> "$L" 2>&1
done
echo "=== $(date -Is)  LOTE I002 COMPLETO" >> "$L"
