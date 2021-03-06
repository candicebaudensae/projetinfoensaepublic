#projet info v3
#projet de programmation S2 ENSAE

import numpy as np
import matplotlib.pyplot as plt
import random as rd
from math import floor
from math import ceil

##on crée une situation initiale
#situation initiale : on crée une matrice aléatoire d'entiers entre 0 et 2 de taille n ( taille du village )
#0 correspond à un terrain vague
#1 correspond à une habitation
#2 correspond à un agent qui pollue l'eau
#3 correspond à une ferme
#4 correspond à une ressource en eau
#5 correspond à une usine de traitement de l'eau
def situation_initiale(n): #n la taille de la grille
    return(np.random.randint(6, size=(n,n)))

A=situation_initiale(10)

def sourceeau(A):
    E=np.zeros((len(A), len(A)))
    for i in range (len(A)):
        for j in range (len(A)):
            if A[i][j]==4:
                E[i][j]=rd.randint(1000, 3000)
    return(E)

E=sourceeau(A)

def pointsdevie(A):
    n=len(A)
    V=np.zeros((n,n))
    for i in range (n):
        for j in range (n):
            if A[i][j]==1:
                V[i][j]=rd.randint(0, 5)
    return (V)

V=pointsdevie(A)

def besoinseneau(A, E, V):
    e=np.sum(E) #somme des réserves en eau
    b=0 #somme des besoins en eau
    n=len(A)
    B=np.zeros((len(A), len(A))) #matrice de besoin
    for i in range (len(A)):
        for j in range (len(A)):
            if A[i][j]==0:
                B[i][j]=0
            elif A[i][j]==1:
                B[i][j]=V[i][j]*rd.randint(0, int(e/5*(n**2))) #n le nombre de cases
                b=b+B[i][j]
            elif A[i][j]==2:
                B[i][j]=rd.randint(0, int(e/(n**2)))
                b=b+B[i][j]
            elif A[i][j]==3:
                B[i][j]=rd.randint(0, int(e/(n**2)))
                b=b+B[i][j]
    return (B)

B=besoinseneau(A,E,V)

def matricedelapollutiondeleau(A,p1,p2): #matrice du pouvoir polluant des agents
    n=len(A)
    P=np.zeros((n,n))
    for i in range (n):
        for j in range (n):
            if A[i][j]==2:
                P[i][j]=p1*rd.random()
            elif A[i][j]==3:
                P[i][j]=p2*rd.random()
    return(P)
#P va rpz le taux de pollution de l'eau de chaque agent
#on considère qu'au t=0 aucune eau n'est polluée

P=matricedelapollutiondeleau(A, 0.02, 0.1)

def pol(n): #matrice de l'eau polluée
    return np.zeros((n,n))

Pol=pol(10)

##itératif
def distance(x,y):#x et y sont des cases cad des A[i][j] par ex
    a=(x[0]-y[0])**2
    b=(x[1]-y[1])**2
    d=np.sqrt(a+b)
    return(d)
#on calcule la distance euclidienne

#distance([0,2], [5,6]) test ok

def rechercheplusproche(a, Matrice, type, interdits): #marche pour tout
    d=[]
    potentiels=[]
    if len(potentiels)>=0:
        for i in range (len(Matrice)):
            for j in range (len(Matrice)):
                if Matrice[i][j]==type:
                    if [i,j] not in (interdits):
                        potentiels.append([i,j])
                        d.append(distance(a,[i,j]))
        m=min(d)
        rang=d.index(min(d))
        return (potentiels[rang])
    else:
        return (False)

#à retester

def pollutioniterative(E, P, Pol, dmax): #pour passer de t à t+1
    n=len(Pol)
    d=0
    x=0
    for i in range (len(Pol)):
        for j in range (len(Pol)):
            x=rechercheplusproche([i,j],A,4,[])
            if x!=False:
                d=distance(x,[i,j])
                if d<=dmax:
                    Pol[x[0]][x[1]]=Pol[x[0]][x[1]]+P[i][j]*E[x[0]][x[1]]
                    E[x[0]][x[1]]= E[x[0]][x[1]]- P[i][j]*E[x[0]][x[1]]
    return (E, Pol) #E eau disponible, Pol matrice de l'eau polluée

#test E, Pol = pollutioniterative(E, P, Pol, 3) fonctionne

def traitementdeleau(A, E, dmax, traitement):#traitement le nombre de litres d'eau que l'on peut traiter
    n=len(A)
    for i in range (n):
        for j in range (n):
            if A[i][j]==5:#si on est sur une station de traitement de l'eau
                indice=rechercheplusproche([i,j], A, 4, [])
                if indice!=False: #si indice est faux, on n'a pas d'eau donc rien n'est effectué, donc on traite le cas où indice n'est pas faux
                    d=distance([i,j],indice )
                    if d<= dmax: # si on est proche d'une source d'eau
                        E[indice[0]][indice[1]]=E[indice[0]][indice[1]]+traitement#si on est assez proche,la station d'épuration reverse de l'eau dans les sources
    return(E)

