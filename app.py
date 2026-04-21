import streamlit as st
import pandas as pd
import requests
import re
import os
from io import BytesIO

# --- 1. CONFIGURATION & STYLE ---
st.set_page_config(page_title="Refuge Médéric - Officiel", layout="wide", page_icon="🐾")

# Importation des icônes
st.markdown('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">', unsafe_allow_html=True)

# Fonction pour les images Google Drive
@st.cache_data(ttl=600)
def get_image_data(url):
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

# Chargement des événements
@st.cache_data(ttl=300)
def charger_evenements_sheet():
    URL_EV = "https://docs.google.com/spreadsheets/d/1XZXKwCfJ_922HAkAANzpXyyZL97uJzcu84viFWdtgpA/export?format=csv&gid=1825198513"
    try:
        df = pd.read_csv(URL_EV)
        df.columns = df.columns.str.strip()
        return df.iloc[::-1].reset_index(drop=True)
    except:
        return pd.DataFrame()

# CSS Personnalisé
st.markdown("""
<style>
.main { background-color: #fdfdfd; }
.hero {
    background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), url('https://images.unsplash.com/photo-1548199973-03cce0bbc87b?q=80&w=2000');
    background-size: cover; background-position: center; padding: 80px 20px; text-align: center; color: white; border-radius: 0 0 50px 50px; margin-bottom: 40px;
}
.btn-action { background-color: #FF0000; color: white !important; padding: 12px 25px; border-radius: 30px; text-decoration: none; font-weight: bold; display: inline-block; }
.help-card-white { background-color: white; padding: 20px; border-radius: 15px; border-left: 5px solid #FF0000; box-shadow: 0 4px 15px rgba(0,0,0,0.05); margin-bottom: 20px; color: #1a1a1a; }
.contact-card { background-color: white; padding: 25px; border-radius: 20px; box-shadow: 0 5px 20px rgba(0,0,0,0.1); border-left: 6px solid #FF0000; color: #1a1a1a; }
</style>
""", unsafe_allow_html=True)

# --- 2. BANNIÈRE ---
st.markdown("""<div class="hero"><h1>REFUGE MÉDÉRIC</h1><p>Donnez une seconde chance à ceux qui n'ont que de l'amour à offrir.</p></div>""", unsafe_allow_html=True)

# --- 3. ONGLETS ---
tab1, tab_event, tab2, tab_pension, tab3, tab4, tab_urgence = st.tabs(
    ["Le Refuge", "Actualités", "Adopter", "Pension", "Aider ❤️", "Contact", "🚨 Urgence"])

