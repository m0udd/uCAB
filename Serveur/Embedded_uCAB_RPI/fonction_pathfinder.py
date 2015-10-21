__author__ = 'skwiner'

import json
from math import sqrt

def cabineplusproche(coordX,coordY,map,numArea):

    #en fonction d'un point donnee (d'apres un clic), on cherche le sommet le plus proche

    sommets=[]
    #on recupere les sommets+coordonnes
    for verticle in map[0]['areas'][numArea]['map']['vertices']:
        sommets.append([verticle['name'],verticle['x'],verticle['y']])

    sommet_plus_proche=sommets[0]
    distance_cabine_plus_proche=9999999999
    #on cherche maintenant le sommet le plus proche
    for sommet in sommets:
        xsommet=sommet[1]
        ysommet=sommet[2]
        dist_calcule=sqrt((coordX-xsommet)**2+(coordY-ysommet)**2)
        if dist_calcule<distance_cabine_plus_proche:
            sommet_plus_proche=sommet
            distance_cabine_plus_proche=dist_calcule

    return sommet_plus_proche[0]

def affiche_peres(pere,depart,extremite,trajet):

    if extremite == depart:
        return [depart] + trajet
    else:
        return (affiche_peres(pere, depart, pere[extremite], [extremite] + trajet))

def plus_court(graphe,etape,fin,visites,dist,pere,depart):

    # si on arrive a la fin, on affiche la distance et les peres
    if etape == fin:
       return dist[fin], affiche_peres(pere,depart,fin,[])
    # si c'est la premiere visite, c'est que l'etape actuelle est le depart : on met dist[etape] a 0
    if  len(visites) == 0 : dist[etape]=0
    # on commence a tester les voisins non visites
    for voisin in graphe[etape]:
        if voisin not in visites:
            # la distance est soit la distance calculee precedemment soit l'infini
            dist_voisin = dist.get(voisin,float('inf'))
            # on calcule la nouvelle distance calculee en passant par l'etape
            candidat_dist = dist[etape] + graphe[etape][voisin]
            # on effectue les changements si cela donne un chemin plus court
            if candidat_dist < dist_voisin:
                dist[voisin] = candidat_dist
                pere[voisin] = etape
    # on a regarde tous les voisins : le noeud entier est visite
    visites.append(etape)
    # on cherche le sommet non visite le plus proche du depart
    non_visites = dict((s, dist.get(s,float('inf'))) for s in graphe if s not in visites)
    noeud_plus_proche = min(non_visites, key = non_visites.get)
    # on applique recursivement en prenant comme nouvelle etape le sommet le plus proche
    return plus_court(graphe,noeud_plus_proche,fin,visites,dist,pere,depart)

def dij_rec(graphe,debut,fin):
    return plus_court(graphe,debut,fin,[],{},{},debut)

def distance_entre_deux_pts(map,p1,numareap1,p2):
    index_vertice=0
    index=0
    xp1=0.0
    xp2=0.0
    yp1=0.0
    yp2=0.0
    indexp1=0
    indexp2=0

    """coordonne premier points"""
    for vertice in map[0]['areas'][numareap1]['map']['vertices']:
        if  map[0]['areas'][numareap1]['map']['vertices'][index]['name']==p1:
            indexp1=index
        index=index+1

    indexp1
    xp1 += map[0]['areas'][numareap1]['map']['vertices'][indexp1]['x']
    yp1 += map[0]['areas'][numareap1]['map']['vertices'][indexp1]['y']
    #print p1
    #print "xp1 = "+str(xp1)
    #print "yp1 = "+str(yp1)

    index_vertice=0
    index=0

    """coordonne deuxieme points"""
    for vertice in map[0]['areas'][numareap1]['map']['vertices']:
        if  map[0]['areas'][numareap1]['map']['vertices'][index]['name']==p2:
            indexp2=index
        index=index+1

    indexp2
    xp2 += map[0]['areas'][numareap1]['map']['vertices'][indexp2]['x']
    yp2 += map[0]['areas'][numareap1]['map']['vertices'][indexp2]['y']
    #print p2
    #print "xp2 = "+str(xp2)
    #print "yp2 = "+str(yp2)

    return sqrt((xp2-xp1)**2+(yp2-yp1)**2)

def pluscourchemin(depart,arrive,map):
    """fonction pour gerers le parcours de graphe"""

    """on recupere les aretes et les sommets"""
    aretes = []
    sommets = []

    #on recupere les sommets
    for verticle in map[0]['areas'][0]['map']['vertices']:
        sommets.append(verticle['name'])

    for verticle in map[0]['areas'][1]['map']['vertices']:
        sommets.append(verticle['name'])

    #on recupere les aretes
    for streets in map[0]['areas'][0]['map']['streets']:
        #on recupere la distance entre les deux points
        distance=distance_entre_deux_pts(map,streets['path'][0],0,streets['path'][1])
        aretes.append([streets['path'][0],streets['path'][1],distance])
        aretes.append([streets['path'][1],streets['path'][0],distance])

    for streets in map[0]['areas'][1]['map']['streets']:
        distance=distance_entre_deux_pts(map,streets['path'][0],1,streets['path'][1])
        aretes.append([streets['path'][0],streets['path'][1],distance])
        aretes.append([streets['path'][1],streets['path'][0],distance])

    for bridge in map[0]['areas'][0]['map']['bridges']:
        aretes.append([bridge['from'],bridge['to']['vertex'],bridge['weight']])

    for bridge in map[0]['areas'][1]['map']['bridges']:
        #if aretes.count([bridge['from'],bridge['to']['vertex'],bridge['weight']])<>1 and aretes.count([bridge['from'],bridge['to']['vertex'],bridge['weight']])<>1 :
        aretes.append([bridge['from'],bridge['to']['vertex'],bridge['weight']])

    #impression des sommets
    #print "sommets"
    #print sommets
    #impression des aretes
    #print "aretes"
    #print aretes

    #on vas creer un dico avec les sommets et leurs voisins + distance du voisin
    graphe = dict()
    for sommet in sommets:
        liste_pere = dict()
        for arete in aretes:
            if arete[0]==sommet or arete[1]==sommet:
                if arete[0]==sommet:
                    liste_pere[arete[1]]=arete[2]
                else:
                    liste_pere[arete[0]]=arete[2]
        graphe[sommet]=liste_pere

    #for elem in graphe:
        #print"voisin de : "+str(elem) + " = "+ str(graphe[elem])

    # chemin = [{"name": "m","x": 1,"y": 1},{"name": "b","x": 1,"y": 1}]
    longueur,chemin=dij_rec(graphe,depart,arrive)
    print 'Plus court chemin : ',chemin, ' de longueur :',longueur
    return chemin[1]