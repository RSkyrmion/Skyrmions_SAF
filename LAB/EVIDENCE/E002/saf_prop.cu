// ============================================================================
// MISSION-R001 — reproducao do par de skyrmions nao-coaxial em T=0
// PRL 135, 086701 (2025) — de Souza Silva, Correia, Pina Velasquez
//
// Modelo: Eq. (A3) do End Matter — integral AREAL sobre duas redes 2D.
//   H = \int dS [ E1*d + E2*d + Aint*m1.m2 ]
//   E_i = A[(dx m)^2+(dy m)^2] - K mz^2 - Ms B.m + D_i[mz(div m) - m.(grad mz)]
//
// Principio de construcao: escreve-se a ENERGIA DISCRETA primeiro; todo campo
// efetivo e' obtido dela por
//        Beff(r) = -(1/(Ms*d*a^2)) * dH/dm(r)
// e validado por diferencas finitas (modo `fd`). Isso faz o fator 1/d do termo
// interlayer (SL-2) aparecer sozinho, em vez de depender de memoria.
//
// Precisao dupla em todo lugar: a grade e' 100x100x2 = 2e4 spins (trivial), e
// o teste de FD exige. Nao ha motivo para float aqui.
// ============================================================================
#include <cstdio>
#include <cstdlib>
#include <cmath>
#include <cstring>
#include <vector>
#include <string>

#define CK(x) do{ cudaError_t e=(x); if(e!=cudaSuccess){ \
  fprintf(stderr,"CUDA %s @ %s:%d\n",cudaGetErrorString(e),__FILE__,__LINE__); exit(1);} }while(0)

// ------------------------------- parametros ---------------------------------
struct Par {
    int    nx, ny;      // celulas
    double a;           // lado da celula [m]
    double d;           // espessura da camada [m]
    double A;           // rigidez de troca [J/m]
    double K;           // anisotropia efetiva K = K0 (demag absorvido) [J/m^3]
    double Ms;          // magnetizacao de saturacao [A/m]
    double D1, D2;      // DMI por camada [J/m^2]
    double Aint;        // acoplamento interlayer areal [J/m^2]
    double Bz;          // campo externo [T]
};

__host__ __device__ inline int wrap(int i,int n){ return (i%n+n)%n; }
__host__ __device__ inline int idx(int i,int j,int nx,int ny){ return wrap(j,ny)*nx + wrap(i,nx); }

// ============================ MISSION-E001 ===================================
// Dinamica LLG (Eq. A1) acrescentada ao saf.cu ACEITO (WRITEBACK-007).
// Convencao fixada em MISSION-E001 §EV-2: gamma na convencao TESLA e TODO campo
// em tesla. Nao introduzir A/m em lugar nenhum.
static const double GAMMA_T = 1.760859e11;   // rad s^-1 T^-1

// ------------------------- energia por celula --------------------------------
// Cada celula recebe: suas ligacoes de troca +x e +y (cada ligacao contada uma
// vez), sua anisotropia, seu Zeeman, seu DMI e metade... nao: o termo interlayer
// e' contado UMA vez, no kernel da camada 0, para nao duplicar.
__global__ void k_energy(const double3* m0, const double3* m1, double* out, Par p)
{
    int c = blockIdx.x*blockDim.x + threadIdx.x;
    int n = p.nx*p.ny; if(c>=n) return;
    int i = c % p.nx, j = c / p.nx;

    double e = 0.0;
    for(int L=0; L<2; ++L){
        const double3* m = L? m1 : m0;
        double D = L? p.D2 : p.D1;
        double3 c0 = m[c];
        double3 px = m[idx(i+1,j,p.nx,p.ny)], mx = m[idx(i-1,j,p.nx,p.ny)];
        double3 py = m[idx(i,j+1,p.nx,p.ny)], my = m[idx(i,j-1,p.nx,p.ny)];

        // troca: forma de ligacao, A*d*|m(r+u)-m(r)|^2  (o a^2 cancela com 1/a^2)
        double dxx=px.x-c0.x, dxy=px.y-c0.y, dxz=px.z-c0.z;
        double dyx=py.x-c0.x, dyy=py.y-c0.y, dyz=py.z-c0.z;
        e += p.A*p.d*(dxx*dxx+dxy*dxy+dxz*dxz + dyx*dyx+dyy*dyy+dyz*dyz);

        // anisotropia e Zeeman
        e += -p.K*c0.z*c0.z * p.d*p.a*p.a;
        e += -p.Ms*p.Bz*c0.z * p.d*p.a*p.a;

        // DMI interfacial, diferencas centrais (MESMO stencil para div e grad)
        double S = (px.x-mx.x) + (py.y-my.y);          // 2a*(div m)
        double gx = (px.z-mx.z), gy = (py.z-my.z);     // 2a*(grad mz)
        e += (p.d*p.a*D*0.5) * ( c0.z*S - c0.x*gx - c0.y*gy );
    }
    // interlayer, areal — contado uma unica vez
    double3 u = m0[c], v = m1[c];
    e += p.a*p.a*p.Aint*(u.x*v.x + u.y*v.y + u.z*v.z);

    out[c] = e;
}

// ------------------------- campo efetivo -------------------------------------
// Beff = -(1/(Ms*d*a^2)) dH/dm  — derivada analitica da energia discreta acima.
__global__ void k_field(const double3* m0, const double3* m1, double3* b0, double3* b1, Par p)
{
    int c = blockIdx.x*blockDim.x + threadIdx.x;
    int n = p.nx*p.ny; if(c>=n) return;
    int i = c % p.nx, j = c / p.nx;

    for(int L=0; L<2; ++L){
        const double3* m = L? m1 : m0;
        const double3* o = L? m0 : m1;      // camada oposta
        double D = L? p.D2 : p.D1;
        double3 c0 = m[c];
        double3 px = m[idx(i+1,j,p.nx,p.ny)], mx = m[idx(i-1,j,p.nx,p.ny)];
        double3 py = m[idx(i,j+1,p.nx,p.ny)], my = m[idx(i,j-1,p.nx,p.ny)];

        // troca: (2A/(Ms a^2)) * laplaciano discreto
        double ce = 2.0*p.A/(p.Ms*p.a*p.a);
        double bx = ce*(px.x+mx.x+py.x+my.x - 4.0*c0.x);
        double by = ce*(px.y+mx.y+py.y+my.y - 4.0*c0.y);
        double bz = ce*(px.z+mx.z+py.z+my.z - 4.0*c0.z);

        // anisotropia + Zeeman
        bz += 2.0*p.K*c0.z/p.Ms;
        bz += p.Bz;

        // DMI: (D/(Ms a)) [ mz(r+x)-mz(r-x), mz(r+y)-mz(r-y), -S ]
        double S = (px.x-mx.x) + (py.y-my.y);
        double cd = D/(p.Ms*p.a);
        bx += cd*(px.z-mx.z);
        by += cd*(py.z-my.z);
        bz += -cd*S;

        // interlayer: -(Aint/(Ms*d)) * m_outra    <<< SL-2, o fator 1/d
        double ci = -p.Aint/(p.Ms*p.d);
        double3 ov = o[c];
        bx += ci*ov.x;  by += ci*ov.y;  bz += ci*ov.z;

        double3 r = make_double3(bx,by,bz);
        if(L) b1[c]=r; else b0[c]=r;
    }
}


// ---------------------------- LLG (MISSION-E001) -----------------------------
// dm/dt = -(gamma/(1+alpha^2)) { m x B + alpha m x (m x B) }
// Nota registrada (MISSION-E001 §3.1): com alpha=0 o denominador vale 1, logo a
// escada EV-1/EV-2 NAO consegue testar se ele foi implementado. Fica aqui explicito.
__global__ void k_llg(const double3* m0, const double3* m1,
                      const double3* b0, const double3* b1,
                      double3* k0, double3* k1,
                      double alpha, int n, double pref, double fscale)
{
    int c = blockIdx.x*blockDim.x + threadIdx.x;
    if(c >= n) return;
    // pref/fscale escolhem a formulacao:
    //   FISICA:      pref=GAMMA_T, fscale=1        -> B em tesla,  passo em segundos
    //   ADIMENSIONAL: pref=1,      fscale=1/B0     -> H=B/B0,      passo em tau
    // com B0 = 2*Aex/(Ms*a0^2) e t0 = 1/(gamma*B0) = Ms*a0^2/(2*Aex*gamma).
    double pre = -pref/(1.0+alpha*alpha);
    for(int L=0; L<2; ++L){
        const double3* m = L? m1 : m0;
        const double3* b = L? b1 : b0;
        double3*       k = L? k1 : k0;
        double3 u=m[c], f=b[c];
        f.x*=fscale; f.y*=fscale; f.z*=fscale;
        // m x B
        double cx = u.y*f.z - u.z*f.y;
        double cy = u.z*f.x - u.x*f.z;
        double cz = u.x*f.y - u.y*f.x;
        // m x (m x B)
        double dx = u.y*cz - u.z*cy;
        double dy = u.z*cx - u.x*cz;
        double dz = u.x*cy - u.y*cx;
        k[c] = make_double3(pre*(cx+alpha*dx), pre*(cy+alpha*dy), pre*(cz+alpha*dz));
    }
}

