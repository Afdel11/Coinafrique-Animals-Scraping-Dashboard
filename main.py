import streamlit as st
import pandas as pd
import base64
import plotly.express as px
import os

# CONFIGURATION DE LA PAGE 
st.set_page_config(page_title="AnimalData Pro Dashboard",
                   layout="wide", initial_sidebar_state="expanded")

# STYLE CSS  
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .main { background-color: #F8F9FB; }
    
    /* Cartes Dashboard */
    .metric-card {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        border: 1px solid #F1F5F9;
        text-align: center;
    }
    .metric-card h4 { margin-bottom: 5px; color: #64748B; font-size: 1.1rem; }
    .metric-card h2 { margin: 0; color: #1E293B; font-size: 2.2rem; }

    /* Boutons de sélection */
    .stButton > button {
        border-radius: 12px;
        height: 70px;
        font-weight: 600;
        border: 2px solid #E2E8F0;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        border-color: #4F46E5;
        background-color: #F5F3FF;
        color: #4F46E5;
    }

    /* Cartes Evaluation */
    .eval-card {
        background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%);
        color: white !important;
        padding: 35px;
        border-radius: 20px;
        text-align: center;
        text-decoration: none;
        display: block;
        transition: transform 0.3s;
    }
    .eval-card:hover { transform: translateY(-5px); box-shadow: 0 10px 20px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

# CONFIGURATION DES CHEMINS 
BASE_RAW_PATH = "web_scraper_data/"
RAW_FILES = {
    "🐶 Chiens": "Web_scraper-chiens_sn-coinafrique-com-2026-02-13.csv",
    "🐑 Moutons": "Web_scraper-moutons_sn-coinafrique-com-2026-02-13.csv",
    "🐔 Volailles": "Web_scraper-poules-lapins-et-pigeons_sn-coinafrique-com-2026-02-13.csv",
    "🐾 Autres": "Web_scraper-autres-animaux_sn-coinafrique-com-2026-02-13.csv"
}

# FONCTION TÉLÉCHARGEMENT 


def get_download_link(df, filename):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    return f'''<a href="data:file/csv;base64,{b64}" download="{filename}" 
    style="text-decoration:none; background:#10B981; color:white; padding:12px 25px; border-radius:10px; font-weight:bold; display:inline-block; margin-top:10px;">
    📥 Télécharger le fichier CSV</a>'''


#  NAVIGATION 
if "page" not in st.session_state:
    st.session_state.page = "Dashboard"

with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2172/2172894.png", width=80)
    st.title("Coinafrique Pro")
    st.markdown("")
    if st.button("📊 Dashboard & Stats"):
        st.session_state.page = "Dashboard"
    if st.button("📁 Données Brutes"):
        st.session_state.page = "Brutes"
    if st.button("📝 Évaluations"):
        st.session_state.page = "Eval"

#  PAGE 1 : DASHBOARD (NETTOYÉES) 
if st.session_state.page == "Dashboard":
    st.title("📈 Dashboard des Données Nettoyées")

    try:
        df = pd.read_csv('animaux_nettoyes.csv')

        #  Ligne de Statistiques 
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(
                f'<div class="metric-card"><h4>Total Annonces</h4><h2>{len(df)}</h2></div>', unsafe_allow_html=True)
        with col2:
            nb_chiens = len(df[df['Categorie'] == 'Chiens'])
            st.markdown(
                f'<div class="metric-card"><h4>🐶 Chiens</h4><h2>{nb_chiens}</h2></div>', unsafe_allow_html=True)
        with col3:
            nb_moutons = len(df[df['Categorie'] == 'Moutons'])
            st.markdown(
                f'<div class="metric-card"><h4>🐑 Moutons</h4><h2>{nb_moutons}</h2></div>', unsafe_allow_html=True)
        with col4:
            # Calcul automatique des "Autres" (Volailles + Autres du CSV)
            nb_autres = len(df) - (nb_chiens + nb_moutons)
            st.markdown(
                f'<div class="metric-card"><h4>🦜 Autres</h4><h2>{nb_autres}</h2></div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        #  Graphique et Aperçu 
        col_chart, col_data = st.columns([1, 1.5])
        with col_chart:
            st.subheader("Répartition Géographique")
            fig = px.pie(df, names='Categorie', hole=0.5,
                         color_discrete_sequence=px.colors.qualitative.Pastel)
            fig.update_layout(margin=dict(t=0, b=0, l=0, r=0))
            st.plotly_chart(fig, use_container_width=True)

        with col_data:
            st.subheader("Aperçu des données")
            st.dataframe(df.head(12), use_container_width=True)
    except:
        st.error(
            "⚠️ Fichier 'animaux_nettoyes.csv' introuvable dans le répertoire racine.")

#  PAGE 2 : DONNÉES BRUTES (4 CHOIX) 
elif st.session_state.page == "Brutes":
    st.title("📁 Explorateur de Données Brutes")
    st.info(
        "Sélectionnez l'un des jeux de données extraits via Web Scraper pour l'analyser.")

    # Grille de boutons
    col1, col2, col3, col4 = st.columns(4)
    for i, (label, file_name) in enumerate(RAW_FILES.items()):
        with [col1, col2, col3, col4][i]:
            if st.button(label):
                st.session_state.active_file = (label, file_name)

    # Zone d'affichage
    if "active_file" in st.session_state:
        label, file_name = st.session_state.active_file
        path = os.path.join(BASE_RAW_PATH, file_name)

        st.markdown(f"### 🔍 Fichier sélectionné : {label}")

        if os.path.exists(path):
            df_raw = pd.read_csv(path)
            st.write(f"Nombre de lignes brutes : **{len(df_raw)}**")
            st.dataframe(df_raw, use_container_width=True)
            st.markdown(get_download_link(df_raw, file_name),
                        unsafe_allow_html=True)
        else:
            st.warning(
                f"Fichier `{file_name}` non trouvé dans `{BASE_RAW_PATH}`.")

# PAGE ÉVALUATION 
elif st.session_state.page == "Eval":
    st.title("📝 Évaluation & Feedback")
    st.write(
        "Votre avis est précieux pour valider la qualité de la collecte de données.")

    st.markdown("<br>", unsafe_allow_html=True)
    col_g, col_k = st.columns(2)

    with col_g:
        st.markdown(f"""
            <a href="https://docs.google.com/forms/d/e/1FAIpQLSd5MCoXZaozxjgvJLvrRjSlqVHbVEu_o_poRXacY0Qw9xrsxA/viewform?usp=header" target="_blank" class="eval-card">
                <h2 style="color:white;">Google Forms</h2>
                <p style="color:rgba(255,255,255,0.8);">Évaluation de l'interface et des données</p>
                <div style="background:rgba(255,255,255,0.2); padding:8px; border-radius:10px; display:inline-block;">Accéder au formulaire ↗️</div>
            </a>
        """, unsafe_allow_html=True)

    with col_k:
        st.markdown(f"""
            <a href="https://ee.kobotoolbox.org/x/UApWpfET" target="_blank" class="eval-card" style="background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);">
                <h2 style="color:white;">KoboCollect</h2>
                <p style="color:rgba(255,255,255,0.8);">Rapport technique et validation</p>
                <div style="background:rgba(255,255,255,0.2); padding:8px; border-radius:10px; display:inline-block;">Accéder à Kobo ↗️</div>
            </a>
        """, unsafe_allow_html=True)

#  FOOTER 
st.markdown("")
st.caption(
    "© 2026 - Data Collection - By Afdel Desmond")
 