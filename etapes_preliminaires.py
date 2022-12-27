# -*- coding: utf-8 -*-
import IP2Location # pour obtenir la geoloc à partir d'une adresse IP
import json # necessaire pour HarPage
from haralyzer import HarPage # pour l'analyse de fichiers HAR


hostname = "www.sydney.edu.au"
ip_server = "2606:4700::6812:1ef8" # ici en IPV6


#  Récupération du TLD (Top Level Domain) et du domaine à partir d'un nom
# Utiliser le découpage d'une chaine à l'aide de la fonction split
# Dans www.elysee.fr le tld est fr et le domaine est elysee.fr
tld = hostname.split('.')[-1]
print(f"TLD = {tld}")
domain_2 = hostname.split('.')[-2] + "." + tld
print(f"domaine de second niveau = {domain_2}")

# Recupération des coordonnées géographiques d'un serveur
# On va utiliser IP2Location 
# Dans un premier temps on doit initialiser les bases de geolocalisation (IPV4 et IPV6)
# On doit préciser les fichiers contenant les données de geoloc de ces bases (ils doivent etre dans le le meme repertoire que le programme)
baseIPV4 = IP2Location.IP2Location("IP2LOCATION-LITE-DB5.BIN")
baseIPV6 = IP2Location.IP2Location("IP2LOCATION-LITE-DB5.IPV6.BIN")
# On va également avoir besoin d'utiliser l'utilitaire ipTools
ipTools = IP2Location.IP2LocationIPTools()
 
# IP2Location stocke les information de geoloc sous forme d'enregistrementn : une structure contenant plusieurs champs : lat, lng, country ..
# La doc https://www.ip2location.com/development-libraries/ip2location/python

# Il faut distinguer les cas en fonction du type d'adresse IP (v4 ou v6) (en utilisant ipTools)
if ipTools.is_ipv4(ip_server) : 
    rec = baseIPV4.get_all(ip_server) # Si l'adresse est en IPV4 on récupère l'enregistrement via la baseIPV4 en utilisant la fonction getall() 
else :
    rec = baseIPV6.get_all(ip_server) # Sinon (l'adresse est en IPV6) on récupère l'enregistrement sur la baseIPV6
    
# On dispose maintenant de l'enregistrement "rec" correspondant à l'ip
# On peut maintenant accéder aux différents champs de l'enregistrement
lat = rec.latitude # latitude
lng = rec.longitude # longitude
print(f"lat,lng : {lat},{lng}")
# il existe un enregistrement "country_short" qui correspond au code court du pays
country = rec.country_short
print(f"code pays : {country}")


# Lecture du fichier HAR
# Un fichier HAR est structuré comme une liste d'entrée (record). Chaque entrée correspond à un échange réseau, et donc à une ligne dans la console du navigateur

# On ouvre un fichier HAR en utilisant la fonction open  
with open("example.har", 'r') as f:
    # On charge ensuite la structure dans la variable har_page à l'aide de la fonction HarPage  
    har_page = HarPage('page_1', har_data=json.loads(f.read())) # Attention le parametre page_1 peut avoir une autre valeur (généralement page_3)

# On parcours ensuite la structure entrée par entrée
for e in har_page.entries:
    print("== entrée HAR : ==")
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
    


    
