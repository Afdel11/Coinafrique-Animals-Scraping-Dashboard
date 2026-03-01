import sqlite3
import pandas as pd

# Connexion à la bd
conn = sqlite3.connect('coinafrique_data.db')
cursor = conn.cursor()

# Charger les données
df = pd.read_csv('animaux_nettoyes.csv')

# Créer la table et insérer les données

df.to_sql('animaux', conn, if_exists='replace', index=False)

print("Base de données SQL créée et alimentée avec succès !")
conn.close()
