#!/usr/bin/env bash
# MISSION-E004R — lote destacado. Rodar SEMPRE da raiz do projeto (ENVIRONMENT.md).
cd /home/rodrigo/pesquisa/SAF || exit 1
S=./LAB/EVIDENCE/E004R/saf_prop4r
L=LAB/EVIDENCE/E004R/RUN-LOG.txt
: > "$L"
run(){ echo "=== $(date -Is)  $*" >> "$L"; /usr/bin/time -f "WALL %e s" $S "$@" >> "$L" 2>&1; }
echo "=== INICIO $(date -Is)" >> "$L"
# --- diagnosticos baratos primeiro ---
run rf3                                                    # RF-3  regua na fronteira PBC
run ev3 sbm 40                                             # RF-2  breathing a 0.025 GHz
run prop none 18.00 20 10 rf4_mesh05_th30 30.0 0.5         # RF-4  artefato com malha 0.5 nm
run prop none 18.00 20 10 rf4_mesh10_th30 30.0 1.0         # RF-4  referencia, malha 1.0 nm
# --- varredura de 300 ns: RF-0 / RF-1 ---
for f in 17.00 17.50 17.75 18.00 18.25; do
  run prop sbm "$f" 300 10 "sbm_${f}GHz" 0.0
done
echo "=== $(date -Is)  LOTE E004R COMPLETO" >> "$L"