// m_out = m_base + h*k
__global__ void k_axpy(const double3* mb0, const double3* mb1,
                       const double3* k0, const double3* k1,
                       double3* o0, double3* o1, double h, int n)
{
    int c = blockIdx.x*blockDim.x + threadIdx.x;
    if(c >= n) return;
    o0[c] = make_double3(mb0[c].x+h*k0[c].x, mb0[c].y+h*k0[c].y, mb0[c].z+h*k0[c].z);
    o1[c] = make_double3(mb1[c].x+h*k1[c].x, mb1[c].y+h*k1[c].y, mb1[c].z+h*k1[c].z);
}

// combinacao RK4 final
__global__ void k_rk4(double3* m0, double3* m1,
                      const double3* a0,const double3* a1,const double3* b0,const double3* b1,
                      const double3* c0,const double3* c1,const double3* d0,const double3* d1,
                      double dt, int n, int renorm)
{
    int c = blockIdx.x*blockDim.x + threadIdx.x;
    if(c >= n) return;
    double s = dt/6.0;
    for(int L=0; L<2; ++L){
        double3* m = L? m1 : m0;
        const double3* ka = L? a1:a0; const double3* kb = L? b1:b0;
        const double3* kc = L? c1:c0; const double3* kd = L? d1:d0;
        double3 v = m[c];
        v.x += s*(ka[c].x + 2.0*kb[c].x + 2.0*kc[c].x + kd[c].x);
        v.y += s*(ka[c].y + 2.0*kb[c].y + 2.0*kc[c].y + kd[c].y);
        v.z += s*(ka[c].z + 2.0*kb[c].z + 2.0*kc[c].z + kd[c].z);
        if(renorm){ double nn=sqrt(v.x*v.x+v.y*v.y+v.z*v.z); v.x/=nn; v.y/=nn; v.z/=nn; }
        m[c]=v;
    }
}

// ---------------------- passo de relaxacao (damping-only) ---------------------
// dm/dt propto -m x (m x Beff) = Beff - (m.Beff) m  = descida mais ingreme.
// T=0 e so o ponto fixo importa; a trajetoria nao e' evidencia aqui (SL-5).
__global__ void k_step(double3* m0, double3* m1, const double3* b0, const double3* b1,
                       double dt, int nx, int ny)
{
    int c = blockIdx.x*blockDim.x + threadIdx.x;
    if(c >= nx*ny) return;
    for(int L=0; L<2; ++L){
        double3* m = L? m1 : m0;
        const double3* b = L? b1 : b0;
        double3 u=m[c], f=b[c];
        double mb = u.x*f.x+u.y*f.y+u.z*f.z;
        double px = f.x-mb*u.x, py = f.y-mb*u.y, pz = f.z-mb*u.z;   // Beff perpendicular
        double vx = u.x+dt*px, vy = u.y+dt*py, vz = u.z+dt*pz;
        double s = rsqrt(vx*vx+vy*vy+vz*vz);
        m[c] = make_double3(vx*s, vy*s, vz*s);
    }
}

// torque maximo |m x Beff|, para criterio de parada
__global__ void k_torque(const double3* m0,const double3* m1,
                         const double3* b0,const double3* b1,double* out,int nx,int ny)
{
    int c = blockIdx.x*blockDim.x + threadIdx.x;
    if(c >= nx*ny) return;
    double best=0.0;
    for(int L=0; L<2; ++L){
        double3 u = L? m1[c]:m0[c];
        double3 f = L? b1[c]:b0[c];
        double tx=u.y*f.z-u.z*f.y, ty=u.z*f.x-u.x*f.z, tz=u.x*f.y-u.y*f.x;
        double t=sqrt(tx*tx+ty*ty+tz*tz);
        if(t>best) best=t;
    }
    out[c]=best;
}

// --------------------------------- host --------------------------------------
struct Sim {
    Par p; int n;
    double3 *dm0,*dm1,*db0,*db1; double* dscr;
    std::vector<double3> h0,h1;

    void init(Par pp){
        p=pp; n=p.nx*p.ny;
        CK(cudaMalloc(&dm0,n*sizeof(double3))); CK(cudaMalloc(&dm1,n*sizeof(double3)));
        CK(cudaMalloc(&db0,n*sizeof(double3))); CK(cudaMalloc(&db1,n*sizeof(double3)));
        CK(cudaMalloc(&dscr,n*sizeof(double)));
        h0.resize(n); h1.resize(n);
    }
    void push(){ CK(cudaMemcpy(dm0,h0.data(),n*sizeof(double3),cudaMemcpyHostToDevice));
                 CK(cudaMemcpy(dm1,h1.data(),n*sizeof(double3),cudaMemcpyHostToDevice)); }
    void pull(){ CK(cudaMemcpy(h0.data(),dm0,n*sizeof(double3),cudaMemcpyDeviceToHost));
                 CK(cudaMemcpy(h1.data(),dm1,n*sizeof(double3),cudaMemcpyDeviceToHost)); }

    double energy(){
        int B=256,G=(n+B-1)/B;
        k_energy<<<G,B>>>(dm0,dm1,dscr,p); CK(cudaGetLastError());
        std::vector<double> h(n); CK(cudaMemcpy(h.data(),dscr,n*sizeof(double),cudaMemcpyDeviceToHost));
        // soma de Kahan: a energia total e' uma diferenca de termos grandes
        double s=0.0,cc=0.0;
        for(int i=0;i<n;i++){ double y=h[i]-cc, t=s+y; cc=(t-s)-y; s=t; }
        return s;
    }
    void field(){ int B=256,G=(n+B-1)/B; k_field<<<G,B>>>(dm0,dm1,db0,db1,p); CK(cudaGetLastError()); }
    double torque(){
        int B=256,G=(n+B-1)/B;
        k_torque<<<G,B>>>(dm0,dm1,db0,db1,dscr,n>0?p.nx:0,p.ny); CK(cudaGetLastError());
        std::vector<double> h(n); CK(cudaMemcpy(h.data(),dscr,n*sizeof(double),cudaMemcpyDeviceToHost));
        double b=0; for(double v:h) if(v>b) b=v; return b;
    }
};

static double frand(){ return 2.0*drand48()-1.0; }
static double3 rndunit(){
    double x,y,z,r;
    do{ x=frand(); y=frand(); z=frand(); r=sqrt(x*x+y*y+z*z);}while(r<1e-6);
    return make_double3(x/r,y/r,z/r);
}

// ------------------- carga topologica de rede (Berg-Luscher) ------------------
// A densidade por diferencas finitas subestima |Q| em skyrmions compactos (medido:
// |Q|=0.984 numa relaxacao limpa). Berg-Luscher usa o angulo solido de cada
// triangulo de spins e soma EXATAMENTE um inteiro na rede. A troca de estimador e'
// justificada por um criterio (Q inteiro) independente do alvo de 10.98 nm.
//
//   tan(Omega/2) = m1.(m2 x m3) / (1 + m1.m2 + m2.m3 + m3.m1)
//
// Retorna a carga POR PLAQUETA (adimensional) e a posicao do centro da plaqueta.
static inline double tri_charge(const double3&A,const double3&B,const double3&C)
{
    double num = A.x*(B.y*C.z-B.z*C.y) + A.y*(B.z*C.x-B.x*C.z) + A.z*(B.x*C.y-B.y*C.x);
    double den = 1.0 + (A.x*B.x+A.y*B.y+A.z*B.z)
                     + (B.x*C.x+B.y*C.y+B.z*C.z)
                     + (C.x*A.x+C.y*A.y+C.z*A.z);
    return 2.0*atan2(num,den);
}

static void charge_density(const std::vector<double3>& m, const Par& p, std::vector<double>& q)
{
    q.assign(p.nx*p.ny, 0.0);
    const double inv = 1.0/(4.0*M_PI);
    for(int j=0;j<p.ny;j++) for(int i=0;i<p.nx;i++){
        double3 s00=m[idx(i  ,j  ,p.nx,p.ny)];
        double3 s10=m[idx(i+1,j  ,p.nx,p.ny)];
        double3 s11=m[idx(i+1,j+1,p.nx,p.ny)];
        double3 s01=m[idx(i  ,j+1,p.nx,p.ny)];
        // plaqueta (i,j) dividida em dois triangulos; carga guardada em (i,j),
        // cujo centro geometrico fica em ((i+1)a, (j+1)a).
        q[idx(i,j,p.nx,p.ny)] = inv*( tri_charge(s00,s10,s11) + tri_charge(s00,s11,s01) );
    }
}

