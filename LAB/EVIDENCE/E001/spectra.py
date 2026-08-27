import numpy as np, sys
# Fundos opostos: camada 1 tem <mz>=+0.97, camada 2 -0.97. Se AMBOS os skyrmions
# expandem (SBM), <mz1> cai e <mz2> sobe -> dmz0 e dmz1 ANTICORRELACIONADOS.
# Logo:  SBM <-> (dmz0 - dmz1)   e   ABM <-> (dmz0 + dmz1).
def load(fn):
    d=np.loadtxt(fn); return d[:,0], d[:,1], d[:,2]
def peak(t,y,lo=2e9,hi=60e9):
    y=y-y.mean(); n=len(y); dt=t[1]-t[0]
    F=np.abs(np.fft.rfft(y*np.hanning(n)))**2
    f=np.fft.rfftfreq(n,dt); m=(f>lo)&(f<hi)
    return f[m][np.argmax(F[m])], f, F
for tag,fn in [('SBM','LAB/EVIDENCE/E001/ev3_sbm_10ns.dat'),
               ('ABM','LAB/EVIDENCE/E001/ev3_abm_10ns.dat')]:
    t,a,b=load(fn)
    r=np.corrcoef(a,b)[0,1]
    fS,_,_=peak(t,a-b); fA,_,_=peak(t,a+b)
    print('excitacao %s:  corr(dmz0,dmz1)=%+.4f  ->  %s' %
          (tag, r, 'anticorrelacionados (respiram EM FASE = SBM)' if r<0 else 'correlacionados (ANTIfase = ABM)'))
    print('   canal SBM (dmz0-dmz1): %6.2f GHz     canal ABM (dmz0+dmz1): %6.2f GHz' % (fS*1e-9,fA*1e-9))
