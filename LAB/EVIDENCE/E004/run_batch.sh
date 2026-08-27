#!/usr/bin/env bash
# MISSION-E004 — lote nao supervisionado (WRITEBACK-014). Destacado: sobrevive ao logout.
cd /home/rodrigo/pesquisa/SAF || exit 1
S=./LAB/EVIDENCE/E004/saf_prop4
L=LAB/EVIDENCE/E004/RUN-LOG.txt
: > "$L"
echo "=== INICIO $(date -Is)  (8 corridas de 100 ns; 18.00 GHz vem do E002)" >> "$L"
for f in 16.50 17.00 17.50 17.75 18.25 18.50 19.00 19.50; do
  echo "=== $(date -Is)  sbm f=$f GHz" >> "$L"
  /usr/bin/time -f "WALL %e s" $S prop sbm "$f" 100 10 "sbm_${f}GHz" 0.0 >> "$L" 2>&1
done
echo "=== $(date -Is)  LOTE E004 COMPLETO" >> "$L"
python3 LAB/EVIDENCE/E004/analyze4.py > LAB/EVIDENCE/E004/CRITERIOS-RESULTADOS.txt 2>&1
echo "=== $(date -Is)  ANALISE ESCRITA em CRITERIOS-RESULTADOS.txt" >> "$L"