// diferenca de imagem minima em um toro
static inline double mi(double v, double L){ while(v> L/2) v-=L; while(v<-L/2) v+=L; return v; }

// CTC (Eq. 1) robusta a PBC: desdobra em torno do pico de |rho| e faz a media
// ponderada por rho ali; sem isso, \int r*rho num toro e' mal definida (SL-4).
struct CTC { double x,y,Q; bool ok; };
static CTC ctc(const std::vector<double3>& m, const Par& p)
{
    std::vector<double> q; charge_density(m,p,q);
    double Lx=p.nx*p.a, Ly=p.ny*p.a;
    int pk=0; double bv=0;
    for(int c=0;c<p.nx*p.ny;c++) if(fabs(q[c])>bv){ bv=fabs(q[c]); pk=c; }
    double px=(pk%p.nx+1.0)*p.a, py=(pk/p.nx+1.0)*p.a;

    double Q=0, sx=0, sy=0;
    for(int j=0;j<p.ny;j++) for(int i=0;i<p.nx;i++){
        double w = q[idx(i,j,p.nx,p.ny)];              // ja e' carga, nao densidade
        double dx = mi((i+1.0)*p.a - px, Lx);
        double dy = mi((j+1.0)*p.a - py, Ly);
        Q += w; sx += w*dx; sy += w*dy;
    }
    CTC r; r.Q=Q; r.ok = fabs(Q)>1e-3;
    r.x = r.ok? px + sx/Q : px;
    r.y = r.ok? py + sy/Q : py;
    return r;
}

static double bond_length(const std::vector<double3>& m0, const std::vector<double3>& m1,
                          const Par& p, CTC& c0, CTC& c1)
{
    c0 = ctc(m0,p); c1 = ctc(m1,p);
    double Lx=p.nx*p.a, Ly=p.ny*p.a;
    double dx = mi(c0.x-c1.x, Lx), dy = mi(c0.y-c1.y, Ly);
    return sqrt(dx*dx+dy*dy);
}

// --------------------------- ansatz de parede de 360 -------------------------
// theta(r) = 2 atan2( sinh(R/w), sinh(r/w) ) : theta(0)=pi, theta(inf)=0.
// phi = gamma + phi0. phi0 e' escolhido pelo SINAL DE D DA PROPRIA CAMADA (SL-6),
// por energia DMI do ansatz — nao por gosto.
static double dmi_energy(const std::vector<double3>& m, double D, const Par& p)
{
    double e=0;
    for(int j=0;j<p.ny;j++) for(int i=0;i<p.nx;i++){
        double3 c0=m[idx(i,j,p.nx,p.ny)];
        double3 px=m[idx(i+1,j,p.nx,p.ny)], mx=m[idx(i-1,j,p.nx,p.ny)];
        double3 py=m[idx(i,j+1,p.nx,p.ny)], my=m[idx(i,j-1,p.nx,p.ny)];
        double S=(px.x-mx.x)+(py.y-my.y);
        e += (p.d*p.a*D*0.5)*( c0.z*S - c0.x*(px.z-mx.z) - c0.y*(py.z-my.z) );
    }
    return e;
}

static void put_skyrmion(std::vector<double3>& m, const Par& p,
                         double cx,double cy,double R,double w,double phi0,int bg)
{
    // bg = +1 : fundo mz=+1, nucleo mz=-1.   bg = -1 : espelhado.
    double Lx=p.nx*p.a, Ly=p.ny*p.a;
    for(int j=0;j<p.ny;j++) for(int i=0;i<p.nx;i++){
        double x=mi((i+0.5)*p.a-cx,Lx), y=mi((j+0.5)*p.a-cy,Ly);
        double r=sqrt(x*x+y*y);
        double th = 2.0*atan2( sinh(R/w), sinh(std::max(r,1e-12)/w) );
        double g  = atan2(y,x) + phi0;
        m[idx(i,j,p.nx,p.ny)] = make_double3( sin(th)*cos(g), sin(th)*sin(g), bg*cos(th) );
    }
}

// escolhe phi0 in {0,pi} minimizando a energia DMI do proprio ansatz
static double pick_chirality(std::vector<double3>& m, const Par& p,
                             double cx,double cy,double R,double w,int bg,double D,
                             double* e0out,double* e1out)
{
    std::vector<double> cand={0.0, M_PI}; double best=0, bestE=1e300;
    for(size_t k=0;k<cand.size();k++){
        put_skyrmion(m,p,cx,cy,R,w,cand[k],bg);
        double e=dmi_energy(m,D,p);
        if(k==0&&e0out)*e0out=e; if(k==1&&e1out)*e1out=e;
        if(e<bestE){ bestE=e; best=cand[k]; }
    }
    put_skyrmion(m,p,cx,cy,R,w,best,bg);
    return best;
}

// ------------------------------ relaxacao ------------------------------------
// Descida mais ingreme com passo adaptativo. A energia deve decrescer
// monotonicamente; se subir, o bloco e' revertido e dt cai pela metade.
// Um dt que nao para de cair e' sintoma de stencil nao-adjunto, nao de fisica.
struct RelaxOut { double E, torque; int iters; bool converged; };

static RelaxOut relax(Sim& S, double tol, int maxit, int nsub, bool log_l, FILE* lf)
{
    int n=S.n;
    double3 *bk0,*bk1; CK(cudaMalloc(&bk0,n*sizeof(double3))); CK(cudaMalloc(&bk1,n*sizeof(double3)));
    double dt=1e-5, E=S.energy(); int it=0; bool conv=false; double tq=0;

    while(it<maxit){
        CK(cudaMemcpy(bk0,S.dm0,n*sizeof(double3),cudaMemcpyDeviceToDevice));
        CK(cudaMemcpy(bk1,S.dm1,n*sizeof(double3),cudaMemcpyDeviceToDevice));
        int B=256,G=(n+B-1)/B;
        for(int s=0;s<nsub;s++){ S.field(); k_step<<<G,B>>>(S.dm0,S.dm1,S.db0,S.db1,dt,S.p.nx,S.p.ny); }
        CK(cudaGetLastError());
        double E2=S.energy();
        if(!(E2<=E) ){                       // pega tambem NaN
            CK(cudaMemcpy(S.dm0,bk0,n*sizeof(double3),cudaMemcpyDeviceToDevice));
            CK(cudaMemcpy(S.dm1,bk1,n*sizeof(double3),cudaMemcpyDeviceToDevice));
            dt*=0.5;
            if(dt<1e-14) break;
            continue;
        }
        E=E2; it+=nsub; dt=fmin(dt*1.1, 1e-2);
        S.field(); tq=S.torque();
        if(log_l && lf && (it % (nsub*20)==0)){
            S.pull(); CTC a,b; double l=bond_length(S.h0,S.h1,S.p,a,b);
            fprintf(lf,"%d  %.6e  %.6f  %.4f  %.4f\n", it, E, l*1e9, a.Q, b.Q);
            fflush(lf);
        }
        if(tq<tol){ conv=true; break; }
    }
    cudaFree(bk0); cudaFree(bk1);
    RelaxOut r; r.E=E; r.torque=tq; r.iters=it; r.converged=conv; return r;
}

