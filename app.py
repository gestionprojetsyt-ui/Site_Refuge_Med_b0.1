import streamlit as st
import pandas as pd
import requests
import base64
import re
import os
from PIL import Image
from io import BytesIO

# --- 1. CONFIGURATION & STYLE ---
st.set_page_config(page_title="Refuge Médéric - Officiel", layout="wide", page_icon="🐾")

# Importation des icônes pour le pied de page
st.markdown('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">',
            unsafe_allow_html=True)

# --- FONCTIONS TECHNIQUES ---

@st.cache_data(ttl=600)
def get_image_data(url):
    """Récupère l'image réelle (données binaires) depuis Google Drive."""
    try:
        if not isinstance(url, str) or 'drive.google.com' not in url:
            return None
        file_id = re.search(r'(?:id=|[/\b])([a-zA-Z0-9_-]{25,})', url).group(1)
        direct_url = f'https://drive.google.com/uc?export=download&id={file_id}'
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(direct_url, headers=headers, timeout=10)
        if response.status_code == 200:
            return BytesIO(response.content)
    except Exception:
        return None
    return None

@st.cache_data(ttl=300)
def charger_evenements_sheet():
    """Charge les actualités depuis le Google Sheet."""
    URL_EV = "https://docs.google.com/spreadsheets/d/1XZXKwCfJ_922HAkAANzpXyyZL97uJzcu84viFWdtgpA/export?format=csv&gid=1825198513"
    try:
        df = pd.read_csv(URL_EV)
        df.columns = df.columns.str.strip()
        return df.iloc[::-1].reset_index(drop=True)
    except:
        return pd.DataFrame()

# --- FENÊTRES SURGISSANTES (DIALOGS) ---

@st.dialog("🔍 Que faire si vous avez perdu votre animal ?", width="large")
def modal_perdu():
    st.markdown("""
    ### 🏠 1. Fouillez CHEZ VOUS
    Cherchez sous les lits, dans les placards... **si la tête passe, tout passe !**
    ### 👃 2. Sortez sa litière
    Les odeurs guident l'animal vers sa maison.
    ### 🗣️ 3. Appelez-le en début de soirée
    Au calme, agitez une boîte de croquettes.
    ### 💻 4. Contactez les sites spécialisés
    * **I-CAD** (Déclaration obligatoire)
    * **Pet Alert 40** / **Chat-perdu.org**
    """)

@st.dialog("🐾 Que faire si vous avez trouvé un animal errant ?", width="large")
def modal_trouve():
    st.markdown("""
    ⚠️ **Rappel important :** Nous ne sommes pas habilités à récupérer les animaux sur la voie publique.
    ### 🏥 1. Vérifiez l'identification
    Amenez-le chez un vétérinaire pour une lecture de puce gratuite.
    ### 🚨 2. Contactez les autorités
    Vous devez passer par la **mairie ou la police** pour obtenir l'autorisation de nous amener l'animal en fourrière.
    """)

# --- STYLE CSS (LE STYLE CARTES BLANCHES) ---
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.stApp { background-color: #fdfdfd; }

.hero {
    background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)),
    url('https://images.unsplash.com/photo-1548199973-03cce0bbc87b?q=80&w=2000');
    background-size: cover; background-position: center;
    padding: 100px 20px; text-align: center; color: white;
    border-radius: 0 0 50px 50px; margin-bottom: 50px;
}

.btn-action {
    background-color: #FF0000; color: white !important;
    padding: 15px 30px; border-radius: 30px; text-decoration: none;
    font-weight: bold; font-size: 1.2em; display: inline-block;
}

.btn-don-vert {
    background-color: #62af05; color: white !important;
    padding: 15px 25px; border-radius: 15px; text-decoration: none;
    font-weight: bold; display: block; text-align: center; margin-bottom: 15px;
}

.help-card-white {
    background-color: white !important; padding: 25px; border-radius: 15px;
    border-left: 5px solid #FF0000; margin-bottom: 20px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.05); color: #1a1a1a !important;
}

.event-card {
    background-color: white !important; padding: 20px; border-radius: 15px;
    border-bottom: 5px solid #FF0000; box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    margin-bottom: 20px; text-align: center;
}

.contact-card {
    background-color: white !important; padding: 35px; border-radius: 20px;
    box-shadow: 0 5px 20px rgba(0,0,0,0.1); border-left: 6px solid #FF0000;
}
</style>
""", unsafe_allow_html=True)

# --- 2. BANNIÈRE D'ACCUEIL ---
st.markdown("""
<div class="hero">
    <h1 style="font-size: 4em; color: white;">REFUGE MÉDÉRIC</h1>
    <p style="font-size: 1.5em; color: white;">Donnez une seconde chance à ceux qui n'ont que de l'amour à offrir.</p><br>
    <a href="#catalogue" class="btn-action">🐾 Voir nos animaux à l'adoption</a>
