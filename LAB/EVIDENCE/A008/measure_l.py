#!/usr/bin/env python3
"""A008 — mede l de um OVF pelo ESTIMADOR CEGO do AUDIT-002, com 'a' como argumento."""
import sys, subprocess, pathlib
sys.path.insert(0, "LAB/EVIDENCE/A003")
from ovf import read_ovf
ovf, a_m, tmp = sys.argv[1], float(sys.argv[2]), sys.argv[3]
hdr, d = read_ovf(ovf)
m1, m2 = d[0], d[1]
ny, nx, _ = m1.shape
with open(tmp, "w") as f:
    f.write("# i j m0x m0y m0z m1x m1y m1z\n")
    for j in range(ny):
        for i in range(nx):
            p, q = m1[j, i], m2[j, i]
            f.write(f"{i} {j} {p[0]:.10f} {p[1]:.10f} {p[2]:.10f} {q[0]:.10f} {q[1]:.10f} {q[2]:.10f}\n")
out = subprocess.run(["python3", "LAB/EVIDENCE/AUDIT-002/estimator.py", tmp, repr(a_m)],
                     capture_output=True, text=True).stdout
d = {k.strip(): v.strip() for k, v in (x.split("=", 1) for x in out.strip().split("\n") if "=" in x)}
print(f"{float(d['l'])*1e9:.6f} {d['Q1']} {d['Q2']}")
