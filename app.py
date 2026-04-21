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

# Fonction pour récupérer l'image réelle
@st.cache_data(ttl=600)
def get_image_data(url):
    try:
        if not isinstance(url, str) or 'drive.google.com' not in url:
            return None
        file_id = re.search(r'(?:id=|[/\b])([a-zA-Z0-9_-]{25,})', url).group(1)
        direct_url = f'https://drive.google.com/uc?export=download&id={file_id}'
        response = requests.get(direct_url, timeout=10)
        if response.status_code == 200:
            return BytesIO(response.content)
    except Exception:
        return None
    return None

# Fonction pour charger les événements
@st.cache_data(ttl=300)
def charger_evenements_sheet():
    URL_EV = "https://docs.google.com/spreadsheets/d/1XZXKwCfJ_922HAkAANzpXyyZL97uJzcu84viFWdtgpA/export?format=csv&gid=1825198513"
    try:
        df = pd.read_csv(URL_EV)
        df.columns = df.columns.str.strip()
        df = df.iloc[::-1].reset_index(drop=True)
        return df
    except:
        return pd.DataFrame()

# --- FENÊTRES SURGISSANTES (DIALOGS) ---
@st.dialog("🔍 Que faire si vous avez perdu votre animal ?", width="large")
def modal_perdu():
    st.markdown("""
    *Publié par animauxdugranddax le 1 janvier 2026*
    Quand un animal disparaît, le plus efficace est d’agir vite pour éviter qu’il ne s’éloigne trop.
    ### 🏠 1. Si c’est un chat, fouillez CHEZ VOUS
    Cherchez sous les lits, dans les placards... **si la tête passe, tout passe !**
    ### 👃 2. Sortez sa litière (pour les chats)
    Astuce étrange mais efficace : ne lavez pas la litière. Les odeurs peuvent guider votre compagnon.
    ### 🗣️ 3. Appelez-le en début de soirée
    ### 🏘️ 4. Faites le tour du quartier
    ### 💻 5. Contactez les sites spécialisés (I-CAD, Pet Alert 40)
    ### 📞 6. Appelez les autorités (Fourrière, Refuge, Mairies)
    ---
    ### ✨ Les bons gestes à l'avenir
    * **Identification :** Obligatoire, elle offre 75% de chances en plus.
    * **Stérilisation :** Calme les envies d'évasion.
    """)

@st.dialog("🐾 Que faire si vous avez trouvé un animal errant ?", width="large")
def modal_trouve():
    st.markdown("""
    ⚠️ **Rappel important :** Nous ne sommes pas habilités à nous déplacer. L'animal doit nous être déposé par la police ou les autorités compétentes.
    ### 🚫 1. Ne prenez pas l'animal chez vous si vous n'en voulez pas
    ### 🏘️ 2. Faites le tour du quartier
    ### 💻 3. Vérifiez les sites spécialisés (Pet Alert 40)
    ### 🏥 4. Amenez-le chez un vétérinaire (Gratuit pour lecture de puce)
    ### 🚨 5. Contactez les autorités pour la fourrière
    """)

# --- STYLE CSS ---
st.markdown("""
<style>
#MainMenu, footer, header {visibility: hidden;}
.main { background-color: #fdfdfd; }
.hero {
    background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), url('https://images.unsplash.com/photo-1548199973-03cce0bbc87b?q=80&w=2000');
    background-size: cover; background-position: center; padding: 100px 20px; text-align: center; color: white; border-radius: 0 0 50px 50px; margin-bottom: 50px;
}
.btn-action { background-color: #FF0000; color: white !important; padding: 15px 30px; border-radius: 30px; text-decoration: none; font-weight: bold; font-size: 1.2em; display: inline-block; }
.btn-mail { background-color: #333333; color: white !important; padding: 15px 30px; border-radius: 30px; text-decoration: none; font-weight: bold; display: inline-block; }
.btn-don-vert { background-color: #62af05; color: white !important; padding: 15px 25px; border-radius: 15px; text-decoration: none; font-weight: bold; display: block; text-align: center; margin-bottom: 15px; }
.help-card-white { background-color: white !important; padding: 25px; border-radius: 15px; border-left: 5px solid #FF0000; margin-bottom: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); color: #1a1a1a !important; height: 100%; }
.project-card-full { background-color: white !important; padding: 20px; border-radius: 15px; border-left: 5px solid #FF0000; margin-bottom: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); color: #1a1a1a !important; }
.event-card { background-color: white !important; padding: 20px; border-radius: 15px; border-bottom: 5px solid #FF0000; box-shadow: 0 4px 15px rgba(0,0,0,0.05); margin-bottom: 20px; text-align: center; color: #1a1a1a !important; }
.contact-card { background-color: white !important; padding: 35px; border-radius: 20px; box-shadow: 0 5px 20px rgba(0,0,0,0.1); border-left: 6px solid #FF0000; color: #1a1a1a !important; margin-bottom: 25px; }
</style>
""", unsafe_allow_html=True)