// ================================ VL-1 =======================================
// FD field-vs-energy, termo a termo. Beff = -(1/(Ms d a^2)) dH/dm.
static int vl1(Par base)
{
    printf("\n=== VL-1  FD field-vs-energy (grade 12x10, nao-quadrada de proposito) ===\n");
    Par p=base; p.nx=12; p.ny=10;
    struct T { const char* name; Par p; };
    std::vector<T> tests;
    { Par q=p; q.K=0;q.D1=0;q.D2=0;q.Aint=0;q.Bz=0;            tests.push_back({"troca      ",q}); }
    { Par q=p; q.A=0;q.D1=0;q.D2=0;q.Aint=0;q.Bz=0;            tests.push_back({"anisotropia",q}); }
    { Par q=p; q.A=0;q.K=0;q.Aint=0;q.Bz=0;                    tests.push_back({"DMI        ",q}); }
    { Par q=p; q.A=0;q.K=0;q.D1=0;q.D2=0;q.Bz=0;               tests.push_back({"interlayer ",q}); }
    { Par q=p; q.A=0;q.K=0;q.D1=0;q.D2=0;q.Aint=0;q.Bz=0.35;   tests.push_back({"Zeeman     ",q}); }
    { Par q=p;                                                 tests.push_back({"TUDO JUNTO ",q}); }

    int fails=0;
    for(auto& t : tests){
        Sim S; S.init(t.p); int n=S.n;
        srand48(12345);
        for(int c=0;c<n;c++){ S.h0[c]=rndunit(); S.h1[c]=rndunit(); }
        S.push(); S.field();
        std::vector<double3> B0(n),B1(n);
        CK(cudaMemcpy(B0.data(),S.db0,n*sizeof(double3),cudaMemcpyDeviceToHost));
        CK(cudaMemcpy(B1.data(),S.db1,n*sizeof(double3),cudaMemcpyDeviceToHost));

        double pre = -1.0/(t.p.Ms*t.p.d*t.p.a*t.p.a);
        double eps = 1e-7, worst=0.0, scale=0.0;
        for(int trial=0; trial<40; ++trial){
            int L   = (int)(drand48()*2);
            int c   = (int)(drand48()*n);
            int comp= (int)(drand48()*3);
            std::vector<double3>& H = L? S.h1 : S.h0;
            double* q = (comp==0)? &H[c].x : (comp==1? &H[c].y : &H[c].z);
            double keep=*q;
            *q=keep+eps; S.push(); double Ep=S.energy();
            *q=keep-eps; S.push(); double Em=S.energy();
            *q=keep;     S.push();
            double num = pre*(Ep-Em)/(2*eps);
            double3 b  = L? B1[c] : B0[c];
            double ana = (comp==0)? b.x : (comp==1? b.y : b.z);
            double err = fabs(num-ana);
            if(err>worst) worst=err;
            if(fabs(ana)>scale) scale=fabs(ana);
        }
        double rel = worst/(scale>0?scale:1.0);
        bool ok = rel < 1e-6;
        printf("  %s  pior erro abs %10.3e   escala %10.3e   rel %9.2e   %s\n",
               t.name, worst, scale, rel, ok?"PASSA":"** FALHA **");
        if(!ok) fails++;
        cudaFree(S.dm0);cudaFree(S.dm1);cudaFree(S.db0);cudaFree(S.db1);cudaFree(S.dscr);
    }
    printf("  VL-1: %s\n", fails?"FALHOU":"PASSOU");
    return fails;
}

// ================================ VL-2 =======================================
// Estados uniformes: isola o fator areal / 1-d do termo interlayer (SL-2).
static int vl2(Par base)
{
    printf("\n=== VL-2  estado uniforme, energia interlayer ===\n");
    Par p=base; p.A=0;p.K=0;p.D1=0;p.D2=0;p.Bz=0;    // so o termo interlayer
    Sim S; S.init(p);
    double Area = p.nx*p.ny*p.a*p.a;
    int fails=0;
    struct C { const char* nm; double s; double expect; };
    std::vector<C> cs = {{"m1=+z, m2=+z (paralelo)  ", +1, +p.Aint*Area},
                         {"m1=+z, m2=-z (antipar.)  ", -1, -p.Aint*Area}};
    for(auto& c : cs){
        for(int i=0;i<S.n;i++){ S.h0[i]=make_double3(0,0,1); S.h1[i]=make_double3(0,0,c.s); }
        S.push();
        double E=S.energy();
        double rel=fabs(E-c.expect)/fabs(c.expect);
        bool ok=rel<1e-12;
        printf("  %s  H_int = %+.6e J   esperado %+.6e J   rel %8.1e  %s\n",
               c.nm,E,c.expect,rel, ok?"PASSA":"** FALHA **");
        if(!ok) fails++;
    }
    // e o campo correspondente: |Beff_int| = Aint/(Ms d)
    S.field();
    std::vector<double3> B(S.n);
    CK(cudaMemcpy(B.data(),S.db0,S.n*sizeof(double3),cudaMemcpyDeviceToHost));
    double expect = p.Aint/(p.Ms*p.d);
    double got = fabs(B[0].z);
    bool ok = fabs(got-expect)/expect < 1e-12;
    printf("  |Beff_int| = %.6f T   esperado Aint/(Ms*d) = %.6f T   %s\n",
           got,expect, ok?"PASSA":"** FALHA **");
    if(!ok) fails++;
    printf("  VL-2: %s\n", fails?"FALHOU":"PASSOU");
    return fails;
}

// ================================ VL-3 =======================================
// Skyrmion unico, Aint=0. kappa = D/Dc = 0.80 diz que isto TEM de funcionar.
static int vl3(Par base)
{
    printf("\n=== VL-3  skyrmion unico, Aint=0 ===\n");
    Par p=base; p.Aint=0.0;
    double Dc = 4.0*sqrt(p.A*p.K)/M_PI;
    printf("  Dc = 4*sqrt(A*K)/pi = %.4f mJ/m^2 ;  kappa = D/Dc = %.4f\n",
           Dc*1e3, fabs(p.D1)/Dc);
    Sim S; S.init(p);
    double cx=p.nx*p.a/2, cy=p.ny*p.a/2;
    double e0,e1;
    double phi = pick_chirality(S.h0,p,cx,cy,4e-9,3e-9,+1,p.D1,&e0,&e1);
    printf("  chiralidade escolhida (camada 1, D1=%+.2f mJ/m^2): phi0=%.0f deg"
           "  [E_DMI(0)=%+.3e J, E_DMI(pi)=%+.3e J]\n", p.D1*1e3, phi*180/M_PI, e0,e1);
    for(int i=0;i<S.n;i++) S.h1[i]=make_double3(0,0,-1);   // camada 2 uniforme, desacoplada
    S.push();
    CTC a0=ctc(S.h0,p);
    printf("  Q inicial = %+.4f\n", a0.Q);
    RelaxOut r = relax(S,1e-5,400000,25,false,NULL);
    S.pull();
    CTC a=ctc(S.h0,p);
    double mzmin=1e9; for(auto&v:S.h0) if(v.z<mzmin) mzmin=v.z;
    printf("  relaxado: iters=%d torque=%.3e T  E=%.6e J  convergiu=%s\n",
           r.iters,r.torque,r.E, r.converged?"sim":"NAO");
    printf("  Q final = %+.4f   (alvo |Q|=1)   mz minimo = %+.4f\n", a.Q, mzmin);
    bool ok = fabs(fabs(a.Q)-1.0) < 0.01 && mzmin < -0.9 && r.converged;
    printf("  VL-3: %s\n", ok?"PASSOU":"FALHOU");
    return ok?0:1;
}

// ================================ VL-4 =======================================
// Par acoplado. Registra l(t) ao longo de toda a relaxacao; l->0 identifica
// imediatamente o ramo coaxial (que seria erro de inicializacao, nao refutacao).
static int vl4(Par p, const char* tag, double tol)
{
    printf("\n=== VL-4  par acoplado  [%s]  Aint=%.3f mJ/m^2  K0=%.2f MJ/m^3 ===\n",
           tag, p.Aint*1e3, p.K*1e-6);
    Sim S; S.init(p);
    double cx=p.nx*p.a/2, cy=p.ny*p.a/2, sep=10e-9;
    double e0,e1;
    double f1 = pick_chirality(S.h0,p,cx-sep/2,cy,4e-9,3e-9,+1,p.D1,&e0,&e1);
    printf("  camada 1: D1=%+.2f mJ/m^2  -> phi0=%3.0f deg  [E(0)=%+.3e  E(pi)=%+.3e]\n",
           p.D1*1e3, f1*180/M_PI, e0,e1);
    double f2 = pick_chirality(S.h1,p,cx+sep/2,cy,4e-9,3e-9,-1,p.D2,&e0,&e1);
    printf("  camada 2: D2=%+.2f mJ/m^2  -> phi0=%3.0f deg  [E(0)=%+.3e  E(pi)=%+.3e]\n",
           p.D2*1e3, f2*180/M_PI, e0,e1);
    S.push();

    CTC a,b; double l0=bond_length(S.h0,S.h1,p,a,b);
    printf("  inicial: l=%.4f nm  Q1=%+.4f  Q2=%+.4f\n", l0*1e9,a.Q,b.Q);

    char fn[512]; snprintf(fn,sizeof fn,"LAB/EVIDENCE/E002/l_of_t_%s.dat",tag);
    FILE* lf=fopen(fn,"w");
    if(lf) fprintf(lf,"# iter  E[J]  l[nm]  Q1  Q2\n");
    RelaxOut r = relax(S,tol,20000000,25,true,lf);
    if(lf) fclose(lf);
    S.pull();
    double l=bond_length(S.h0,S.h1,p,a,b);
    printf("  relaxado: iters=%d torque=%.3e T  E=%.6e J  convergiu=%s\n",
           r.iters,r.torque,r.E, r.converged?"sim":"NAO");
    printf("  ----> l = %.4f nm   Q1=%+.4f  Q2=%+.4f\n", l*1e9, a.Q, b.Q);
    printf("  ----> serie l(t) em %s\n", fn);

    // gravar estado final para evidencia
    char sn[512]; snprintf(sn,sizeof sn,"LAB/EVIDENCE/E002/mfinal_%s.dat",tag);
    FILE* mf=fopen(sn,"w");
    if(mf){ fprintf(mf,"# i j m0x m0y m0z m1x m1y m1z\n");
        for(int j=0;j<p.ny;j++) for(int i=0;i<p.nx;i++){ int c=idx(i,j,p.nx,p.ny);
            fprintf(mf,"%d %d %.8f %.8f %.8f %.8f %.8f %.8f\n",i,j,
              S.h0[c].x,S.h0[c].y,S.h0[c].z, S.h1[c].x,S.h1[c].y,S.h1[c].z); }
        fclose(mf); printf("  ----> estado final em %s\n",sn); }

    // criterio FIXADO EM MISSION-R001.md ANTES desta execucao: [10.43, 11.53] nm
    bool topo   = fabs(fabs(a.Q)-1)<0.05 && fabs(fabs(b.Q)-1)<0.05 && a.Q*b.Q<0;
    bool noncox = l*1e9 > 1.0;
    bool inband = (l*1e9 >= 10.43 && l*1e9 <= 11.53);
    printf("  carga topologica Q1=-Q2, |Q|~1 ...... %s\n", topo?"ok":"FALHOU");
    printf("  ramo nao-coaxial (l nao vai a 0) .... %s\n", noncox?"ok":"FALHOU (ramo coaxial)");
    printf("  l em [10.43, 11.53] nm .............. %s\n", inband?"ok":"FORA DA BANDA");
    return (topo&&noncox&&inband)?0:1;
}


