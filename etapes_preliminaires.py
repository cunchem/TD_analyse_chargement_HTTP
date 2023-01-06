# -*- coding: utf-8 -*-
import IP2Location # pour obtenir la geoloc à partir d'une adresse IP
import json # necessaire pour HarPage
from haralyzer import HarParser, HarPage # pour l'analyse de fichiers HAR

# On va utiliser IP2Location 
# Dans un premier temps on doit initialiser les bases de geolocalisation (IPV4 et IPV6)
# On doit préciser les fichiers contenant les données de geoloc de ces bases (ils doivent etre dans le le meme repertoire que le programme)
baseIPV4 = IP2Location.IP2Location("IP2LOCATION-LITE-DB5.BIN")
baseIPV6 = IP2Location.IP2Location("IP2LOCATION-LITE-DB5.IPV6.BIN")
# On va également avoir besoin d'utiliser l'utilitaire ipTools
ipTools = IP2Location.IP2LocationIPTools()



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
    if ipTools.is_ipv4(ip_server) : 
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
    if ipTools.is_ipv4(ip_server) : 
        rec = baseIPV4.get_all(ip_server) # Si l'adresse est en IPV4 on récupère l'enregistrement via la baseIPV4 en utilisant la fonction getall() 
    else :
        rec = baseIPV6.get_all(ip_server) # Sinon (l'adresse est en IPV6) on récupère l'enregistrement sur la baseIPV6
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
    
# ==== Test des fonctions ====
# On utilisera les coordonnées du site web d'une université australienne 
hostname = "www.sydney.edu.au"
ip_server = "2606:4700::6812:1ef8" # ici en IPV6

#  Récupération du TLD (Top Level Domain) et du domaine à partir d'un nom
tld = get_tld(hostname)
print(f"TLD = {tld}")
domain_2 = get_2nd_lvl_domain(hostname)
print(f"domaine de second niveau = {domain_2}")

# Détermination du type (V4 ou V6) d'une adresse IP
affiche_type_adresse(ip_server)
# Recupération du code pays à partir d'une adresse IP  
country = get_country_code(ip_server)
print(f"code pays : {country}")




# Lecture du fichier HAR
# Un fichier HAR est structuré comme une liste d'entrée (record). Chaque entrée correspond à un échange réseau, et donc à une ligne dans la console du navigateur
    
# On ouvre un fichier HAR en utilisant la fonction open  
with open("example.har", 'r') as f:
    # On charge ensuite la structure entière dans har_parser  
    har_parser = HarParser(json.loads(f.read()))

# On parcours chaque page chargée
for har_page in har_parser.pages:
    print()
    print("===== Page HAR : =====")
    print(str(har_page))
    # On parcours ensuite la structure entrée par entrée
    for e in har_page.entries:
        print("-- entrée HAR : --")
        # chaque entrée e correspond à record représentant une interaction réseau
        # une entrée est composée de différents attributs représentant les caractéristiques de l'échange
        # par exemple l'attribut  e.url contient l'URL demandée
        url = e.url
        print(f"URL : {url}")
        # Il existe d'autres attributs https://haralyzer.readthedocs.io/en/latest/basic/harentry.html
        # Affichez les attributs suivants : addresse IP du serveur, port, nom de l'hote (serveur) 
        print(e.serverAddress)
        print(e.port)
        print(e.request.host) # Attention l'attribut e.hostname correspond au hostname de la page demandé


    
