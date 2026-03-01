import sqlite3
import pandas as pd

# Connexion à la base (crée le fichier s'il n'existe pas)
conn = sqlite3.connect('coinafrique_data.db')
cursor = conn.cursor()

# Charger les données scrapées
df = pd.read_csv('animaux_nettoyes.csv')

# Créer la table et insérer les données
# Si la table existe déjà, elle sera remplacée (if_exists='replace')
df.to_sql('animaux', conn, if_exists='replace', index=False)

print("Base de données SQL créée et alimentée avec succès !")
conn.close()
