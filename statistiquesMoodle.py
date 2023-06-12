# coding: utf-8

import argparse
import os
import json
import datetime
import random
import numpy as np
import matplotlib.pyplot as plt

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

def obtenir_noms(stats_json):
    noms_a_enlever = obtenir_noms_a_enlever('noms_a_enlever.txt')
    noms = set()
    for ev in stats_json[0]:
        nom = ev[1]
        if not (nom in noms):
            #print("Ajout du nom", nom)
            noms.add(nom)
    return noms - noms_a_enlever

def obtenir_noms_ev(stats_json, noms_a_enlever=set()):
    noms_ev_a_enlever = set([])
    noms_ev = set()
    for ev in stats_json[0]:
        nom = ev[1]
        nom_ev = ev[5]
        if not (nom in noms_a_enlever) and not (nom_ev in noms_ev):
            #print("Ajout du nom", nom)
            noms_ev.add(nom_ev)
    return noms_ev - noms_ev_a_enlever

def obtenir_histo(stats_json, nom):
    histo = 53 * [0] # 53 semaines
    for ev in stats_json[0]:
        nom_courant = ev[1]
        if nom_courant == nom:
            histo[num_de_semaine(ev[0])] += 1
    return histo

def compter_clef_nom(stats_json, clef : str, nom : str) -> int :
    n_clef = 0
    for ev in stats_json[0] :
        nom_courant = ev[1]
        #print(nom_courant, nom)
        if nom_courant == nom and clef in ev :
            #print(ev, clef, nom)
            n_clef += 1
    return n_clef
    
def test1():
    histo = 26 * [0]
    with open('oscar.json', 'r') as f:
        stats_json = json.load(f)
        for ev in stats_json[0]:
            histo[num_de_semaine(ev[0])] += 1

    print(histo)

    for i, n in enumerate(histo):
        print(f"Semaine {i:2} : {n:3} connexion(s)")

def test2():
    noms = set()
    with open('total.json', 'r') as f:
        stats_json = json.load(f)
        for ev in stats_json[0]:
            nom = ev[1]
            if not nom in noms:
                #print("Ajout du nom ", nom)
                noms.add(nom)

        elu = random.choice(list(noms))

        print("Nom choisi : ", elu)
        
        for ev in stats_json[0]:
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
def test4():
    with open('total.json', 'r', encoding='utf-8') as f:
        stats_json = json.load(f)
    noms_ev = obtenir_noms_ev(stats_json)
    print(*noms_ev,sep='\n')

def test5():
    with open('total.json', 'r', encoding='utf-8') as f:
        stats_json = json.load(f)
        noms = obtenir_noms(stats_json)
        for nom in noms : 
            print(nom, "nombre de cours consultés :", compter_clef_nom(stats_json, "Cours consulté", nom))
               
if __name__ == '__main__':
    analyseur = argparse.ArgumentParser('statistiquesMoodle', 'Extrait des statistiques des journaux Moodle.')
    
    analyseur.add_argument('nom_fichier', help='Le nom du fichier à analyser.')

    args = analyseur.parse_args()

    print('Nom du fichier :', args.nom_fichier)

    stats_json = []
    with open(args.nom_fichier, 'r', encoding='utf-8') as f :
        stats_json = json.load(f)
        print(*sorted([nom_de_famille(nom) for nom in obtenir_noms(stats_json)]), sep='\n')