// ================================ R002 =======================================
// Classificacao do desfecho da relaxacao para mapear a regiao de estabilidade.
// SL-B2: um skyrmion EM EXPLOSAO continua com |Q|=1 — a topologia se conserva
// enquanto o dominio cresce. Classificar so por Q rotularia explodido como
// estavel. Por isso (Q, area) conjuntamente. Limiar de area calibrado do estado
// ligado do R001: 1.10% das celulas; usamos 10% (~9x).
static double reversed_area_frac(const std::vector<double3>& m, int bg)
{
    long c=0; for(const auto& v : m) if(bg>0 ? (v.z<0.0) : (v.z>0.0)) c++;
    return double(c)/double(m.size());
}

static int classify(Par p, double tol, int maxit, double sep)
{
    Sim S; S.init(p);
    double cx=p.nx*p.a/2, cy=p.ny*p.a/2;
    double e0,e1;
    pick_chirality(S.h0,p,cx-sep/2,cy,4e-9,3e-9,+1,p.D1,&e0,&e1);
    pick_chirality(S.h1,p,cx+sep/2,cy,4e-9,3e-9,-1,p.D2,&e0,&e1);
    S.push();
    RelaxOut r = relax(S,tol,maxit,25,false,NULL);
    S.pull();
    CTC a,b; double l = bond_length(S.h0,S.h1,p,a,b);
    double A0 = reversed_area_frac(S.h0,+1), A1 = reversed_area_frac(S.h1,-1);
    double Amax = fmax(A0,A1);
    double q0=fabs(a.Q), q1=fabs(b.Q);

    const char* cls;
    if(!r.converged)                            cls="AMBIGUOUS";
    else if(q0<0.5 || q1<0.5)                   cls="COLLAPSE";
    else if(Amax>0.10)                          cls="EXPLODE";
    else if(q0>=0.95&&q0<=1.05&&q1>=0.95&&q1<=1.05)
                                                cls=(l*1e9<1.0)?"COAXIAL":"NONCOAXIAL";
    else                                        cls="AMBIGUOUS";

    // linha unica, parseavel: CSV para o driver
    printf("%.4f,%.4f,%.2f,%s,%.4f,%+.4f,%+.4f,%.4f,%.4f,%d,%.3e\n",
           p.Aint*1e3, p.K*1e-6, sep*1e9, cls, l*1e9, a.Q, b.Q, A0, A1, r.iters, r.torque);
    fflush(stdout);
    return 0;
}

// ================================= main ======================================

// ======================= integrador RK4 (MISSION-E001) =======================
struct Dyn {
    Sim* S; int n;
    double pref=GAMMA_T, fscale=1.0;   // default: formulacao fisica
    double3 *ka0,*ka1,*kb0,*kb1,*kc0,*kc1,*kd0,*kd1,*t0,*t1;
    void init(Sim* s){
        S=s; n=S->n; size_t B=n*sizeof(double3);
        CK(cudaMalloc(&ka0,B)); CK(cudaMalloc(&ka1,B)); CK(cudaMalloc(&kb0,B)); CK(cudaMalloc(&kb1,B));
        CK(cudaMalloc(&kc0,B)); CK(cudaMalloc(&kc1,B)); CK(cudaMalloc(&kd0,B)); CK(cudaMalloc(&kd1,B));
        CK(cudaMalloc(&t0,B));  CK(cudaMalloc(&t1,B));
    }
    // Par de cada estagio vem do chamador (excitacao depende do tempo)
    void stage(const double3* m0,const double3* m1,double3* k0,double3* k1,Par pp,double alpha){
        int B=256,G=(n+B-1)/B;
        k_field<<<G,B>>>(m0,m1,S->db0,S->db1,pp); CK(cudaGetLastError());
        k_llg  <<<G,B>>>(m0,m1,S->db0,S->db1,k0,k1,alpha,n,pref,fscale); CK(cudaGetLastError());
    }
    void step(double dt,double alpha,Par pA,Par pB,Par pC,Par pD,int renorm){
        int B=256,G=(n+B-1)/B;
        stage(S->dm0,S->dm1,ka0,ka1,pA,alpha);
        k_axpy<<<G,B>>>(S->dm0,S->dm1,ka0,ka1,t0,t1,dt*0.5,n);
        stage(t0,t1,kb0,kb1,pB,alpha);
        k_axpy<<<G,B>>>(S->dm0,S->dm1,kb0,kb1,t0,t1,dt*0.5,n);
        stage(t0,t1,kc0,kc1,pC,alpha);
        k_axpy<<<G,B>>>(S->dm0,S->dm1,kc0,kc1,t0,t1,dt,n);
        stage(t0,t1,kd0,kd1,pD,alpha);
        k_rk4<<<G,B>>>(S->dm0,S->dm1,ka0,ka1,kb0,kb1,kc0,kc1,kd0,kd1,dt,n,renorm);
        CK(cudaGetLastError());
    }
};

static inline double sinc_(double x){ if(fabs(x)<1e-15) return 1.0; double y=M_PI*x; return sin(y)/y; }

// excitacao: kind 0 = nenhuma, 1 = ABM (Bz sinc), 2 = SBM (K sinc)
static Par excite(Par base,double t,int kind,double B0,double dKrel,double fc){
    Par q=base;
    if(kind==1) q.Bz = B0*sinc_(fc*t);
    if(kind==2) q.K  = base.K*(1.0 + dKrel*sinc_(fc*t));
    return q;
}

static double maxdev_norm(Sim& S){
    S.pull(); double w=0;
    for(int i=0;i<S.n;i++){
        double3 a=S.h0[i], b=S.h1[i];
        w=fmax(w,fabs(sqrt(a.x*a.x+a.y*a.y+a.z*a.z)-1.0));
        w=fmax(w,fabs(sqrt(b.x*b.x+b.y*b.y+b.z*b.z)-1.0));
    } return w;
}
static void mean_m(Sim& S,double* mz0,double* mz1,double* mx0){
    S.pull(); double a=0,b=0,c=0;
    for(int i=0;i<S.n;i++){ a+=S.h0[i].z; b+=S.h1[i].z; c+=S.h0[i].x; }
    *mz0=a/S.n; *mz1=b/S.n; if(mx0)*mx0=c/S.n;
}

// ============================ EV-1 ===========================================
static int ev1(Par p){
    printf("\n=== EV-1  LLG conservativa (alpha=0, sem excitacao, sem renorm) ===\n");
    Sim S; S.init(p); Dyn D; D.init(&S);
    double cx=p.nx*p.a/2, cy=p.ny*p.a/2, sep=10e-9; double e0,e1;
    pick_chirality(S.h0,p,cx-sep/2,cy,4e-9,3e-9,+1,p.D1,&e0,&e1);
    pick_chirality(S.h1,p,cx+sep/2,cy,4e-9,3e-9,-1,p.D2,&e0,&e1);
    S.push();
    double E0=S.energy(); double dt=10e-15; long steps=(long)llround(1e-9/dt);
    for(long it=0; it<steps; ++it) D.step(dt,0.0,p,p,p,p,0);
    double E1=S.energy(); double dev=maxdev_norm(S);
    double rel=fabs(E1-E0)/fabs(E0);
    printf("  dt=%.1f fs   t=1.0 ns   passos=%ld\n", dt*1e15, steps);
    printf("  E inicial=%.9e J   E final=%.9e J\n", E0,E1);
    printf("  deriva relativa de energia = %.3e   (criterio < 1e-4)\n", rel);
    printf("  max| |m|-1 |               = %.3e   (criterio < 1e-10)\n", dev);
    int ok = (rel<1e-4) && (dev<1e-10);
    printf("  EV-1: %s\n", ok?"PASSOU":"FALHOU");
    return ok?0:1;
}

