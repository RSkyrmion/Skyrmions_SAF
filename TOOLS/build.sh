#!/usr/bin/env bash
# Build do mumax3 a partir do fonte arquivado. Autorizado por WRITEBACK-021 (acao de sistema).
set -o pipefail
cd /home/rodrigo/pesquisa/SAF/TOOLS/mumax3 || exit 1
export GOROOT=/home/rodrigo/pesquisa/SAF/TOOLS/go
export GOPATH=/home/rodrigo/pesquisa/SAF/TOOLS/gopath
export PATH="$GOROOT/bin:$PATH"
export CUDA_HOME=/usr
L=/home/rodrigo/pesquisa/SAF/TOOLS/BUILD-LOG.txt
: > "$L"
{
  echo "=== INICIO $(date -Is)"
  go version; nvcc --version | tail -2
  echo "=== 1) kernels CUDA, CUDA_CC=89 (sm_89, o da RTX 4050)"
  ( cd cuda && make CUDA_CC=89 NVCC_CCBIN=/usr/bin/gcc-11 2>&1 | tail -25 )
  echo "=== rc kernels: $?"
  echo "=== 2) binario"
  go build -o /home/rodrigo/pesquisa/SAF/TOOLS/mumax3-bin ./cmd/mumax3 2>&1 | tail -25
  echo "=== rc binario: $?"
  echo "=== FIM $(date -Is)"
} >> "$L" 2>&1
