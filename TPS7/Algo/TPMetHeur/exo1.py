import random
def creerQ (path):
    file = open(path,"r")
    ligne = file.read()
    n=ligne[0]
    Q=[]
    Ql=[]
    wordbeg=0
    wordend=0
    cpt = 0
    for i in range(4,len(ligne)):
        if
        Ql.append(int(ligne[i]))
        cpt+=1
        if cpt>=6:
            cpt=0
            Q.append(Ql)
           Ql=[]
   return Q

Q=[[-17, 10, 10, 10, 0, 20], [10, -18, 10, 10, 10, 20], [10, 10, -29, 10, 20, 20],[10,10,10,-19,10,10],[0,10,20,10,-17,10],[20,20,20,10,10,-28]]

def f (X,Q):
    sum=0
    for i in range(len(X)):
        for j in range(len(X)):
            sum+=(Q[i][j]*X[i]*X[j])
    return sum

X=[1,1,0,1,0,0]

def solIni (Q):
    X=[]
    n=len(Q)
    for i in range(n):
        X.append(random.randint(0,1))
    return X

def meilleurVoisin(X,Q):
    X2=X
    mV=[1 for i in range(len(X))]
    for i in range(len(X)):
        X2[i]=1-X2[i]
        if (f(X2,Q)<f(mV,Q)):
            mV=X2.copy()
        X2[i]=1-X2[i]
    return mV

def SteepestHillClimbing(X,Q):
    MAX_Depl=100
    sol=X
    nbDepl=0
    Stop=0
    while((nbDepl<MAX_Depl) and not (Stop)):
        s2=meilleurVoisin(sol,Q)
        if (f(s2,Q)<f(sol,Q)):
            sol = s2.copy()
        else:
            Stop=1
        nbDepl+=1
    return(sol)

def SHCVar (X,Q):
    rep=X
    nbEssais=0
    MAX_Essais=10
    sol=X
    while(nbEssais<MAX_Essais):
        tmp = SteepestHillClimbing(sol,Q)
        if(f(tmp,Q)<f(rep,Q)):
            rep=tmp.copy()
        sol=solIni(Q).copy()
        nbEssais+=1
    return(rep)
