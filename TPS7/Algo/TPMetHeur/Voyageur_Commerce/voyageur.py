import random
import time
import sys
from math import *



def lectF(path):
    file = open(path,"r")
    ligne = file.read()
    split=ligne.split('\n')
    data = []
    for i in range(0,len(split)) :
        if i == 0:
            data.append(int((split[0].split('\t'))[0]))
        else:
            tmp=split[i].split('\t')
            pos = [int(tmp[1]),int(tmp[2])]
            data.append(pos)
    return data


def solIni(data):
    size = data[0]
    sol = []
    for i in range(1,size+1):
        sol.append(i)
    for i in range(size-1):
        solId = random.randint(0,size-1)
        tmp = sol[i]
        sol[i] = sol[solId]
        sol[solId] = tmp
    return sol



def distSol (data,sol):
    dist = 0
    lastPos = [0,0]
    for i in range(0,data[0]):
        dist+= sqrt((lastPos[0] - data[sol[i]][0])**2 + (lastPos[1] - data[sol[i]][1])**2)
        lastPos[0] = data[sol[i]][0]
        lastPos[1] = data[sol[i]][1]
    dist+= sqrt((lastPos[0])**2 + (lastPos[1])**2)
    return dist



def meilleurVoisin(data, sol):
    sol2 = sol
    mV = sol
    tmp = mV[0]
    mV[0] = mV[1]
    mV[1] = tmp
    for i in range(data[0]):
        for j in range(data[0]):
            if (j != i):
                tmp = sol2[i]
                sol2[i] = sol2[j]
                sol2[j] = tmp
                if(distSol(data, sol2) < distSol(data,mV)):
                    mV = sol2.copy()
                tmp = sol2[i]
                sol2[i] = sol2[j]
                sol2[j] = tmp
    return(mV)



def SteepestHillClimbing(data,x):
    MAX_Depl=100
    sol=x
    nbDepl=0
    Stop=0
    while((nbDepl<MAX_Depl) and not (Stop)):
        s2=meilleurVoisin(data,sol)
        if (distSol(data,s2)<distSol(data,sol)):
            sol = s2.copy()
        else:
            Stop=1
        nbDepl+=1
    return(sol, nbDepl)

def SHCVar (data):
    rep=solIni(data)
    nbEssais=0
    MAX_Essais=10
    sol=rep
    while(nbEssais<MAX_Essais):
        print("Etape ", nbEssais)
        print("solution tirée au hasard: ", sol)
        tmp, nbDepl = SteepestHillClimbing(data,sol)
        print("solution trouvée: ", tmp)
        print("en ", nbDepl, " deplacements")
        if(distSol(data,tmp)<distSol(data,rep)):
            rep=tmp.copy()
        sol=solIni(data).copy()
        nbEssais+=1
    return(rep)



def nonTabu(X,Tabu):
    res = True
    for i in Tabu:
        if X == i:
            res = False
    return res
        
def bestNonTabuNeigh (data, sol, Tabu):
    sol2 = sol
    mV = sol
    tmp = mV[0]
    mV[0] = mV[1]
    mV[1] = tmp
    for i in range(data[0]):
        for j in range(data[0]):
            if (j != i):
                tmp = sol2[i]
                sol2[i] = sol2[j]
                sol2[j] = tmp
                if((distSol(data, sol2) < distSol(data,mV))and(nonTabu(sol2,Tabu))):
                    mV = sol2.copy()
                tmp = sol2[i]
                sol2[i] = sol2[j]
                sol2[j] = tmp
    return mV

def nbVoisinsNonTabu(sol,Tabu):
    res = 0
    sl = sol
    for i in range(len(sol)):
        for j in range(len(sol)):
            if (j != i):
                tmp = sl[i]
                sl[i] = sl[j]
                sl[j] = tmp
                if (nonTabu(sl,Tabu)):
                    res += 1
                tmp = sl[i]
                sl[i] = sl[j]
                sl[j] = tmp
    return res
                
def TabuSearch (data,sol):
    s = sol
    print("solution initiale: ", s)
    Tabu = [[],[]]
    idT = 0
    nbMoves = 0
    bestSoFar = s
    Stop = False
    while nbMoves < 10 and Stop == False:
        if nbVoisinsNonTabu(sol,Tabu) == 0:
            Stop = True
        else:
            Tabu[idT] = s
            idT+=1
            if (idT == len(Tabu)):
                idT = 0
            s = bestNonTabuNeigh(data,s,Tabu)
            if (distSol(data,s)<distSol(data,bestSoFar)):
                bestSoFar = s
            nbMoves += 1
    print("solution atteinte: ", bestSoFar)
    print("Tabou à la fin: ", Tabu)
    return bestSoFar


path = sys.argv[1]

data = lectF(path)
sol = solIni(data)
dist = distSol(data,sol)
deb = time.time()
steep = SHCVar(data)
fin = time.time()
print("SHC en: ", fin-deb, " secondes")
deb = time.time()
tb = TabuSearch(data,sol)
fin = time.time()
print("Tabou en: ", fin-deb, " secondes")

print("Solution initiale: ", sol)
print("distance solution: ", dist)
print("solution trouvée avec Steepest Hill Cling: ", steep)
print("distance SHC: ", distSol(data,steep))
print("solution trouvée avec Tabou Search: ", tb)
print("distance Tabou: ", distSol(data,tb))