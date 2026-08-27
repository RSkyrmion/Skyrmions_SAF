#!/usr/bin/env bash
cd /home/rodrigo/pesquisa/SAF || exit 1
L=LAB/EVIDENCE/A005R/RUN-LOG.txt
S=/tmp/claude-1000/-home-rodrigo-pesquisa-SAF/471574db-345c-43d2-a045-35b73207a394/scratchpad
: > "$L"
for t in ac3_par ac1_theta0 ac2_theta30; do
  echo "=== $(date -Is)  $t" >> "$L"
  rm -rf $S/$t.out
  /usr/bin/time -f "WALL %e s" timeout 3600 ./TOOLS/mumax3-bin -o $S/$t.out -f LAB/EVIDENCE/A005R/$t.mx3 >> "$L" 2>&1
  echo "--- ovf: $(ls $S/$t.out/*.ovf 2>/dev/null | wc -l)" >> "$L"
done
echo "=== $(date -Is)  LOTE A005R COMPLETO" >> "$L"