# --- HEADER HERO ---
st.markdown("""
<div class="hero">
<h1 style="font-size: 4em; margin-bottom: 10px; color: white;">REFUGE MÉDÉRIC</h1>
<p style="font-size: 1.5em; margin-bottom: 30px; color: white;">Donnez une seconde chance à ceux qui n'ont que de l'amour à offrir.</p>
<a href="#catalogue" class="btn-action">🐾 Voir nos animaux à l'adoption</a>
</div>
""", unsafe_allow_html=True)

# --- STATS RAPIDES ---
col1, col2, col3 = st.columns(3)
with col1: st.markdown("<div style='text-align:center;'><h3>📍 Localisation</h3><p>Saint-Paul-lès-Dax (40)</p></div>", unsafe_allow_html=True)
with col2: st.markdown("<div style='text-align:center;'><h3>🐕 Nos Pensionnaires</h3><p>Chiens et chats de tous âges</p></div>", unsafe_allow_html=True)
with col3: st.markdown("<div style='text-align:center;'><h3>❤️ Notre Engagement</h3><p>Soins, protection et amour</p></div>", unsafe_allow_html=True)

st.markdown("---")

# --- ONGLETS ---
tab1, tab_event, tab2, tab_pension, tab3, tab4, tab_urgence = st.tabs(
    ["Le Refuge", "Nos Actualités", "Nos Animaux", "Pension", "Nous Aider ❤️", "Contact & Accès", "🚨 Urgence/Fourrière"])

with tab1:
    col_refuge_1, col_refuge_2 = st.columns([1.2, 1])
    with col_refuge_1:
        st.markdown("<h3 style='color:#FF0000;'>📍 Notre Mission & Identité</h3>", unsafe_allow_html=True)
        st.write("L'association **LES ANIMAUX DU GRAND DAX** (SIREN : 993 900 000) gère le refuge Médéric.")
        st.markdown("<br><h3 style='color:#FF0000;'>🚀 Nos Projets & Événements</h3>", unsafe_allow_html=True)
        st.markdown('<div class="project-card-full"><h4>📅 Journée Portes Ouvertes</h4><p>Venez rencontrer nos chiens et nos chats et notre équipe de passionnés !</p></div>', unsafe_allow_html=True)
        st.markdown('<div class="project-card-full"><h4>🐈 Amélioration de la Fourrière Chats</h4><p>Des travaux sont prévus pour améliorer l\'accueil. Nous avons besoin de dons de matériaux et de bras !</p></div>', unsafe_allow_html=True)
    with col_refuge_2:
        st.markdown("<div class='contact-card' style='margin-top:0;'><h3 style='text-align:center; margin-top:0;'>🙏 NOUS SOUTENIR</h3><a href='https://www.helloasso.com/associations/animaux-du-grand-dax/formulaires/2' class='btn-don-vert'><i class='fas fa-heart'></i> Faire un don (HelloAsso)</a></div>", unsafe_allow_html=True)

with tab_event:
    st.markdown("<h2 style='text-align:center; color:#FF0000;'>NOS ACTUALITÉS EN IMAGES</h2>", unsafe_allow_html=True)
    df_ev = charger_evenements_sheet()
    if not df_ev.empty:
        for i in range(0, len(df_ev), 2):
            cols_ev = st.columns(2)
            for j in range(2):
                if i + j < len(df_ev):
                    row = df_ev.iloc[i + j]
                    with cols_ev[j]:
                        st.markdown('<div class="event-card">', unsafe_allow_html=True)
                        img_data = get_image_data(str(row['Valeur']))
                        if img_data: st.image(img_data, use_container_width=True)
                        st.markdown(f"<h3>{row['Cle']}</h3></div>", unsafe_allow_html=True)

with tab2:
    st.components.v1.iframe("https://refugemedb12-fuhsesxanqbpnqkdkxkaug.streamlit.app/?embed=true", height=900, scrolling=True)

