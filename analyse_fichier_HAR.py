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
    

def plot_nb_exchange_per_country(df,axes):
    # Nombre d'échanges par pays
    data = df.groupby("country")["country"].count().sort_values(ascending=True)
    plot_subplot(data,axes,"Nb. echanges","Nb. échanges par pays")

def plot_nb_exchange_per_2nd_lvl_domain(df,axes):
    # Nombre d'échanges par domaine de 2nd niveau
    data = df.groupby("domain")["domain"].count().sort_values(ascending=True).tail(15)
    plot_subplot(data,axes,"Nb. echanges","Nb. échanges par domaine 2nd niv")
def plot_nb_contact_per_2nd_lvl_domain(df,axes):
    # Nombre de domaines de 2nd niveau contactés
    data = df["domain"].value_counts()
    n = data.size
    #print(data)
    print(n)
    axes.axis('off')
    axes.text(0.1, 0.1, f'Nombre de domaines de 2nd niveau contactés : {n}', style='italic',   bbox={'facecolor': 'blue', 'alpha': 0.5, 'pad': 10})
    
    
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
    total = data.sum()
    for p in axes.patches:
        percentage = '{:.1f}%'.format(100 * p.get_width()/total)
        x = p.get_x() + p.get_width() + 0.02
        y = p.get_y() + p.get_height()/2 -0.1
        axes.annotate(percentage, (x, y), fontsize = 6)
    
def plot_data(df) :
    '''
    Génère les graphes de résultats à partir d'un dataframe 2D dans laquelle chaque ligne correspond aux attributs d'un échange réseau
        Parameters:
            df : un dataframe 2D donc chaque ligne contient les attributs ['hostname','tld','domain','requestSize', 'responseSize', 'country'] d'un échange réseau
    '''
    # préparation des plots
    fig, axes = plt.subplots(nrows=4, ncols=2, constrained_layout = True)
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
    # Desactivation des axes de la 4eme ligne pour faire de la place pour le texte  
    axes[3,0].axis('off')    
    axes[3,1].axis('off')
    # Nombre de domaines tiers / serveur contactés
    plot_nb_contact_per_2nd_lvl_domain(df,axes[3,0])
    
    
    plt.show()


# Fonctions provenant de l'exercice préliminaire 
# TODO Q4.1 : ajouter vos fonctions ici 
    
def get_tld(hostname):
    '''
    Retourne le TLD d'un hostname
    Parameters :
        hostname (string) : le hostname
    Returns :
        tld (string) : le TLD
    '''
    tld = hostname.split('.')[-1]
    return tld

def get_2nd_lvl_domain(hostname):
    '''
    Retourne le domaine de second niveau d'un hostname
    Parameters :
        hostname (string) : le hostname
    Returns :
        domain_2 (string) : le domaine de second niveau
    '''
    tld = get_tld(hostname)
    domain_2 = hostname.split('.')[-2] + "." + tld
    return domain_2
    

def affiche_type_adresse(ip):
    '''
    Affiche le type d'une adresse IP
    Parameters :
        ip (string) : l'adresse IP
    '''
    if ipTools.is_ipv4(ip) : 
        print("IPV4")
    else :
        print("IPV6")

def get_IP2Loc_record(ip):
    '''
    Récupère l'enregristrement IP2Location correspondant à une adresse IP
    Parameters :
        ip (string) : l'adresse IP
    Returns : 
        rec (record) : l'enregistrement 
    '''
    # IP2Location stocke les information de geoloc sous forme d'enregistrementn : une structure contenant plusieurs champs : lat, lng, country ..
    # La doc https://www.ip2location.com/development-libraries/ip2location/python

    # Il faut distinguer les cas en fonction du type d'adresse IP (v4 ou v6) (en utilisant ipTools)
    if ipTools.is_ipv4(ip) : 
        rec = baseIPV4.get_all(ip) # Si l'adresse est en IPV4 on récupère l'enregistrement via la baseIPV4 en utilisant la fonction getall() 
    else :
        rec = baseIPV6.get_all(ip) # Sinon (l'adresse est en IPV6) on récupère l'enregistrement sur la baseIPV6
    return rec

def get_country_code(ip):
    '''
    Retourne le code pays associé à une adresse IP
    Parameters :
        ip (string) : l'adresse IP
    Returns : 
        country_code : le code pays
    '''
    rec = get_IP2Loc_record(ip)    
    return rec.country_short
    

    

# Analyse d'une entrée
        
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
        ip_server = entry.serverAddress
    except KeyError :
        # Certaines entrée n'ont pas d'attribut serverAdress car elles ont été bloquées
        # Dans ce cas, on retourne None à la place de la liste
        return None    
        
    # TODO Q4.2 : récupérer / calculer la valeurs des variables précédentes
    # Hostname
    hostname = entry.request.host
    print(f"hostname = {hostname}")
    
    # TODO Q4.3 
    # TLD et domain_2
    tld = get_tld(hostname)
    print(f"TLD = {tld}")
    domain_2 = get_2nd_lvl_domain(hostname)
    print(f"domain de second niveau = {domain_2}")
    
    # TODO Q4.4 
    # requestSize et responseSize
    requestSize = entry.request.bodySize
    responseSize = entry.response.bodySize
    
    # TODO Q4.5 
    # country code
    country = get_country_code(ip_server)
    
    # Les résultats sont rangés dans une liste avant d'être retournés
    res = [hostname, tld, domain_2, requestSize, responseSize, country]
    return res    


# TODO : renseigner le nom du fichier du journal HAR a ouvrir
har_file_name = "har_data.har"
with open(har_file_name, 'r', encoding="utf-8") as f:
    har_page = HarPage('page_3', har_data=json.loads(f.read())) # en cas d'erreur avec le page_id, modifier en "page_1"


my_data = []
for e in har_page.entries:
    a = analyse_entry(e)
    print(a)
    if a != None : # on ignore les None (problème identifié avec l'entrée)
        my_data += [a]
process_data(my_data)