#test E= traitementdeleau(A, E, 3, 500) fonctionne ok

def utilisationdeleau(A,B,E,V,Prod, cp): #le programme est trop long
    n=len(A)
    diff=0
    qtemanquante=0
    M=np.zeros((n,n))
    interdits=[]
    for i in range(n):
        for j in range(n):
            if V[i][j]!=0 or A[i][j]==3:#on le fait que pour ceux qui ont encore des points de vie et pour les fermes
                qtemanquante=B[i][j]
                indice=rechercheplusproche([i,j], A, 4, interdits)
                while qtemanquante>0 or indice!=False:
                    indice=rechercheplusproche([i,j], A, 4, interdits)#on regarde les ressources les plus proches
                    if indice==False:
                        A[i][j]=0
                        B[i][j]=0
                        V[i][j]=max([V[i][j]-1, 0])

                    else:
                        diff=E[indice[0]][indice[1]]-B[i][j]
                        if diff>=0:
                            Prod=production(A, E, Prod, cp)
                            E[indice[0]][indice[1]]=diff
                            qtemanquante=0
                        else:
                            qtemanquante=-diff
                            interdits.append([i,j])
                            Prod=production(A, E, Prod, cp)
                            E[indice[0]][indice[1]]= 0 #on enlève combien on a consommé
    return (E,B,V)


def production(A, E, Prod, cp): #production des agriculteurs en fonction de la ressource en eau potable, cp coeff de production, Prod matrice de la production
    n=len(E)
    for i in range (n):
        for j in range (n):
            if A[i][j]==3:
                indice=rechercheplusproche([i,j], A, 4, [])
                if indice!=False:
                    Prod[i][j]=Prod[i][j]+cp*E[indice[0]][indice[1]] #production proportionnelle à la quantité d'eau qu'ils ont
    return (Prod)

#test Prod=production(A,E,Prod,3) fonctionne

##à améliorer car pour l'instant si le fermier proche n'a pas à manger, on ne mange pas, or, on peut aller voir plus loin
def survie(A, E, Prod, consounitaire):
    n=len(A)
    diff=0
    for i in range(n):
        for j in range (n):
            f=rechercheplusproche([i,j], A, 3, [])
            if f!=False:
                diff=Prod[f[0],f[1]]-V[i][j]*consounitaire
                if diff<0:
                    if V[i][j]>=1:
                        V[i][j]=V[i][j]-1
                        Prod[f]=0
                    else:
                        V[i][j]=0
                else :
                    Prod[f[0],f[1]]=Prod[f[0],f[1]] - consounitaire*V[i][j] #on consomme en fonction de ses points de vie ( ou fictivement du nombre de personnes dans le foyer )
    return (V,Prod)

# test V,Prod = survie(A, E, Prod, 2) ok

##programme qui compile
def evolutiontemporelle(n, t, consounitaire, p1, p2, cp, dmax, traitement): # t le temps d'étude, n la taille de la grille
    A=situation_initiale(n)
    E=sourceeau(A)
    V=pointsdevie(A)
    B=besoinseneau(A,E,V)
    e=np.sum(E)
    b=np.sum(B)
    Pol=pol(n)
    P=matricedelapollutiondeleau(A, p1, p2)
    Prod=np.zeros((n,n))
    #evolutiondeE
    #evolutiondeB
    #evolutiondePol
    #evolutiondespointsdevie
    for i in range (t):
        V, Prod=survie(A,E,Prod,consounitaire) #on regarde si on peut nourrir tout le monde et on stocke l'excédent de production
        E, Pol= pollutioniterative(E, P, Pol, dmax)#ce qui pollue l'eau avec le reste des agents pollueurs
        E,B,V=utilisationdeleau(A, B, E, V, Prod, cp) #on répartit l'eau restante
        E=traitementdeleau(A, E, dmax, traitement) # on recrée de l'eau pour le cycle suivant
        #evolutiondeE.append(E)
        #evolutiondeB.append(B)
        #evolutiondePol.append(Pol)
        #evolutiondespointsdevie.append(V)

    return ()

#test
#evolutiontemporelle(5, 1, 1, 0.1, 0.2, 0.5, 2, 10)

##visualisation
#def visualiser(n,t):
    #on pourrait faire une animation de la grille pour voir comment ça évolue de manière interactive
    #https://pyspc.readthedocs.io/fr/latest/05-bases/12-animation.html






##questionnements
#prendre en compte consommation de légumes
#animation
#évolution temporelle faire un programme qui actualise jour par jour
#tester avec plusieurs valeurs
#renouvellement de l'eau ?

##tests
