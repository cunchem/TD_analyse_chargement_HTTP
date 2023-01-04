#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  1 10:48:05 2022

@author: cunche
"""

import IP2Location # pour géolocaliser un serveur à partir d'une adresse IP
import json # necessaire pour HarPage
from haralyzer import HarPage # pour lire le fichier .har
import numpy as np #  pour l'analyse de données
import matplotlib.pyplot as plt #  pour créer des graphs
import pandas as pd # pour l'analyse de données



# Initialisation des bases IP2Location
baseIPV4 = IP2Location.IP2Location("IP2LOCATION-LITE-DB5.BIN")
baseIPV6 = IP2Location.IP2Location("IP2LOCATION-LITE-DB5.IPV6.BIN")
ipTools = IP2Location.IP2LocationIPTools()


# vvvv Ne pas modifier vvvv:

def process_data(my_data) : 
    '''
    Traite les données pour produire des résultats (valeurs et plots) à partir d'une liste 2D dans laquelle chaque ligne correspond aux attributs d'un échange réseau
        Parameters:
            my_data : une liste 2D donc chaque ligne contient les attributs ['hostname','tld','domain','requestSize', 'responseSize', 'country'] d'un échange réseau
    '''
    # préparation du dataframe    
    my_array = np.array(my_data)      
    df = pd.DataFrame(my_array, columns = ['hostname','tld','domain','requestSize', 'responseSize', 'country'])
    df=df.astype({'requestSize' : 'int64', 'responseSize' : 'int64'})
    # Conversion des tailles de données en Ko (/1000)
    df['requestSize']=df['requestSize'].div(1000)
    df['responseSize']=df['responseSize'].div(1000)
    
    print("="*20)
    # nb de domaines de second niveau contactés
    nb_domain = len(pd.unique(df["domain"]))
    print(f"Nombre de domaine de second niveau : {nb_domain}")    
    plot_data(df)


def plot_vol_sent_per_country(df,axes):
    # Volume de données envoyé par pays
    data = df.groupby("country")["requestSize"].sum().sort_values(ascending=True)
    plot_subplot(data,axes,"Volume (Ko)","Volume envoyé par pays")
    
def plot_vol_recv_per_country(df,axes):
    # Volume de données recues par pays
    data = df.groupby("country")["responseSize"].sum().sort_values(ascending=True)
    plot_subplot(data,axes,"Volume (Ko)","Volume recu par pays")
    
def plot_vol_sent_per_2nd_lvl_domain(df,axes):
     # Volume de données envoyé par domaine de 2nd niveau
    data = df.groupby("domain")["requestSize"].sum().sort_values(ascending=True).tail(15)
    plot_subplot(data,axes,"Volume (Ko)","Volume envoyé par domaine de 2nd niveau")

def plot_vol_recv_per_2nd_lvl_domain(df,axes):
     # Volume de données reçu par domaine de 2nd niveau
    data = df.groupby("domain")["responseSize"].sum().sort_values(ascending=True).tail(15)
    plot_subplot(data,axes,"Volume (Ko)","Volume reçu par domaine de 2nd niveau")
    
def plot_vol_recv_per_country(df,axes):
    # Volume de données recues par pays
    data = df.groupby("country")["responseSize"].sum().sort_values(ascending=True)
    plot_subplot(data,axes,"Volume (Ko)","Volume recu par pays")

def plot_nb_exchange_per_country(df,axes):
    # Nombre d'échanges par pays
    data = df.groupby("country")["country"].count().sort_values(ascending=True)
    plot_subplot(data,axes,"Nb. echanges","Nb. échanges par pays")

def plot_nb_exchange_per_2nd_lvl_domain(df,axes):
    # Nombre d'échanges par domaine de 2nd niveau
    data = df.groupby("domain")["domain"].count().sort_values(ascending=True).tail(15)
    plot_subplot(data,axes,"Nb. echanges","Nb. échanges par domaine 2nd niv")

    
def plot_subplot(data,axes,xlabel,title):
    '''
    Génère, à partir de données, un subplot placé sur des axes avec un titre global et un titre pour l'axe des abscisses
        Parameters:
            data : les données sous forme d'une liste d'entiers
            axes : les axes sur lesquels sera placé le subplot
            xlabel : le titre de l'axe des abscisses
            title : le titre global du subplot
    '''
    axes.set_xlabel(xlabel)
    axes.set_title(title,y=-0.5)
    data.plot(kind='barh',ax=axes)
    
def plot_data(df) :
    '''
    Génère les graphes de résultats à partir d'un dataframe 2D dans laquelle chaque ligne correspond aux attributs d'un échange réseau
        Parameters:
            df : un dataframe 2D donc chaque ligne contient les attributs ['hostname','tld','domain','requestSize', 'responseSize', 'country'] d'un échange réseau
    '''
    # préparation des plots
    fig, axes = plt.subplots(nrows=3, ncols=2, constrained_layout = True)
    # Volume de données envoyé par pays
    plot_vol_sent_per_country(df,axes[0,0])
    # Volume de données recues par pays
    plot_vol_recv_per_country(df,axes[0,1])
    # Volume de données envoyé par domaine de 2nd niveau
    plot_vol_sent_per_2nd_lvl_domain(df,axes[1,0])
    # Volume de données recues par domaine de 2nd niveau
    plot_vol_recv_per_2nd_lvl_domain(df,axes[1,1])
    # Nombre d'échanges par pays
    plot_nb_exchange_per_country(df,axes[2,0])
    # Nombre d'échanges par domaine de 2nd niveau
    plot_nb_exchange_per_2nd_lvl_domain(df,axes[2,1])


        
def analyse_entry(entry):
    '''
    Analyse une entrée HAR et retourne une liste contenant des informations sur cet échange
        Parameters :
            entry : (HARentry) une entrée HAR correspondant à un échange réseau
        Returns : 
            res : une liste contenant des informations sur la page :  hostname, tld, domain_2, requestSize, responseSize, country, ou None si il y a un problème avec l'entrée
    '''
    
    
    print("=============================")

    # Liste des variables à renseigner
    hostname = ""
    tld = "" # Top Level Domain
    domain_2 = "" # Domaine de second niveau
    requestSize = 0 # Taille de la requete
    responseSize = 0 # Taille de la réponse
    country = "" # code du pays ou se trouve le serveur
    
    # Récupération de l'IP du serveur :
    try :
        ipServeur = entry.serverAddress
    except KeyError :
        # Certaines entrée n'ont pas d'attribut serverAdress car elles ont été bloquées
        # Dans ce cas, on retourne None à la place de la liste
        return None    
        
        
    # TODO : récupérer / calculer la valeurs des variables précédentes
    
    # Hostname
    hostname = entry.request.host
    print(f"hostname = {hostname}")
    # TLD et domain_2
    tld = hostname.split('.')[-1]
    print(f"TLD = {tld}")
    domain_2 = hostname.split('.')[-2] + "." + tld
    print(f"domain de second niveau = {domain_2}")
    # requestSize et responseSize
    requestSize = entry.request.bodySize
    responseSize = entry.response.bodySize
    # country code
    
    if ipTools.is_ipv4(ipServeur) :
        rec = baseIPV4.get_all(ipServeur) #https://www.ip2location.com/development-libraries/ip2location/python
    else :
        rec = baseIPV6.get_all(ipServeur)
    country = rec.country_short 
    
    # Les résultats sont rangés dans une liste avant d'être retournés
    res = [hostname, tld, domain_2, requestSize, responseSize, country]
    return res    


# TODO : renseigner le nom du fichier du journal HAR a ouvrir
with open("har_data.har", 'r') as f:
    har_page = HarPage('page_3', har_data=json.loads(f.read())) # en cas d'erreur avec le page_id, modifier en "page_1"


my_data = []
for e in har_page.entries:
    a = analyse_entry(e)
    print(a)
    if a != None : # on ignore les None (problème identifié avec l'entrée)
        my_data += [a]
process_data(my_data)

