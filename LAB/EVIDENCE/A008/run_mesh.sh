#!/usr/bin/env bash
# A008 — roda uma malha ate l convergir (< 0.001 nm entre rodadas), com recibo por processo.
# AM-0.3: convergencia checada na SAIDA (l), NUNCA no torque.
cd /home/rodrigo/pesquisa/SAF || exit 1
A=LAB/EVIDENCE/A008; S=/tmp/claude-1000/-home-rodrigo-pesquisa-SAF/471574db-345c-43d2-a045-35b73207a394/scratchpad/a008
a_nm=$1; L=$A/MESH-LOG.txt; mkdir -p $S
prev=NONE; lprev=""
for r in 1 2 3 4; do
  mx=$A/mesh_a${a_nm}nm_r${r}.mx3
  python3 $A/gen_mx3.py $a_nm $r "$prev" > $mx
  out=$S/a${a_nm}_r${r}.out; rm -rf $out
  python3 scripts/run_with_receipt.py --mission MISSION-A008 \
    --run-id "a${a_nm}nm-r${r}" --receipt $A/RUN-RECEIPTS/a${a_nm}nm-r${r}.json \
    --cwd /home/rodrigo/pesquisa/SAF --timeout 5400 \
    --parameters "{\"a_nm\":$a_nm,\"rodada\":$r,\"MinimizerStop\":1e-8}" \
    --executor "Claude (Claude Code)" --checkpoint "WRITEBACK-039" \
    --input "$mx" --output "$A/ck_a${a_nm}nm_r${r}.ovf" \
    -- ./TOOLS/mumax3-bin -o $out -f $mx >> "$L" 2>&1
  rc=$?
  [ ! -f $out/m000000.ovf ] && { echo "  a=$a_nm r=$r SEM OVF (rc=$rc) — malha encerrada" >> "$L"; break; }
  cp $out/m000000.ovf $A/ck_a${a_nm}nm_r${r}.ovf
  read l q1 q2 <<< "$(python3 $A/measure_l.py $A/ck_a${a_nm}nm_r${r}.ovf $(python3 -c "print($a_nm*1e-9)") $S/st.dat)"
  echo "  a=${a_nm}nm r=$r  l=${l} nm  Q1=${q1} Q2=${q2}" >> "$L"
  if [ -n "$lprev" ]; then
    d=$(python3 -c "print(abs($l-$lprev))")
    echo "     |dl| entre rodadas = ${d} nm  (criterio AM-0.3: < 0.001)" >> "$L"
    python3 -c "import sys; sys.exit(0 if abs($l-$lprev)<0.001 else 1)" && { echo "     CONVERGIU" >> "$L"; break; }
  fi
  lprev=$l; prev=$A/ck_a${a_nm}nm_r${r}.ovf
done
