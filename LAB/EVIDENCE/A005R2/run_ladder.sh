#!/usr/bin/env bash
# A005R2 Estagio F — escada com checkpoints. Cada degrau: processo separado, timeout 900 s.
# Orcamento: 4 processos, 3600 s de parede. NAO aumentar timeout depois de ver l.
cd /home/rodrigo/pesquisa/SAF || exit 1
A=LAB/EVIDENCE/A005R2; L=$A/LADDER-LOG.txt
S=/tmp/claude-1000/-home-rodrigo-pesquisa-SAF/471574db-345c-43d2-a045-35b73207a394/scratchpad
: > "$L"
ALVOS=(2e-5 1e-5 3e-6 1e-6)
T0=$(date +%s)
for k in 1 2 3 4; do
  [ $k -gt 1 ] && [ ! -f "$A/ck$((k-1)).ovf" ] && { echo "=== degrau $k NAO INICIADO: checkpoint anterior ausente" >> "$L"; break; }
  echo "=== $(date -Is)  degrau $k  alvo ${ALVOS[$((k-1))]} T" >> "$L"
  rm -rf $S/f$k.out
  /usr/bin/time -f "WALL %e s" timeout 900 ./TOOLS/mumax3-bin -o $S/f$k.out -f $A/f${k}_degrau.mx3 >> "$L" 2>&1
  rc=$?
  if [ $rc -eq 0 ] && [ -f $S/f$k.out/m000000.ovf ]; then
    cp $S/f$k.out/m000000.ovf $A/ck$k.ovf
    echo "--- degrau $k COMPLETO, checkpoint ck$k.ovf" >> "$L"
  else
    echo "--- degrau $k EXPIROU/FALHOU (rc=$rc). Escada encerrada; degraus anteriores preservados." >> "$L"
    break
  fi
  T1=$(date +%s); [ $((T1-T0)) -gt 3600 ] && { echo "--- teto de 3600 s atingido; escada encerrada" >> "$L"; break; }
done
echo "=== $(date -Is)  ESCADA ENCERRADA (parede $(( $(date +%s)-T0 )) s)" >> "$L"
