import numpy as np, struct, re
def read_ovf(fn):
    hdr={}; 
    with open(fn,'rb') as f:
        line=f.readline()
        while line:
            s=line.decode('latin1').strip()
            if s.startswith('# Begin: Data'):
                mode=s.split('Data',1)[1].strip(); break
            m=re.match(r'#\s*([\w ]+):\s*(.*)',s)
            if m: hdr[m.group(1).strip().lower()]=m.group(2).strip()
            line=f.readline()
        nx,ny,nz=(int(hdr[k]) for k in ('xnodes','ynodes','znodes'))
        n=nx*ny*nz
        if mode.lower().startswith('binary'):
            nb=int(mode.split()[-1]); fmt='<d' if nb==8 else '<f'
            chk=struct.unpack(fmt,f.read(nb))[0]
            expect=123456789012345.0 if nb==8 else 1234567.0
            assert abs(chk-expect)<1e-3*abs(expect), f"check {chk}"
            dt=np.dtype('<f8' if nb==8 else '<f4')
            d=np.frombuffer(f.read(n*3*dt.itemsize),dtype=dt).reshape(nz,ny,nx,3)
        else:
            vals=[]
            for line in f:
                s=line.decode('latin1').strip()
                if s.startswith('#'): break
                vals.extend(float(x) for x in s.split())
            d=np.array(vals).reshape(nz,ny,nx,3)
    return hdr,d.astype(float)

if __name__=='__main__':
    import sys, math
    mu0=4*math.pi*1e-7
    for fn in sys.argv[1:]:
        h,d=read_ovf(fn)
        print(f"--- {fn.split('/')[-1]}")
        print("   grid", h.get('xnodes'),h.get('ynodes'),h.get('znodes'), "| unit", h.get('valueunits',h.get('valueunit','?')))
        for z in range(d.shape[0]):
            H=d[z]; mag=np.linalg.norm(H,axis=-1)
            print(f"   z={z}: |H|med={mag.mean():.6e} A/m   -> |B|={mu0*mag.mean():.6f} T   Hz_med={H[...,2].mean():+.6e}")
