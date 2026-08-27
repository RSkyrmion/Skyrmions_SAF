#!/usr/bin/env bash
cd /home/rodrigo/pesquisa/SAF || exit 1
S=./LAB/EVIDENCE/I003/saf_dt
L=LAB/EVIDENCE/I003/RUN-LOG.txt
: > "$L"
# ID-1: mesma malha (0.5 nm), mesmo estado, dt=10 fs contra dt=2.5 fs, janela de 4 ns
for DT in 10 2.5; do
  echo "=== $(date -Is)  malha 0.5 nm, dt=${DT} fs, theta=30, SEM excitacao, 4 ns" >> "$L"
  /usr/bin/time -f "WALL %e s" $S prop none 18.00 4 "$DT" "id1_mesh05_dt${DT}fs" 30.0 0.5 >> "$L" 2>&1
done
echo "=== $(date -Is)  LOTE I003 COMPLETO" >> "$L"
