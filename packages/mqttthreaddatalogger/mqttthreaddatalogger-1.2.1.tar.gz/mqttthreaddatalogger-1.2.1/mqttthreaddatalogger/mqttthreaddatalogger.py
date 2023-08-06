import threading
import time
import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
import ssl
import base64
import random, string
import math
import json
import time
import csv
#import os.path
import os
import datetime

#x = datetime.datetime.now()

#print(x.strftime("%d-%m-%y %H:%M:%S"))

# fonction qui retourne une chaine aléatoire
def randomword(length):
    lettresEtChiffres = string.ascii_letters + string.digits
    chaineAleatoire = ''.join((random.choice(lettresEtChiffres) for i in range(length)))
    return chaineAleatoire

def enregistreFichier(nomFichier,champs,tab1): # exemple nomFichier = 'donnees.csv' 
    if not os.path.exists(nomFichier):
        with open(nomFichier, 'w', newline='') as file:
            writer = csv.writer(file, delimiter=';',quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
            #date = [datetime.datetime.now()]
            champsfichier = ["date"]
            for i in range(0,len(champs)):
                if isinstance(champs[i], list) :
                    champsfichier.append(champs[i][-1])
                else :
                    champsfichier.append(champs[i])
            writer.writerow(champsfichier)
    else :
        with open(nomFichier, 'a', newline='') as file:
            writer = csv.writer(file, delimiter=';',quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
            date = [datetime.datetime.now().strftime("%d-%m-%y %H:%M:%S")]
            tab1 = date +tab1
            writer.writerow(tab1)
            #    i+=1


class mqttthreaddatalogger (threading.Thread):
    def __init__(self, url, port, user, pwd, proto):      # données supplémentaires
        threading.Thread.__init__(self)  # ne pas oublier cette ligne
        # (appel au constructeur de la classe mère)
        self.url = url           # donnée supplémentaire ajoutée à la classe
        self.port = port
        self.user = user
        self.pwd = pwd
        self.proto = proto
        self.nomFichier = "donnees.csv"
        #self.data = []
        self.Key = []
        #self.topic = "/#"
        self.topic = []
        self.client = mqtt.Client(client_id= randomword(8),clean_session=True,protocol=mqtt.MQTTv311,transport=self.proto) # transport="tcp" pour ssl)
        self.client.username_pw_set(username=self.user,password=self.pwd)
        self.client.tls_set(tls_version=ssl.PROTOCOL_TLSv1_2)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        

    def run(self):
        self.client.connect(self.url, self.port, 60)
        self.client.loop_forever()
        
    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(self, client, userdata, flags, rc):
        if (str(rc)=="0"):
            print("Connexion MQTT effectuée avec succès ! ")
            print("Les données sélectionnées sont enregistrées dans le fichier : " + self.nomFichier)
            # Subscribing in on_connect()
            for i in range(len(self.topic)):            
                self.client.subscribe(self.topic[i])
                print("Abonnement au topic : " +self.topic[i])
        else :
            print("Problème de Connexion MQTT !!! ")
            print("Code d'erreur : "+str(rc))
      

    # The callback for when a PUBLISH message is received from the server.
    def on_message(self, client, userdata, msg):
        data = msg.payload.decode("utf-8").strip('\r\n') # decode et enlève les \r \n
        #print("message reçu")
        tab = []
        try:
            y = json.loads(data)
            for i in range(0,len(self.Key)):
                if isinstance(self.Key[i], list) :
                    topic = y[self.Key[i][0]]
                    for j in range(1,len(self.Key[i])):
                        topic = topic[self.Key[i][j]]
                    tab.append(topic)
                else :
                    tab.append(float(y[self.Key[i]]))# prends la valeurs ecl self.data[i] est une liste !!!!!
                #print(tab)
        except:
            print("problème de lecture JSON ",data)
        else:# si pas d'erreur
            print(data)
            enregistreFichier(self.nomFichier,self.Key,tab)
            #for i in range(len(tab)): 
            #    self.data[i].append(tab[i])
            #print(self.data[0])
            
    def selectTopic(self,top):
        self.topic = top
    
    def selectKey(self,tab):
        #list = []
        self.data = [[] for i in range(0,len(tab))]
        self.Key = tab
    
    def selectNomFichier(self,nomFic):
        #list = []
        self.nomFichier = nomFic



