# coding: utf-8

import argparse
import os
import json
import datetime
import random
import numpy as np
import matplotlib.pyplot as plt

noms_a_enlever = set() # Les noms des utilisateur ne devant pas apparaîtres dans les stats
json_stats = [] # La liste reournée par json.loads
entrees = []
"""
Une entrée présente dans la liste ci-dessus est consituée, dans l'ordre, de :
- l'heure
- le nom complet de l'utilisateur
- le contexte de l'événement
- le composant (HP5, par exemple)
- le nom de l'événement
- une description
- une origine (web, par exemple)
- une ip
"""

def obtenir_noms_a_enlever(fichier : str) -> set :
    """
    Lit le fichier passé en paramètre, si ce dernier existe, et retourne un ensemble, éventuelment vide, de noms.
    Le fichier contient des chaînes de caractères séparées par des retours à la ligne.
    """
    noms_a_enlever = set()
    if os.path.isfile(fichier) :
        with open(fichier) as f : 
            lignes = f.readlines()
            for ligne in lignes :
                if ligne[-1] == '\n' :
                    noms_a_enlever.add(ligne[:-1])
                else :
                    noms_a_enlever.add(ligne)
    else :
        print(f"Le fichier {fichier} n'existe pas.")
    return noms_a_enlever

def num_de_semaine(date: str) -> int:
    """
    Retourne le numéro de la semaine (de 01 à 53) à partir d'une date au format %d %m %y, %H:%M
    Exemple : 4 juin 23, 15:49
    """
    mois_fr = ['janv.', 'févr.', 'mars', 'avril', 'mai', 'juin', 'juil.', 'août', 'sept.', 'oct.', 'nov.', 'déc.']
    mois_en = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']

    chaine_format = '%d %m %y, %H:%M'

    for avant, apres in zip(mois_fr, mois_en):
        date = date.replace(avant, apres)
    
    date = datetime.datetime.strptime(date, chaine_format)
    num = int( date.strftime('%U') )
    return num

def nom_de_famille(nom : str) -> str :
    """Extrait le nom de famille de la chaîne de caractère qui contient prénom et nom"""
    mots = nom.split(" ")
    return " ".join(mots[1:])

def obtenir_valeurs(i : int) -> set :
    """Retourne l'ensemble des valeurs d'indice i (dans chacune des entrées)"""
    valeurs = set()
    for entree in entrees :
        valeur = entree[i]
        valeurs.add(valeur)
    return valeurs

def obtenir_noms():
    """Retourne l'ensemble des noms, privé de l'ensemble des noms à enlever"""
    return obtenir_valeurs(1) - noms_a_enlever

def obtenir_contextes():
    return obtenir_valeurs(5)

def obtenir_histo(nom):
    histo = 53 * [0] # 53 semaines
    for ev in entrees:
        nom_courant = ev[1]
        if nom_courant == nom:
            histo[num_de_semaine(ev[0])] += 1
    return histo

def compter_valeur(valeur : str, nom : str) -> int :
    n_valeur = 0
    for ev in entrees :
        nom_courant = ev[1]
        #print(nom_courant, nom)
        if nom_courant == nom :
            # Permet d'ignorer la valeur et de compter tous les événements
            if valeur == "NULL" :
                n_valeur += 1
            else :
                if valeur in ev :
                    n_valeur += 1
    return n_valeur

def test1():
    histo = 26 * [0]
    with open('oscar.json', 'r') as f:
        stats_json = json.load(f)
        for ev in entrees:
            histo[num_de_semaine(ev[0])] += 1

    print(histo)

    for i, n in enumerate(histo):
        print(f"Semaine {i:2} : {n:3} connexion(s)")

def select_avec(valeurs : list) -> [] :
    """
    L'équivalent du SQL SELECT * FROM entrees WHERE nom="Toto", nom de l'événement = "Badge délivré"
    
    serait

    select_avec(["Toto", "Badge délivré"])
    """
    selection = []
    for entree in entrees :
        selectionne = True
        for valeur in valeurs :
            if not (valeur in entree) :
                selectionne = False
        if selectionne :
            selection.append(entree)
    return selection

def test2():
    noms = set()
    with open('total.json', 'r') as f:
        stats_json = json.load(f)
        for ev in entrees:
            nom = ev[1]
            if not nom in noms:
                #print("Ajout du nom ", nom)
                noms.add(nom)

        elu = random.choice(list(noms))

        print("Nom choisi : ", elu)
        
        for ev in entrees:
            nom = ev[1]
            if nom == elu:
                print([ev[i] for i in [0,1]], num_de_semaine(ev[0]))

def test3():
    with open('total.json', 'r', encoding='utf-8') as f:
        stats_json = json.load(f)
    noms = obtenir_noms(stats_json)
    #print(noms)
    n_connexions = []
    histos = []
    for nom in noms:
        histo = obtenir_histo(stats_json, nom)
        #print(nom, histo)
        histos.append(histo)
        n_connexions.append( (nom, sum(histo)) )
    #print(histos)
    #plt.plot(histos)
    #plt.show()
    with open('n_connexions.csv', 'w') as g:
        for nom, n  in sorted(n_connexions, key=lambda x: x[1]):
            print(nom_de_famille(nom), n, sep=",")
            g.write(f"{nom_de_famille(nom)},{n}\n")
            #print(f"{nom_de_famille(nom)},{n}\n")

def afficher_tableau(valeur : str) :
    noms = obtenir_noms()
    for nom in sorted(noms, key=nom_de_famille) : 
        #print(nom, "nombre de cours consultés :", compter_valeur("Cours consulté", nom))
        print(nom_de_famille(nom), compter_valeur(valeur, nom), sep=',')
               
if __name__ == '__main__':
    analyseur = argparse.ArgumentParser('statistiquesMoodle', 'Extrait des statistiques des journaux Moodle.')
    
    analyseur.add_argument('nom_fichier', help='Le nom du fichier à analyser.')
    analyseur.add_argument('-n', '--noms', action='store_true', help='Renvoie la liste des noms apparaissant dans le journal.')
    analyseur.add_argument('-v', '--valeur', help='Renvoie le tableau du nombre d\'occurences de valeur pour chaque nom.')
    analyseur.add_argument('--contextes', action='store_true', help='Renvoie la liste des contextes apparaissant dans le journal.')
    analyseur.add_argument('--enlever', default='noms_a_enlever.txt', help='Le fichier contenant la liste de noms à enlever.')

    args = analyseur.parse_args()

    stats_json = []

    assert args.nom_fichier.endswith(".json"), f"Le fichier doit être un .json. Fichier fourni : {args.nom_fichier}"

    with open(args.nom_fichier, 'r', encoding='utf-8') as f :
        stats_json = json.load(f)
        entrees = stats_json[0]
    noms_a_enlever = obtenir_noms_a_enlever(args.enlever)
       
    if args.noms :
        print(*sorted([nom_de_famille(nom) for nom in obtenir_noms()]), sep='\n')
        
    if args.valeur:
        afficher_tableau(args.valeur)

    if args.contextes :
        print(*sorted(obtenir_contextes()), sep='\n')