// ============================ EV-2 ===========================================
static int ev2(Par base,double alpha){
    printf("\n=== EV-2  precessao de Larmor (alvo analitico) ===\n");
    Par p=base; p.A=0;p.K=0;p.D1=0;p.D2=0;p.Aint=0; p.Bz=0.1;
    double falvo = GAMMA_T*p.Bz/(2*M_PI*(1.0+alpha*alpha));
    Sim S; S.init(p); Dyn D; D.init(&S);
    double th=0.1;
    for(int i=0;i<S.n;i++){ S.h0[i]=make_double3(sin(th),0,cos(th)); S.h1[i]=make_double3(sin(th),0,cos(th)); }
    S.push();
    double dt=1e-15; double T=2.0/falvo;  long steps=(long)llround(T/dt);
    char fn2[256]; snprintf(fn2,sizeof fn2,"LAB/EVIDENCE/E002/ev2_precessao_a%.3f.dat",alpha);
    FILE* f=fopen(fn2,"w");
    fprintf(f,"# t[s] mx my mz\n");
    for(long it=0; it<=steps; ++it){
        if(it%50==0){ S.pull(); double3 m=S.h0[0];
            fprintf(f,"%.9e %.12e %.12e %.12e\n", it*dt, m.x,m.y,m.z); }
        if(it<steps) D.step(dt,alpha,p,p,p,p,0);
    }
    fclose(f);
    printf("  B=%.3f T   f_alvo = gamma*B/2pi = %.6f GHz\n", p.Bz, falvo*1e-9);
    printf("  alpha=%.4f   f_alvo com 1/(1+a^2) = %.9f GHz\n", alpha, falvo*1e-9);
    printf("  serie em %s\n", fn2);
    return 0;
}

// ============================ EV-3 ===========================================
static int ev3(Par p,int kind,double ns){
    const char* nm = (kind==2)?"SBM (dK)":"ABM (Bz)";
    printf("\n=== EV-3  espectro de breathing — %s, janela %.1f ns ===\n", nm, ns);
    Sim S; S.init(p); Dyn D; D.init(&S);
    double cx=p.nx*p.a/2, cy=p.ny*p.a/2, sep=10e-9; double e0,e1;
    pick_chirality(S.h0,p,cx-sep/2,cy,4e-9,3e-9,+1,p.D1,&e0,&e1);
    pick_chirality(S.h1,p,cx+sep/2,cy,4e-9,3e-9,-1,p.D2,&e0,&e1);
    S.push();
    RelaxOut r = relax(S,1e-5,600000,25,false,NULL);
    printf("  equilibrio: iters=%d torque=%.3e T convergiu=%s\n", r.iters,r.torque,r.converged?"sim":"NAO");
    double z0,z1,dummy; mean_m(S,&z0,&z1,&dummy);
    printf("  <mz>_eq camada1=%+.9f  camada2=%+.9f\n", z0,z1);

    double alpha=0.02, B0=4e-3, dKrel=0.004, fc=100e9;
    double dt=10e-15, tsamp=2e-12; long steps=(long)llround(ns*1e-9/dt);
    long every=(long)llround(tsamp/dt);
    char fn[256]; snprintf(fn,sizeof fn,"LAB/EVIDENCE/E002/ev3_%s_%.0fns.dat",(kind==2)?"sbm":"abm",ns);
    FILE* f=fopen(fn,"w"); fprintf(f,"# t[s] dmz0 dmz1\n");
    for(long it=0; it<=steps; ++it){
        if(it%every==0){ double a,b; mean_m(S,&a,&b,NULL);
            fprintf(f,"%.9e %.12e %.12e\n", it*dt, a-z0, b-z1); }
        if(it<steps){
            double t=it*dt;
            Par pA=excite(p,t,kind,B0,dKrel,fc);
            Par pB=excite(p,t+dt/2,kind,B0,dKrel,fc);
            Par pD=excite(p,t+dt,kind,B0,dKrel,fc);
            D.step(dt,alpha,pA,pB,pB,pD,1);
        }
    }
    fclose(f);
    printf("  alpha=%.3f B0=%.1f mT dK/K0=%.3f fc=%.0f GHz  amostragem %.0f ps\n",
           alpha,B0*1e3,dKrel,fc*1e-9,tsamp*1e12);
    printf("  serie em %s\n", fn);
    return 0;
}


// ================= comparacao FISICA vs ADIMENSIONAL (E001 adendo) ===========
// Equacao adimensional (forma dada por Rodrigo):
//   dS/dtau = -(1/(1+a^2)) [ S x H + a S x (S x H) ],  t = t0*tau
//   t0 = Ms*a0^2/(2*Aex*gamma) = 1/(gamma*B0),  B0 = 2*Aex/(Ms*a0^2)
static int ndcheck(Par p,double alpha){
    double B0 = 2.0*p.A/(p.Ms*p.a*p.a);
    double t0 = 1.0/(GAMMA_T*B0);
    printf("\n=== ND-CHECK  fisica vs adimensional  (alpha=%.3f) ===\n",alpha);
    printf("  B0 = 2*Aex/(Ms*a0^2) = %.6f T     t0 = 1/(gamma*B0) = %.6e s = %.4f ps\n",B0,t0,t0*1e12);
    printf("  conferencia gamma*B0*t0 = %.17g   (tem de ser 1)\n", GAMMA_T*B0*t0);

    double dt=10e-15, ttot=0.2e-9; long steps=(long)llround(ttot/dt);
    double dtau = dt/t0;
    printf("  dt = %.1f fs = %.6f t0   |   passos = %ld   |   t_total = %.2f ns\n",
           dt*1e15, dtau, steps, ttot*1e9);

    std::vector<double3> ref0, ref1; double Efis=0,End=0;
    for(int run=0; run<2; ++run){
        Sim S; S.init(p); Dyn D; D.init(&S);
        if(run==1){ D.pref=1.0; D.fscale=1.0/B0; }
        double cx=p.nx*p.a/2, cy=p.ny*p.a/2, sep=10e-9; double e0,e1;
        pick_chirality(S.h0,p,cx-sep/2,cy,4e-9,3e-9,+1,p.D1,&e0,&e1);
        pick_chirality(S.h1,p,cx+sep/2,cy,4e-9,3e-9,-1,p.D2,&e0,&e1);
        S.push();
        double h = (run==0)? dt : dtau;
        for(long it=0; it<steps; ++it) D.step(h,alpha,p,p,p,p,0);
        S.pull();
        if(run==0){ ref0=S.h0; ref1=S.h1; Efis=S.energy(); }
        else{
            End=S.energy();
            double w=0,rms=0; long n=0;
            for(int i=0;i<S.n;i++){
                double3 a=ref0[i],b=S.h0[i];
                double d2=(a.x-b.x)*(a.x-b.x)+(a.y-b.y)*(a.y-b.y)+(a.z-b.z)*(a.z-b.z);
                w=fmax(w,sqrt(d2)); rms+=d2; n++;
                double3 c=ref1[i],e=S.h1[i];
                d2=(c.x-e.x)*(c.x-e.x)+(c.y-e.y)*(c.y-e.y)+(c.z-e.z)*(c.z-e.z);
                w=fmax(w,sqrt(d2)); rms+=d2; n++;
            }
            printf("  E(fisica)      = %.15e J\n", Efis);
            printf("  E(adimensional)= %.15e J\n", End);
            printf("  |dE|/|E|                 = %.3e\n", fabs(End-Efis)/fabs(Efis));
            printf("  max |S_fis - S_nd|       = %.3e\n", w);
            printf("  rms |S_fis - S_nd|       = %.3e\n", sqrt(rms/n));
            printf("  (epsilon de double = %.2e; diferenca so de arredondamento e' ~1e-13)\n", 2.22e-16);
        }
    }
    return 0;
}