</div>
""", unsafe_allow_html=True)

# --- 3. SECTIONS D'INFORMATION (ONGLETS) ---
tab1, tab_event, tab2, tab_pension, tab3, tab4, tab_urgence = st.tabs(
    ["Le Refuge", "Nos Actualités", "Nos Animaux", "Pension", "Nous Aider ❤️", "Contact & Accès", "🚨 Urgence"])

with tab1:
    col_refuge_1, col_refuge_2 = st.columns([1.2, 1])
    with col_refuge_1:
        st.markdown("<h3 style='color:#FF0000;'>📍 Notre Mission</h3>", unsafe_allow_html=True)
        st.write("L'association **LES ANIMAUX DU GRAND DAX** gère le refuge Médéric. Nous assurons la transition entre l'abandon et une nouvelle vie.")
        
        st.markdown("<h3 style='color:#FF0000;'>🚀 Nos Projets</h3>", unsafe_allow_html=True)
        st.markdown('<div class="help-card-white"><h4>📅 Portes Ouvertes</h4><p>Rencontrez nos protégés et notre équipe !</p></div>', unsafe_allow_html=True)
        st.markdown('<div class="help-card-white"><h4>🐈 Fourrière Chats</h4><p>Rénovation urgente prévue. Besoin de dons de matériaux.</p></div>', unsafe_allow_html=True)

    with col_refuge_2:
        st.markdown("<div class='contact-card'>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align:center;'>🙏 NOUS SOUTENIR</h3>", unsafe_allow_html=True)
        st.markdown('<a href="https://www.helloasso.com/associations/animaux-du-grand-dax/formulaires/2" class="btn-don-vert">Faire un don (HelloAsso)</a>', unsafe_allow_html=True)
        st.info("Appel particulier : Nous recherchons des bras volontaires pour les travaux !")
        st.markdown("</div>", unsafe_allow_html=True)

with tab_event:
    st.markdown("<h2 style='text-align:center; color:#FF0000;'>ACTUALITÉS</h2>", unsafe_allow_html=True)
    df_ev = charger_evenements_sheet()
    if not df_ev.empty:
        for i in range(0, len(df_ev), 2):
            cols_ev = st.columns(2)
            for j in range(2):
                if i + j < len(df_ev):
                    row = df_ev.iloc[i + j]
                    with cols_ev[j]:
                        st.markdown('<div class="event-card">', unsafe_allow_html=True)
                        img = get_image_data(str(row['Valeur']))
                        if img: st.image(img, use_container_width=True)
                        st.markdown(f"<h4>{row['Cle']}</h4></div>", unsafe_allow_html=True)

with tab2:
    st.markdown("<div id='catalogue'></div>", unsafe_allow_html=True)
    st.components.v1.iframe("https://refugemedb12-fuhsesxanqbpnqkdkxkaug.streamlit.app/?embed=true", height=900, scrolling=True)

with tab_pension:
    st.markdown("<h2 style='text-align:center; color:#FF0000;'>PENSION CANINE</h2>", unsafe_allow_html=True)
    st.write("Box spacieux, sortie quotidienne et dodo confortable.")
    tarifs = {"Prestation": ["1 chien", "2 chiens"], "Public": ["15€/j", "23€/j"], "Adopté chez nous": ["13€/j", "20€/j"]}
    st.table(pd.DataFrame(tarifs))

with tab3:
    st.markdown("<h2 style='text-align:center; color:#FF0000;'>NOUS AIDER</h2>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1: st.markdown('<div class="help-card-white"><h4>🕒 Temps</h4><p>Bénévolat pour promenades et câlins.</p></div>', unsafe_allow_html=True)
    with c2: st.markdown('<div class="help-card-white"><h4>💰 Argent</h4><p>Dons via HelloAsso ou chèque.</p></div>', unsafe_allow_html=True)
    with c3: st.markdown('<div class="help-card-white"><h4>📦 Nature</h4><p>Croquettes, couvertures, litière.</p></div>', unsafe_allow_html=True)
    
    st.markdown("### 📝 Devenir Bénévole")
    if os.path.exists("info_benevole.pdf"):
        with open("info_benevole.pdf", "rb") as f:
            st.download_button("📄 Télécharger le dossier (PDF)", f, "info_benevole.pdf", "application/pdf")
    else:
        st.warning("Dossier d'intégration bientôt disponible.")

with tab4:
    c_info, c_map = st.columns([1, 1.2])
    with c_info:
        st.markdown('<div class="contact-card"><h4>📍 ADRESSE</h4><p>182 chemin Lucien Viau, 40990 St-Paul-lès-Dax</p><h4>⏰ HORAIRES</h4><p>Mer. au Dim. : 14h - 18h</p></div>', unsafe_allow_html=True)
    with c_map:
        st.map(pd.DataFrame({'lat': [43.7431], 'lon': [-1.0664]}), zoom=14)

with tab_urgence:
    st.error("🚨 URGENCE & FOURRIÈRE")
    if st.button("🔍 J'AI PERDU MON ANIMAL"): modal_perdu()
    if st.button("🐾 J'AI TROUVÉ UN ANIMAL"): modal_trouve()

# --- 4. PIED DE PAGE ---
st.markdown("---")
cf1, cf2, cf3 = st.columns([1.5, 1, 1.5])
with cf1:
    st.markdown("<h4 style='color: #FF0000;'>REFUGE MÉDÉRIC</h4>", unsafe_allow_html=True)
    st.write("Association Les Animaux du Grand Dax.")
with cf2:
    st.markdown("<h4 style='color: #FF0000;'>LIENS</h4>", unsafe_allow_html=True)
    st.write("[Facebook](https://www.facebook.com/refuge.mederic)")
with cf3:
    st.markdown("<h4 style='color: #FF0000;'>NEWSLETTER</h4>", unsafe_allow_html=True)
    mail = st.text_input("Votre e-mail", key="news", label_visibility="collapsed")
    if st.button("S'inscrire"):
        if "password_admin" in st.secrets and mail == st.secrets["password_admin"]:
            st.session_state.access_admin = True
            st.rerun()
        elif "@" in mail: st.success("Enregistré !")

if st.session_state.get("access_admin", False):
    st.warning("🔓 Mode Admin activé")
    if st.button("Quitter"): st.session_state.access_admin = False; st.rerun()

st.markdown("<p style='text-align: center; color: #888; font-size: 0.8em;'><br>© 2026 Refuge Médéric</p>", unsafe_allow_html=True)