with tab1:
    col_refuge_1, col_refuge_2 = st.columns([1.5, 1])
    with col_refuge_1:
        st.markdown("<h3 style='color:#FF0000;'>📍 Notre Mission</h3>", unsafe_allow_html=True)
        st.write("L'association **LES ANIMAUX DU GRAND DAX** gère le refuge Médéric. Nous assurons la transition entre l'abandon et une nouvelle vie.")
        st.markdown("<div class='help-card-white'><h4>📅 Journée Portes Ouvertes</h4><p>Venez rencontrer nos bénévoles et nos pensionnaires lors de nos événements réguliers !</p></div>", unsafe_allow_html=True)
    with col_refuge_2:
        st.markdown("<div class='contact-card'>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align:center;'>🙏 NOUS SOUTENIR</h3>", unsafe_allow_html=True)
        st.markdown('<a href="https://www.helloasso.com/associations/animaux-du-grand-dax/formulaires/2" style="background-color:#62af05; color:white; padding:15px; display:block; text-align:center; border-radius:10px; text-decoration:none; font-weight:bold;">Faire un don (HelloAsso)</a>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

with tab_event:
    df_ev = charger_evenements_sheet()
    if not df_ev.empty:
        for index, row in df_ev.iterrows():
            st.markdown(f"### {row['Cle']}")
            img = get_image_data(str(row['Valeur']))
            if img: st.image(img, width=400)
            st.divider()

with tab2:
    st.components.v1.iframe("https://refugemedb12-fuhsesxanqbpnqkdkxkaug.streamlit.app/?embed=true", height=800)

with tab3:
    st.markdown("<h2 style='text-align:center; color:#FF0000;'>COMMENT NOUS AIDER ?</h2>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    c1.markdown("<div class='help-card-white'><h4>🕒 Temps</h4><p>Devenez bénévole pour les balades et les câlins.</p></div>", unsafe_allow_html=True)
    c2.markdown("<div class='help-card-white'><h4>💰 Argent</h4><p>Dons via HelloAsso ou chèque au refuge.</p></div>", unsafe_allow_html=True)
    c3.markdown("<div class='help-card-white'><h4>📦 Nature</h4><p>Croquettes, couvertures et litières sont les bienvenus.</p></div>", unsafe_allow_html=True)

with tab4:
    ci, cm = st.columns([1, 1.2])
    with ci:
        st.markdown("""<div class='contact-card'><h4>📍 ADRESSE</h4><p>182 chemin Lucien Viau<br>40990 Saint-Paul-lès-Dax</p><h4>📞 CONTACT</h4><p>05 58 73 68 82</p></div>""", unsafe_allow_html=True)
    with cm:
        st.markdown('<div style="background-color:white; padding:15px; border-radius:20px; color:black;"><h4>🗺️ Plan d\'accès</h4></div>', unsafe_allow_html=True)
        map_data = pd.DataFrame({'lat': [43.7431], 'lon': [-1.0664]})
        st.map(map_data, zoom=14)
        st.markdown('<a href="https://wego.here.com/directions/drive/mylocation/43.7431,-1.0664" target="_blank" style="display:block; background:#FF0000; color:white; text-align:center; padding:10px; border-radius:10px; text-decoration:none; margin-top:10px;">🚀 Itinéraire HERE WeGo</a>', unsafe_allow_html=True)

with tab_urgence:
    cu1, cu2 = st.columns(2)
    with cu1:
        st.error("🚨 ANIMAL TROUVÉ / PERDU")
        st.write("Contactez immédiatement la mairie ou la police municipale du lieu de découverte.")
    with cu2:
        st.markdown("<div class='help-card-white'><h4>💰 Tarifs Fourrière</h4><p>Animal identifié : 40€<br>Non-identifié : 125€<br>+ 15€ / jour supp.</p></div>", unsafe_allow_html=True)

# --- 5. PIED DE PAGE ---
st.markdown("---")
f1, f2, f3, f4 = st.columns([1.5, 1, 1.2, 1])

with f1:
    st.markdown("<h4 style='color: #FF0000;'>🐾 REFUGE MÉDÉRIC</h4>", unsafe_allow_html=True)
    st.write("Association Les Animaux du Grand Dax.")

with f2:
    st.markdown("<h4 style='color: #FF0000;'>PLAN DU SITE</h4>", unsafe_allow_html=True)
    st.write("[Accueil](#) | [Adopter](#)")

with f3:
    st.markdown("<h4 style='color: #FF0000;'>📧 NEWSLETTER</h4>", unsafe_allow_html=True)
    email = st.text_input("E-mail", placeholder="votre@email.com", label_visibility="collapsed", key="news_key")
    if st.button("S'inscrire 🐾", key="btn_news_f"):
        if "password_admin" in st.secrets and email == st.secrets["password_admin"]:
            st.session_state.access_admin = True
            st.rerun()
        elif "@" in email:
            st.success("Inscrit !")

if st.session_state.get("access_admin", False):
    st.warning("🔓 Mode Admin Alpha_5")
    if st.button("Quitter l'admin"):
        st.session_state.access_admin = False
        st.rerun()

with f4:
    st.markdown("<h4 style='color: #FF0000;'>CONTACT</h4>", unsafe_allow_html=True)
    st.markdown(f"""
        <div style="line-height:2;">
            <a href="https://facebook.com/refuge.mederic" style="text-decoration:none; color:inherit;"><img src="https://upload.wikimedia.org/wikipedia/commons/b/b8/2021_Facebook_icon.svg" width="20"> Facebook</a><br>
            <a href="https://instagram.com/refuge_mederic/" style="text-decoration:none; color:inherit;"><img src="https://upload.wikimedia.org/wikipedia/commons/e/e7/Instagram_logo_2016.svg" width="20"> Instagram</a><br>
            <a href="mailto:animauxdugranddax@gmail.com" style="text-decoration:none; color:inherit;"><img src="https://upload.wikimedia.org/wikipedia/commons/7/7e/Gmail_icon_%282020%29.svg" width="20"> Gmail</a>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<p style='text-align: center; color: #888; font-size: 0.8em; margin-top:50px;'>© 2026 Refuge Médéric | 🤖 Version Alpha_5</p>", unsafe_allow_html=True)
