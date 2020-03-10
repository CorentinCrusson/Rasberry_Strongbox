# python 3.7
#coding: utf-8

import requests
import json
import mariadb
# import RPi.GPIO as GPIO  # Importe la bibliothèque pour contrôler les GPIOs
#from pirc522 import RFID
import time
from login import *


def callApi(url):
    r = requests.get(url)
    if r.status_code != 200:
        raise Exception("Erreur {}".format(r.status_code))
    data = r.json()

    return data


def initDatabase():
    conn = mariadb.connect(
        host="localhost",
        user="root",
        passwd="root",
        database="enregistrement"
    )
    cursor = conn.cursor()

    return conn, cursor


def insertDatabase(connDb="", cur="", idCon="", badgeCon="", etape="", loginOk=""):
    cur.execute("""INSERT INTO enregistrement (idInfirmiere,commentaire,numEtape,etat) VALUES (%s,%s,%s,%s)""",
                (idCon, badgeCon, etape, loginOk))
    connDb.commit()


def waitBadge():
    # On affiche un message demandant à l'utilisateur de passer son badge
    print('En attente d\'un badge : ')
    vretour = True

    # On va faire une boucle infinie pour lire en boucle
    while vretour:
        rc522.wait_for_tag()  # On attnd qu'une puce RFID passe à portée
        # Quand une puce a été lue, on récupère ses infos
        (error, tag_type) = rc522.request()

        if not error:  # Si on a pas d'erreur
            # On nettoie les possibles collisions, ça arrive si plusieurs cartes passent en même temps
            (error, uid) = rc522.anticoll()

            if not error:  # Si on a réussi à nettoyer
                badgeCon = uid
                vretour = False
    return badgeCon


def verifFace():
    vretour = False

    return vretour


def etape1(url, conn, cursor):

    loginOk = False

    idCon, passCon = createWindow()

    tryUrl = url + idCon+"/"+passCon+"/infirmiere"
    data = callApi(tryUrl)

    try:
        print("Bonjour {0} {1} !".format(data['nom'], data['prenom']))
        loginOk = True
    except:
        print("Échec de Connexion")

    insertDatabase(connDb=conn, cur=cursor, idCon=idCon,
                   etape='1', loginOk=loginOk)

    return loginOk


def etape2(url, conn, cursor):
    # RECUP ID BADGE

    rc522 = RFID()  # On instancie la lib

    loginOk = False

    badgeCon = waitBadge()

    tryUrl = url + badgeCon+"/infirmiere"

    data = callApi(tryUrl)

    try:
        print("Connexion réussi pour le badge {0}".format(data['badge']))
        loginOk = True
    except:
        print("Echec de Connexion")
        loginOk = False

    insertDatabase(connDb=conn, cur=cursor, badgeCon=badgeCon,
                   etape='2', loginOk=loginOk)

    return loginOk


def etape3(url, conn, cursor):
    print("En attente de la Reconnaissance du Visage ...")
    loginOk = verifFace()

    insertDatabase(connDb=conn, cur=cursor,
                   etape='3', loginOk=loginOk)

    return loginOk


def main():

    url = "http://www.btssio-carcouet.fr/ppe4/public/connect2/"

    #conn, cursor = initDatabase()
    conn, cursor = ("", "")

    if etape1(url, conn, cursor) is True:
        if etape2(url, conn, cursor) is True:
            if etape3(url, conn, cursor) is True:
                print('etape3 OK')
            else:
                return False
        else:
            return False

    else:
        return False

    return True


if __name__ == "__main__":
    main()