// ============================ MISSION-E002 ===================================
// Autopropulsao (Fig. 2 do PRL). Pre-registro em LAB/MISSIONS/MISSION-E002.md.
// Tres coisas novas, todas exigidas pelo pre-registro:
//   1. ctc2()  — CTC com ORIGEM DE DESDOBRAMENTO CONTINUA (E002 §5 PV-1). O ctc()
//      herdado desdobra em torno do argmax de |rho|; conforme o par deriva, essa
//      celula SALTA e muda quais caudas sao reenroladas por L=100 nm. Uma cauda de
//      1e-7 vale ~0.01 pm — a ordem do sinal do ABM (0.05 pm). Corrigido ANTES da
//      primeira corrida de producao, nao depois de ver o ruido.
//   2. dissip() — tensor de dissipacao, Eq. (2). Ms*d/gamma com d = ESPESSURA
//      (0.4 nm), nao a0. Mesma armadilha d-vs-a0 do SL-2 / ADENDUM-003: a escolha
//      errada erra por 2.5x.
//   3. excite_mono() — excitacao monocromatica do texto principal, nao o sinc de
//      banda larga do E001.

// CTC com origem de desdobramento dada pelo chamador (continua no tempo).
static CTC ctc2(const std::vector<double3>& m, const Par& p, double px, double py)
{
    std::vector<double> q; charge_density(m,p,q);
    double Lx=p.nx*p.a, Ly=p.ny*p.a;
    double Q=0, sx=0, sy=0, cq=0, cx=0, cy=0;          // Kahan nos tres
    for(int j=0;j<p.ny;j++) for(int i=0;i<p.nx;i++){
        double w  = q[idx(i,j,p.nx,p.ny)];
        double dx = mi((i+1.0)*p.a - px, Lx);
        double dy = mi((j+1.0)*p.a - py, Ly);
        double y,t;
        y=w    -cq; t=Q +y; cq=(t-Q )-y; Q =t;
        y=w*dx -cx; t=sx+y; cx=(t-sx)-y; sx=t;
        y=w*dy -cy; t=sy+y; cy=(t-sy)-y; sy=t;
    }
    CTC r; r.Q=Q; r.ok = fabs(Q)>1e-3;
    r.x = r.ok? px + sx/Q : px;
    r.y = r.ok? py + sy/Q : py;
    return r;
}

// Tensor de dissipacao, Eq. (2):  [D]_uv = (Ms*d/gamma) * \int d^2r  du m . dv m
// Diferencas centradas em malha periodica. Retorna Dxx,Dyy,Dxy e sqrt(det D).
struct Diss { double xx,yy,xy,det; };
static Diss dissip(const std::vector<double3>& m, const Par& p)
{
    double sxx=0,syy=0,sxy=0, cxx=0,cyy=0,cxy=0;
    const double inv2a = 1.0/(2.0*p.a);
    for(int j=0;j<p.ny;j++) for(int i=0;i<p.nx;i++){
        double3 xp=m[idx(i+1,j,p.nx,p.ny)], xm=m[idx(i-1,j,p.nx,p.ny)];
        double3 yp=m[idx(i,j+1,p.nx,p.ny)], ym=m[idx(i,j-1,p.nx,p.ny)];
        double ax=(xp.x-xm.x)*inv2a, ay=(xp.y-xm.y)*inv2a, az=(xp.z-xm.z)*inv2a;
        double bx=(yp.x-ym.x)*inv2a, by=(yp.y-ym.y)*inv2a, bz=(yp.z-ym.z)*inv2a;
        double vxx=ax*ax+ay*ay+az*az, vyy=bx*bx+by*by+bz*bz, vxy=ax*bx+ay*by+az*bz;
        double y,t;
        y=vxx-cxx; t=sxx+y; cxx=(t-sxx)-y; sxx=t;
        y=vyy-cyy; t=syy+y; cyy=(t-syy)-y; syy=t;
        y=vxy-cxy; t=sxy+y; cxy=(t-sxy)-y; sxy=t;
    }
    const double pre = (p.Ms*p.d/GAMMA_T)*(p.a*p.a);   // \int d^2r -> soma * a^2
    Diss D; D.xx=pre*sxx; D.yy=pre*syy; D.xy=pre*sxy;
    double dt_ = D.xx*D.yy - D.xy*D.xy;
    D.det = (dt_>0)? sqrt(dt_) : 0.0;
    return D;
}

// Excitacao MONOCROMATICA (texto principal): kind 0 = nenhuma, 1 = ABM, 2 = SBM.
static Par excite_mono(Par base,double t,int kind,double B0,double dKrel,double f)
{
    Par q=base; double s=sin(2.0*M_PI*f*t);
    if(kind==1) q.Bz = B0*s;
    if(kind==2) q.K  = base.K*(1.0 + dKrel*s);
    return q;
}

// ---- rastreador de CTC absoluta (desdobrada) --------------------------------
struct Track { double ax,ay, wx,wy; bool started; };
static void track_update(Track& T, const std::vector<double3>& m, const Par& p, CTC& out)
{
    double Lx=p.nx*p.a, Ly=p.ny*p.a;
    if(!T.started){ out = ctc(m,p); T.ax=out.x; T.ay=out.y; T.wx=out.x; T.wy=out.y;
                    T.started=true; return; }
    out = ctc2(m,p,T.wx,T.wy);
    T.ax += out.x - T.wx;  T.ay += out.y - T.wy;      // deslocamento pequeno
    T.wx = out.x - Lx*floor(out.x/Lx);                 // origem sempre na caixa
    T.wy = out.y - Ly*floor(out.y/Ly);
}

// ============================ PV-0 ===========================================
// Unidades e forma do tensor de dissipacao no equilibrio. Nenhuma dinamica.
static int pv0(Par p)
{
    printf("\n=== PV-0  tensor de dissipacao no equilibrio (Eq. 2) ===\n");
    Sim S; S.init(p);
    double cx=p.nx*p.a/2, cy=p.ny*p.a/2, sep=10e-9; double e0,e1;
    pick_chirality(S.h0,p,cx-sep/2,cy,4e-9,3e-9,+1,p.D1,&e0,&e1);
    pick_chirality(S.h1,p,cx+sep/2,cy,4e-9,3e-9,-1,p.D2,&e0,&e1);
    S.push();
    RelaxOut r = relax(S,1e-5,600000,25,false,NULL);
    S.pull();
    CTC c0,c1; double l=bond_length(S.h0,S.h1,p,c0,c1);
    Diss D0=dissip(S.h0,p), D1=dissip(S.h1,p);
    double dm = 0.5*(D0.det+D1.det);
    printf("  equilibrio: iters=%d torque=%.3e T convergiu=%s   l=%.6f nm  Q=%.4f/%.4f\n",
           r.iters,r.torque,r.converged?"sim":"NAO", l*1e9, c0.Q, c1.Q);
    printf("  Ms*d/gamma = %.6e N s/m\n", p.Ms*p.d/GAMMA_T);
    for(int L=0;L<2;L++){ Diss D = L? D1:D0;
        printf("  camada %d: Dxx=%.6e Dyy=%.6e Dxy=%.6e  sqrt(det)=%.6e N s/m\n",
               L+1,D.xx,D.yy,D.xy,D.det); }
    double aniso = fabs(D0.xx-D0.yy)/D0.xx, offd = fabs(D0.xy)/D0.xx;
    printf("\n  1/2(D1+D2) = %.4f e-15 N s/m      criterio [13.5, 16.5]\n", dm*1e15);
    printf("  |Dxx-Dyy|/Dxx = %.4f                criterio < 0.05\n", aniso);
    printf("  |Dxy|/Dxx     = %.4f                criterio < 0.05\n", offd);
    int ok = (dm*1e15>=13.5)&&(dm*1e15<=16.5)&&(aniso<0.05)&&(offd<0.05);
    printf("  PV-0: %s\n", ok?"PASSOU":"FALHOU");
    return ok?0:1;
}

