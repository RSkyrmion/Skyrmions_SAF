import numpy as np
def _tri(a,b,c):
    num = np.einsum('...i,...i',a,np.cross(b,c))
    den = 1.0 + np.einsum('...i,...i',a,b) + np.einsum('...i,...i',b,c) + np.einsum('...i,...i',c,a)
    return 2.0*np.arctan2(num,den)

def charge(m, a, pbc=True):
    """m: (ny,nx,3) normalizado. Retorna Q e (Rx,Ry) em metros.
       Berg-Luscher: dois triangulos por celula; Omega atribuido ao centroide."""
    ny,nx,_ = m.shape
    if pbc:
        ip = np.roll(np.arange(nx),-1); jp = np.roll(np.arange(ny),-1)
    else:
        ip = np.minimum(np.arange(nx)+1, nx-1); jp = np.minimum(np.arange(ny)+1, ny-1)
    m00 = m
    m10 = m[:,ip,:]
    m01 = m[jp,:,:]
    m11 = m[np.ix_(jp,ip)]
    O1 = _tri(m00,m10,m11)
    O2 = _tri(m00,m11,m01)
    x = (np.arange(nx)+0.5)*a; y = (np.arange(ny)+0.5)*a
    X,Y = np.meshgrid(x,y)
    # centroides dos dois triangulos, deslocados de (a/3,a/3) e (a/3,2a/3)*
    c1x, c1y = X + 2*a/3, Y + a/3
    c2x, c2y = X + a/3,   Y + 2*a/3
    Q = (O1.sum()+O2.sum())/(4*np.pi)
    W = O1.sum()+O2.sum()
    Rx = (O1*c1x + O2*c2x).sum()/W
    Ry = (O1*c1y + O2*c2y).sum()/W
    return Q, Rx, Ry

def bond_length(m0, m1, a, pbc=True):
    Q0,x0,y0 = charge(m0,a,pbc); Q1,x1,y1 = charge(m1,a,pbc)
    l = np.hypot(x1-x0, y1-y0)
    return l, Q0, Q1

def read_saf_dat(fn, nx=None, ny=None):
    d = np.loadtxt(fn)
    i = d[:,0].astype(int); j = d[:,1].astype(int)
    nx = i.max()+1 if nx is None else nx; ny = j.max()+1 if ny is None else ny
    m0 = np.zeros((ny,nx,3)); m1 = np.zeros((ny,nx,3))
    m0[j,i,:] = d[:,2:5]; m1[j,i,:] = d[:,5:8]
    return m0,m1
