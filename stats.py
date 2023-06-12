import json
import datetime
import random
import numpy as np
import matplotlib.pyplot as plt

noms_a_enlever = set(['-', 'Elodie Roullot', 'Benjamin De Prost', 'Mathilde Capelle', 'Guillaume Roux', 'Leila Ben Youssef', 'Admin Utilisateur', 'Victorine Henaff', 'Paul Billon', 'Mohamed Bouchareb', 'Marine Lelong', 'Philippe Akueson'])

def num_de_semaine(date: str) -> int:
    mois_fr = ['janv.', 'févr.', 'mars', 'avril', 'mai', 'juin', 'juil.', 'août', 'sept.', 'oct.', 'nov.', 'déc.']
    mois_en = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']

    chaine_format = '%d %m %y, %H:%M'

    for avant, apres in zip(mois_fr, mois_en):
        date = date.replace(avant, apres)
    
    date = datetime.datetime.strptime(date, chaine_format)
    num = int( date.strftime('%U') )
    return num

def nom_de_famille(nom : str) -> str :
    mots = nom.split(" ")
    return " ".join(mots[1:])

def obtenir_noms(stats_json):
    noms = set()
    for ev in stats_json[0]:
        nom = ev[1]
        if not (nom in noms):
            #print("Ajout du nom", nom)
            noms.add(nom)
    return noms - noms_a_enlever

def obtenir_noms_ev(stats_json):
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

def compter_clef_nom(stats_stats, clef : str, nom : str) -> int :
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
if __name__ == '__main__':
    with open('total.json', 'r', encoding='utf-8') as f:
        stats_json = json.load(f)
    noms = obtenir_noms(stats_json)
    for nom in noms : 
        print(nom, "nombre de cours cousultés :", compter_clef_nom(stats_json, "Cours consulté", nom))
               
    
