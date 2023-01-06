import random
def creerQ (path):
    file = open(path,"r")
    tete = 0
    ligne = file.read()
    split=ligne.split(' ')
    n=int(split[0])
    p = int(split[1])
    Q1 = split[2:len(split)]
    cpt = 0
    Ql = []
    Q = []
    for id in Q1:
        if (cpt < n):
            Ql.append(int(id))
            cpt += 1
        if (cpt == n):
            Q.append(Ql)
            Ql = []
            cpt = 0
    return Q,p


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

def meilleurVoisin(X,Q,p):
    X2=X
    mV=[1 for i in range(len(X))]
    for i in range(len(X)):
        X2[i]=1-X2[i]
        if ((f(X2,Q)<f(mV,Q))and(sum(X2)>=p)):
            mV=X2.copy()
        X2[i]=1-X2[i]
    return mV

def SteepestHillClimbing(X,Q,p):
    MAX_Depl=100
    sol=X
    nbDepl=0
    Stop=0
    while((nbDepl<MAX_Depl) and not (Stop)):
        s2=meilleurVoisin(sol,Q,p)
        if (f(s2,Q)<f(sol,Q)):
            sol = s2.copy()
        else:
            Stop=1
        nbDepl+=1
    return(sol)

def SHCVar (X,Q,p):
    rep=X
    nbEssais=0
    MAX_Essais=10
    sol=X
    while(nbEssais<MAX_Essais):
        tmp = SteepestHillClimbing(sol,Q,p)
        if(f(tmp,Q)<f(rep,Q)):
            rep=tmp.copy()
        sol=solIni(Q).copy()
        nbEssais+=1
    return(rep)
'''
Q6,p6 = creerQ("partition6.txt")
X6 = solIni(Q6)
print("SHC = ", SteepestHillClimbing(X6,Q6,p6))
print("SHCVAR = ", SHCVar(X6,Q6,p6))

QG,pG = creerQ("graphie12345.txt")
XG = solIni(QG)
print("SHC = ", SteepestHillClimbing(XG,QG,pG))
print("SHCVAR = ", SHCVar(XG,QG,pG))
'''
def nonTabu(X,Tabu):
    res = True
    for i in Tabu:
        if X == i:
            res = False
    return res
        
def bestNonTabuNeigh (X,Q,Tabu):
    X2=X
    mV=[1 for i in range(len(X))]
    for i in range(len(X)):
        X2[i]=1-X2[i]
        if (f(X2,Q)<f(mV,Q))and(nonTabu(X2,Tabu)):
            mV=X2.copy()
        X2[i]=1-X2[i]
    return mV

def TabuSearch (X,Q):
    s = X
    Tabu = []
    nbMoves = 0
    bestSoFar = s
    Stop = False
    while nbMoves < 10 and Stop == False:
        if bestNonTabuNeigh(s,Q,Tabu) == [1 for i in range(len(s))]:
            Stop = True
        else:
            Tabu.append(s)
            s = bestNonTabuNeigh(s,Q,Tabu)
            if (f(s,Q)<f(bestSoFar,Q)):
                bestSoFar = s
            nbMoves += 1
    return bestSoFar
