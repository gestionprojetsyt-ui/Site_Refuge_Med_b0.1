import streamlit as st
import pandas as pd
import requests
import re
import os
from io import BytesIO

# --- 1. CONFIGURATION & STYLE ---
st.set_page_config(page_title="Refuge Médéric - Officiel", layout="wide", page_icon="🐾")

st.markdown('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">',
            unsafe_allow_html=True)

# Fonction pour récupérer l'image réelle (Google Drive)
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

# Fonction pour charger les événements (Google Sheets)
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
    ### 🏠 1. Si c’est un chat, fouillez CHEZ VOUS
    Cherchez sous les lits, dans les placards... **si la tête passe, tout passe !**
    ### 👃 2. Sortez sa litière
    Les odeurs peuvent le guider vers sa maison.
    ### 🗣️ 3. Appelez-le en début de soirée
    Moins de bruit, plus de chances qu'il vous entende.
    ### 💻 4. Sites spécialisés
    I-CAD, Pet Alert 40, Chat-perdu.org.
    """)

@st.dialog("🐾 Que faire si vous avez trouvé un animal errant ?", width="large")
def modal_trouve():
    st.markdown("""
    ⚠️ **Rappel :** L'animal doit nous être déposé par la police ou les autorités compétentes.
    ### 🏥 1. Vétérinaire (Gratuit)
    Vérification de la puce électronique sans RDV.
    ### 🚨 2. Contactez la Mairie ou la Police
    Eux seuls peuvent déclencher la prise en charge en fourrière.
    """)

# CSS CUSTOM
st.markdown("""
<style>
#MainMenu, footer, header {visibility: hidden;}
.main { background-color: #fdfdfd; }
.hero {
    background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), url('https://images.unsplash.com/photo-1548199973-03cce0bbc87b?q=80&w=2000');
    background-size: cover; background-position: center; padding: 100px 20px; text-align: center; color: white; border-radius: 0 0 50px 50px; margin-bottom: 50px;
}
.btn-action { background-color: #FF0000; color: white !important; padding: 15px 30px; border-radius: 30px; text-decoration: none; font-weight: bold; display: inline-block; }
.btn-don-vert { background-color: #62af05; color: white !important; padding: 15px 25px; border-radius: 15px; text-decoration: none; font-weight: bold; display: block; text-align: center; margin-bottom: 15px; }
.help-card-white { background-color: white !important; padding: 25px; border-radius: 15px; border-left: 5px solid #FF0000; margin-bottom: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); color: #1a1a1a !important; }
.event-card { background-color: white !important; padding: 20px; border-radius: 15px; border-bottom: 5px solid #FF0000; box-shadow: 0 4px 15px rgba(0,0,0,0.05); margin-bottom: 20px; text-align: center; }
.contact-card { background-color: white !important; padding: 35px; border-radius: 20px; box-shadow: 0 5px 20px rgba(0,0,0,0.1); border-left: 6px solid #FF0000; color: #1a1a1a !important; }
</style>
""", unsafe_allow_html=True)

# --- 2. ACCUEIL ---
st.markdown('<div class="hero"><h1 style="font-size: 3.5em; color: white;">REFUGE MÉDÉRIC</h1><p style="font-size: 1.2em; color: white;">Donnez une seconde chance à ceux qui n\'ont que de l\'amour à offrir.</p><a href="#catalogue" class="btn-action">🐾 Voir les animaux</a></div>', unsafe_allow_html=True)

# --- 3. ONGLETS ---
t1, t2, t3, t4, t5, t6, t7 = st.tabs(["Refuge", "Actu", "Adopter", "Pension", "Aider", "Contact", "🚨 Urgence"])

with t1:
    st.markdown("<h3 style='color:#FF0000;'>📍 Notre Mission</h3>", unsafe_allow_html=True)
    st.write("L'association **LES ANIMAUX DU GRAND DAX** gère le refuge Médéric pour la protection et le placement des animaux.")
    st.info("ℹ️ SIREN : 993 900 000")

with t2:
    st.markdown("<h2 style='text-align:center;'>NOS ACTUALITÉS</h2>", unsafe_allow_html=True)
    df_ev = charger_evenements_sheet()
    if not df_ev.empty:
        for i, row in df_ev.iterrows():
            st.markdown(f'<div class="event-card"><h3>{row["Cle"]}</h3></div>', unsafe_allow_html=True)
            img_data = get_image_data(str(row['Valeur']))
            if img_data: st.image(img_data, use_container_width=True)

with t3:
    st.components.v1.iframe("https://refugemedb12-fuhsesxanqbpnqkdkxkaug.streamlit.app/?embed=true", height=800)

with t4:
    st.write("### Tarifs Pension")
    tarifs = {"Prestation": ["1 chien", "2 chiens"], "Public": ["15€/j", "23€/j"], "Ancien du refuge": ["13€/j", "20€/j"]}
    st.table(pd.DataFrame(tarifs))

with t5:
    st.markdown('<a href="https://www.helloasso.com/associations/animaux-du-grand-dax/formulaires/2" class="btn-don-vert">Faire un don ❤️</a>', unsafe_allow_html=True)
    if os.path.exists("info_benevole.pdf"):
        with open("info_benevole.pdf", "rb") as f:
            st.download_button("📄 Dossier Bénévole (PDF)", f, "info_benevole.pdf", "application/pdf")

with t6:
    st.markdown('<div class="contact-card"><h4>📍 ADRESSE</h4><p>182 chemin Lucien Viau, 40990 St-Paul-lès-Dax<br>📞 05 58 73 68 82</p></div>', unsafe_allow_html=True)
    st.map(pd.DataFrame({'lat': [43.72594], 'lon': [-1.05030]}))

with t7:
    c1, c2 = st.columns(2)
    with c1: 
        if st.button("🔍 J'ai perdu mon animal", use_container_width=True, type="primary"): modal_perdu()
    with c2:
        if st.button("🐾 J'ai trouvé un animal", use_container_width=True): modal_trouve()

# --- 4. FOOTER & NEWSLETTER ---
st.markdown("---")
col_f = st.columns(3)
with col_f[1]:
    st.write("📧 **Newsletter**")
    email = st.text_input("Email", label_visibility="collapsed")
    if st.button("S'inscrire"):
        if "@" in email:
            with open("liste_newsletter.txt", "a") as f: f.write(email + "\n")
            st.success("Enregistré !")

# --- 5. ADMIN SÉCURISÉ ---
with st.expander("🔐 Admin"):
    pwd_input = st.text_input("Code", type="password")
    
    # Gestion sécurisée du mot de passe
    mdp_secret = "mederic40" # Valeur par défaut
    if "password_admin" in st.secrets:
        mdp_secret = st.secrets["password_admin"]

    if pwd_input == mdp_secret:
        if os.path.exists("liste_newsletter.txt"):
            with open("liste_newsletter.txt", "r") as f:
                emails = f.read()
            st.dataframe([e for e in emails.split("\n") if e])
            st.download_button("Télécharger la liste", emails, "liste.txt")
        else:
            st.info("Aucun inscrit.")
