import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def scrape_coinafrique(base_url, category_name, num_pages=3):
    all_data = []
    # Headers pour éviter d'être bloqué
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    print(f"--- Début du scraping : {category_name} ---")
    
    for page in range(1, num_pages + 1):
        try:
            url = f"{base_url}?page={page}"
            print(f"Page {page} en cours...")
            
            res = requests.get(url, headers=headers, timeout=10)
            res.raise_for_status() # Vérifie si la requête a réussi
            
            soup = BeautifulSoup(res.text, 'html.parser')
            
            # Sélecteur des cartes d'annonces
            containers = soup.find_all('div', class_='col s6 m4 l3') 
            
            if not containers:
                print(f"Pas de données trouvées à la page {page}.")
                break

            for container in containers:
                try:
                    # Extraction selon les variables du Projet 3 
                    name = container.find('p', class_='ad__card-description').text.strip()
                    
                    price_raw = container.find('p', class_='ad__card-price').text.strip()
                    # Nettoyage du prix pour le dashboard
                    price = price_raw.replace('CFA', '').replace(' ', '').strip()
                    
                    address = container.find('p', class_='ad__card-location').text.strip()
                    
                    # Lien image
                    img_tag = container.find('img', class_='ad__card-img')
                    img_link = img_tag['src'] if img_tag else "Pas d'image"
                    
                    all_data.append({
                        'Nom_Details': name,
                        'Prix': price,
                        'Adresse': address,
                        'Image_Lien': img_link,
                        'Categorie': category_name
                    })
                except Exception:
                    continue
            
            # Petite pause pour ne pas surcharger le serveur
            time.sleep(1) 
            
        except Exception as e:
            print(f"Erreur sur la page {page}: {e}")
            break
                
    return pd.DataFrame(all_data)

# URLs du Projet 3
categories = [
    ("https://sn.coinafrique.com/categorie/chiens", "Chiens"),
    ("https://sn.coinafrique.com/categorie/moutons", "Moutons"),
    ("https://sn.coinafrique.com/categorie/poules-lapins-et-pigeons", "Volailles"),
    ("https://sn.coinafrique.com/categorie/autres-animaux", "Autres")
]

# Liste pour stocker les DataFrames
dfs = []

for url, cat in categories:
    df = scrape_coinafrique(url, cat, num_pages=2) # Teste avec 2 pages d'abord
    dfs.append(df)

# Fusion et sauvegarde
df_final = pd.concat(dfs, ignore_index=True)
df_final.to_csv('animaux_nettoyes.csv', index=False)
print("\nScraping terminé ! Fichier 'animaux_nettoyes.csv' créé.")
print(df_final.head())