// ============================ producao =======================================
// uso: saf_prop prop <none|sbm|abm> <f_GHz> <ns> [dt_fs] [tag]
static int prop(Par p,int kind,double fGHz,double ns,double dtfs,const char* tag)
{
    const char* nm = (kind==2)?"SBM (dK)":(kind==1)?"ABM (Bz)":"NENHUMA (piso de ruido)";
    printf("\n=== E002  autopropulsao — %s, f=%.4f GHz, janela %.1f ns, dt=%.1f fs ===\n",
           nm,fGHz,ns,dtfs);
    Sim S; S.init(p); Dyn D; D.init(&S);
    double cx=p.nx*p.a/2, cy=p.ny*p.a/2, sep=10e-9; double e0,e1;
    pick_chirality(S.h0,p,cx-sep/2,cy,4e-9,3e-9,+1,p.D1,&e0,&e1);
    pick_chirality(S.h1,p,cx+sep/2,cy,4e-9,3e-9,-1,p.D2,&e0,&e1);
    S.push();
    RelaxOut r = relax(S,1e-6,2000000,25,false,NULL);
    S.pull();
    CTC q0,q1; double leq=bond_length(S.h0,S.h1,p,q0,q1);
    printf("  equilibrio: iters=%d torque=%.3e T convergiu=%s  l_eq=%.6f nm\n",
           r.iters,r.torque,r.converged?"sim":"NAO", leq*1e9);

    const double alpha=0.02, B0=4e-3, dKrel=0.005, f=fGHz*1e9;
    const double dt=dtfs*1e-15, tsamp=2e-12;
    long steps=(long)llround(ns*1e-9/dt), every=(long)llround(tsamp/dt);
    if(every<1) every=1;

    char fn[512]; snprintf(fn,sizeof fn,"LAB/EVIDENCE/E002/prop_%s.dat",tag);
    FILE* fp=fopen(fn,"w");
    fprintf(fp,"# MISSION-E002  %s  f=%.6f GHz  alpha=%.3f  dt=%.1f fs  janela=%.1f ns\n",
            nm,fGHz,alpha,dtfs,ns);
    fprintf(fp,"# B0=%.1f mT  dK/K0=%.4f  l_eq=%.9f nm\n", B0*1e3, dKrel, leq*1e9);
    fprintf(fp,"# t[s] X1[m] Y1[m] X2[m] Y2[m] l[m] Q1 Q2 Ddet1 Ddet2 Dxx1 Dyy1 Dxy1 Dxx2 Dyy2 Dxy2\n");

    Track T0{0,0,0,0,false}, T1{0,0,0,0,false};
    double worst=0;
    for(long it=0; it<=steps; ++it){
        if(it%every==0){
            S.pull();
            CTC c0,c1; track_update(T0,S.h0,p,c0); track_update(T1,S.h1,p,c1);
            double dx=T0.ax-T1.ax, dy=T0.ay-T1.ay;
            Diss A=dissip(S.h0,p), B=dissip(S.h1,p);
            fprintf(fp,"%.9e %.15e %.15e %.15e %.15e %.15e %.6f %.6f "
                       "%.9e %.9e %.9e %.9e %.9e %.9e %.9e %.9e\n",
                    it*dt, T0.ax,T0.ay, T1.ax,T1.ay, sqrt(dx*dx+dy*dy), c0.Q,c1.Q,
                    A.det,B.det, A.xx,A.yy,A.xy, B.xx,B.yy,B.xy);
        }
        if(it%(every*500)==0){ double w=maxdev_norm(S); if(w>worst) worst=w; }
        if(it<steps){
            double t=it*dt;
            Par pA=excite_mono(p,t,       kind,B0,dKrel,f);
            Par pB=excite_mono(p,t+dt/2,  kind,B0,dKrel,f);
            Par pD=excite_mono(p,t+dt,    kind,B0,dKrel,f);
            D.step(dt,alpha,pA,pB,pB,pD,1);
        }
    }
    fclose(fp);
    printf("  max||m|-1| ao longo da corrida = %.3e   (PV-2 exige < 1e-9)\n", worst);
    printf("  serie em %s\n", fn);
    return 0;
}

int main(int argc,char** argv)
{
    std::string mode = (argc>1)? argv[1] : "all";
    double tol   = (argc>2)? atof(argv[2]) : 1e-5;     // tolerancia de torque [T]
    double a_nm  = (argc>3)? atof(argv[3]) : 1.0;      // lado da celula [nm]
    const char* tag = (argc>4)? argv[4] : "weak";

    // MISSION-E002: o defeito de argv do RELEASE-E001 §6.1 reaparece no BANNER se a
    // blindagem vier depois dele — `prop none 18.0 2.0` fazia o cabecalho anunciar
    // "6x6 celulas de 18 nm" enquanto a corrida usava 100x100 (l_eq batia com o
    // valor selado do R001). A corrida estava certa e o cabecalho, errado; um
    // cabecalho errado dentro da evidencia e' o mesmo tipo de dano. Blindar ANTES.
    if(mode.rfind("ev",0)==0 || mode=="ndcheck" || mode=="pv0" || mode=="prop"){
        tol = 1e-5; a_nm = 1.0;
    }

    Par p;
    p.nx=(int)llround(100.0/a_nm); p.ny=p.nx;   // caixa fixa de 100 x 100 nm^2
    p.a  = a_nm*1e-9;
    p.d  = 0.4e-9;        // d1 = d2 = 0.4 nm
    p.A  = 15e-12;        // 15 pJ/m
    p.K  = 0.6e6;         // K0 = 0.6 MJ/m^3  (QA-01: demag absorvido, sem demag)
    p.Ms = 0.58e6;        // 0.58 MA/m
    p.D1 =  3.05e-3;      // D1 = -D2 = 3.05 mJ/m^2
    p.D2 = -3.05e-3;
    p.Aint = 0.02e-3;     // acoplamento fraco
    p.Bz = 0.0;

    if(mode!="classify"){
    printf("MISSION-R001/R002 — PRL 135, 086701 (2025)\n");
    printf("grade %dx%d celulas de %.1f nm, PBC | d=%.1f nm A=%.0f pJ/m K=%.2f MJ/m^3 "
           "Ms=%.2f MA/m D=%.2f mJ/m^2 Aint=%.3f mJ/m^2 B=%.1f T\n",
           p.nx,p.ny,p.a*1e9,p.d*1e9,p.A*1e12,p.K*1e-6,p.Ms*1e-6,p.D1*1e3,p.Aint*1e3,p.Bz);
    printf("Beff = -(1/(Ms*d*a^2)) dH/dm   |   Aint/(Ms*d) = %.4f T   | tol_torque=%.1e T\n",
           p.Aint/(p.Ms*p.d), tol); }

    if(mode=="classify"){
        // uso: saf classify <Aint_mJm2> <K0_MJm3> [a_nm]
        double Aint_in = (argc>2)? atof(argv[2]) : 0.02;
        double K0_in   = (argc>3)? atof(argv[3]) : 0.60;
        double an      = (argc>4)? atof(argv[4]) : 1.0;
        double tl      = (argc>5)? atof(argv[5]) : 1e-5;
        int    mi_     = (argc>6)? atoi(argv[6]) : 600000;
        double sp      = (argc>7)? atof(argv[7]) : 10.0;   // separacao inicial [nm]
        p.Aint = Aint_in*1e-3;  p.K = K0_in*1e6;
        p.nx=(int)llround(100.0/an); p.ny=p.nx; p.a=an*1e-9;
        return classify(p, tl, mi_, sp*1e-9);
    }

    // argv[2..3] pertencem aos modos ev*; o parsing generico do topo os leu como
    // tol e a_nm. Blindar TODOS os despachos ev*, nao so o ev3 (defeito registrado
    // em RELEASE-E001 §6.1 estava corrigido apenas no ev3).
    if(mode.rfind("ev",0)==0 || mode=="ndcheck"){ p.a=1e-9; p.nx=100; p.ny=100; }
    // MISSION-E002: mesmos cuidados de argv do defeito registrado em RELEASE-E001 §6.1
    if(mode=="pv0" || mode=="prop"){ p.a=1e-9; p.nx=100; p.ny=100; }
    if(mode=="pv0") return pv0(p);
    if(mode=="prop"){
        std::string k = (argc>2)? argv[2] : "none";
        int kind = (k=="sbm")?2 : (k=="abm")?1 : 0;
        double fGHz = (argc>3)? atof(argv[3]) : 18.0;
        double ns   = (argc>4)? atof(argv[4]) : 200.0;
        double dtfs = (argc>5)? atof(argv[5]) : 10.0;
        const char* tg = (argc>6)? argv[6] : k.c_str();
        return prop(p,kind,fGHz,ns,dtfs,tg);
    }
    if(mode=="ndcheck"){ double al=(argc>2)? atof(argv[2]) : 0.02; return ndcheck(p,al); }
    if(mode=="ev1") return ev1(p);
    if(mode=="ev2"){ double al=(argc>2)? atof(argv[2]) : 0.0; return ev2(p,al); }
    if(mode=="ev3"){ int kind=(argc>2 && std::string(argv[2])=="sbm")?2:1;
                     double ns=(argc>3)? atof(argv[3]) : 2.0;
                     return ev3(p,kind,ns); }

    int bad=0;
    if(mode=="fd"     || mode=="all") bad += vl1(p);
    if(mode=="uniform"|| mode=="all") bad += vl2(p);
    if(mode=="single" || mode=="all") { if(bad){printf("\nescada interrompida: VL-1/VL-2 falharam.\n"); return 1;} bad += vl3(p); }
    if(mode=="pair"   || mode=="all") { if(bad){printf("\nescada interrompida: VL anterior falhou.\n"); return 1;} bad += vl4(p,tag,tol); }

    printf("\n%s\n", bad? "RESULTADO: escada NAO passou inteira." : "RESULTADO: escada completa passou.");
    return bad?1:0;
}
