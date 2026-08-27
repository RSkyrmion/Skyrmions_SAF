#!/usr/bin/env bash
cd /home/rodrigo/pesquisa/SAF || exit 1
L=LAB/EVIDENCE/A005/RUN-LOG.txt
S=/tmp/claude-1000/-home-rodrigo-pesquisa-SAF/471574db-345c-43d2-a045-35b73207a394/scratchpad
: > "$L"
for t in ar0_no_eixo ar1_fora_eixo; do
  echo "=== $(date -Is)  $t" >> "$L"
  rm -rf $S/$t.out
  /usr/bin/time -f "WALL %e s" ./TOOLS/mumax3-bin -o $S/$t.out -f LAB/EVIDENCE/A005/$t.mx3 >> "$L" 2>&1
  echo "--- ovf gravados: $(ls $S/$t.out/*.ovf 2>/dev/null | wc -l)" >> "$L"
done
echo "=== $(date -Is)  LOTE A005 COMPLETO" >> "$L"
