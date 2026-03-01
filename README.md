# 🐾 AnimalData Pro - Scraping & Dashboard Coinafrique

Ce projet a été réalisé dans le cadre du **Projet 3 : Collecte de données**. L'objectif est de collecter, nettoyer et visualiser les annonces de la catégorie "Animaux" du site Coinafrique Sénégal.

## 🚀 Fonctionnalités
- **Scraping Automatisé** : Extraction de données avec `BeautifulSoup` sur plusieurs catégories (Chiens, Moutons, Volailles, Autres).
- **Données Brutes** : Accès aux fichiers CSV extraits via l'extension `Web Scraper`.
- **Dashboard Interactif** : Visualisation des statistiques clés et de la répartition géographique avec `Streamlit` et `Plotly`.
- **Évaluation** : Système de feedback intégré via `KoboCollect` et `Google Forms`.

## 🛠️ Stack Technique
* **Langage** : Python 3.x
* **Scraping** : BeautifulSoup4, Requests
* **Analyse de données** : Pandas
* **Visualisation** : Plotly Express
* **Interface Web** : Streamlit
* **Collecte de Feedback** : KoboToolbox (XLSForm)

## 📁 Structure du Projet
```text
├── app.py                 # Application principale Streamlit
├── scrap_all.py           # Script de scraping BeautifulSoup
├── animaux_nettoyes.csv   # Dataset final nettoyé
├── requirements.txt       # Dépendances du projet
└── web_scraper_data/      # Dossier contenant les 4 fichiers bruts CSV# Coinafrique-Animals-Scraping-Dashboard