with tab_pension:
    st.markdown("<h2 style='text-align:center; color:#FF0000;'>SERVICE DE PENSION</h2>", unsafe_allow_html=True)
    col_p1, col_p2 = st.columns([1.5, 1])
    with col_p1:
        st.markdown("### 🏠 Un accueil toute l'année")
        st.write("Nos box sont spacieux et peuvent accueillir jusqu'à deux chiens d'une même famille.")
    with col_p2:
        st.image("https://images.unsplash.com/photo-1516734212186-a967f81ad0d7?q=80&w=1000")
    tarifs_data = {"Prestation": ["1 chien", "2 chiens"], "Tout Public": ["15€ / jour", "23€ / jour"], "Adopté chez nous": ["13€ / jour", "20€ / jour"]}
    st.table(pd.DataFrame(tarifs_data))

with tab3:
    st.markdown("<h2 style='text-align:center; color:#FF0000;'>NOUS AIDER</h2>", unsafe_allow_html=True)
    ca, cb, cc = st.columns(3)
    with ca: st.markdown('<div class="help-card-white"><h4>🕒 Temps</h4><p>Promenades, nourrissage, nettoyage.</p></div>', unsafe_allow_html=True)
    with cb: st.markdown('<div class="help-card-white"><h4>💰 Don financier</h4><p>HelloAsso, Chèques, Tookets.</p></div>', unsafe_allow_html=True)
    with cc: st.markdown('<div class="help-card-white"><h4>📦 Don en nature</h4><p>Croquettes, litières, couvertures.</p></div>', unsafe_allow_html=True)
    if os.path.exists("info_benevole.pdf"):
        with open("info_benevole.pdf", "rb") as f:
            st.download_button("📄 Télécharger le dossier d'intégration (PDF)", f, "info_benevole.pdf", "application/pdf", use_container_width=True)

with tab4:
    st.markdown("<h2 style='text-align:center; color:#FF0000;'>INFORMATIONS & ACCÈS</h2>", unsafe_allow_html=True)
    c_info, c_map = st.columns([1, 1.2])
    with c_info:
        st.markdown('<div class="contact-card"><h4>📍 ADRESSE</h4><p>182 chemin Lucien Viau, 40990 St-Paul-lès-Dax</p><h4>⏰ HORAIRES</h4><p>Mercredi au Dimanche : 14h-18h</p><h4>📞 CONTACT</h4><p>05 58 73 68 82</p></div>', unsafe_allow_html=True)
    with c_map:
        st.map(pd.DataFrame({'lat': [43.72594], 'lon': [-1.05030]}), zoom=14)

with tab_urgence:
    st.markdown("<h2 style='text-align:center; color:#FF0000;'>🚨 SERVICE DE FOURRIÈRE</h2>", unsafe_allow_html=True)
    c_u1, c_u2 = st.columns(2)
    with c_u1: 
        if st.button("🔍 J'ai perdu mon animal", use_container_width=True, type="primary"): modal_perdu()
    with c_u2:
        if st.button("🐾 J'ai trouvé un animal", use_container_width=True): modal_trouve()
    st.markdown('<div class="help-card-white"><h4>💰 Tarifs Fourrière</h4><p>Identifié : 40€ | Non-identifié : 125€ | Supplément : 15€/jour</p></div>', unsafe_allow_html=True)

# --- FOOTER ---
st.markdown("---")
col_f1, col_f2, col_f3, col_f4 = st.columns([1.5, 1, 1.2, 1])
with col_f1: st.markdown("<h4 style='color: #FF0000;'>🐾 REFUGE MÉDÉRIC</h4><p>Association Animaux du Grand Dax</p>", unsafe_allow_html=True)
with col_f3:
    st.markdown("<h4 style='color: #FF0000;'>📧 NEWSLETTER</h4>", unsafe_allow_html=True)
    email_user = st.text_input("Votre e-mail", placeholder="votre@email.com", label_visibility="collapsed", key="mail_f")
    if st.button("S'inscrire 🐾"):
        if "@" in email_user:
            with open("liste_newsletter.txt", "a") as f: f.write(email_user + "\n")
            st.success("Enregistré !")

# --- ADMINISTRATION SÉCURISÉE (VIA SECRETS) ---
st.markdown("---")
with st.expander("🔐 Administration"):
    code_secret = st.text_input("Code secret", type="password", key="admin_pwd")
    
    # Utilisation des secrets Streamlit pour protéger le mot de passe
    try:
        real_password = st.secrets["admin_password"]
        if code_secret == real_password:
            if os.path.exists("liste_newsletter.txt"):
                with open("liste_newsletter.txt", "r") as f: contenu = f.read()
                st.download_button("📥 Télécharger les mails", contenu, "emails.txt")
                st.code(contenu)
            else:
                st.info("Liste vide.")
    except KeyError:
        st.error("Action requise : Définissez 'admin_password' dans les Secrets de votre Dashboard Streamlit.")
