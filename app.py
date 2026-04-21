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

st.markdown('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">',
            unsafe_allow_html=True)

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

# --- DIALOGS ---
@st.dialog("🔍 Que faire si vous avez perdu votre animal ?", width="large")
def modal_perdu():
    st.markdown("""
    ### 🏠 1. Si c’est un chat, fouillez CHEZ VOUS
    Cherchez sous les lits, les placards... si la tête passe, tout passe !
    ### 👃 2. Sortez sa litière
    ### 🗣️ 3. Appelez-le en début de soirée
    ### 🏘️ 4. Faites le tour du quartier
    ### 💻 5. Contactez les sites spécialisés (I-CAD, Pet Alert 40)
    ### 📞 6. Appelez les autorités (Fourrière, Refuge)
    """)

@st.dialog("🐾 Que faire si vous avez trouvé un animal errant ?", width="large")
def modal_trouve():
    st.markdown("""
    ⚠️ **Rappel :** L'animal doit nous être déposé par la police ou les autorités.
    ### 🚫 1. Ne prenez pas l'animal chez vous
    ### 🏘️ 2. Faites le tour du quartier
    ### 🏥 3. Amenez-le chez un vétérinaire (Gratuit pour lecture puce)
    ### 🚨 4. Contactez la mairie ou la police
    """)

st.markdown("""
<style>
#MainMenu, footer, header {visibility: hidden;}
.main { background-color: #fdfdfd; }
.hero {
    background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), url('https://images.unsplash.com/photo-1548199973-03cce0bbc87b?q=80&w=2000');
    background-size: cover; background-position: center; padding: 100px 20px; text-align: center; color: white; border-radius: 0 0 50px 50px; margin-bottom: 50px;
}
.btn-action { background-color: #FF0000; color: white !important; padding: 15px 30px; border-radius: 30px; text-decoration: none; font-weight: bold; display: inline-block; }
.btn-don-vert { background-color: #62af05; color: white !important; padding: 15px 25px; border-radius: 15px; text-decoration: none; font-weight: bold; display: block; text-align: center; }
.help-card-white { background-color: white !important; padding: 25px; border-radius: 15px; border-left: 5px solid #FF0000; margin-bottom: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); color: #1a1a1a !important; }
.event-card { background-color: white !important; padding: 20px; border-radius: 15px; border-bottom: 5px solid #FF0000; box-shadow: 0 4px 15px rgba(0,0,0,0.05); margin-bottom: 20px; text-align: center; color: #1a1a1a !important; }
.contact-card { background-color: white !important; padding: 35px; border-radius: 20px; box-shadow: 0 5px 20px rgba(0,0,0,0.1); border-left: 6px solid #FF0000; color: #1a1a1a !important; }
</style>
""", unsafe_allow_html=True)

# --- ACCUEIL ---
st.markdown('<div class="hero"><h1 style="font-size: 4em; color: white;">REFUGE MÉDÉRIC</h1><p style="font-size: 1.5em; color: white;">Donnez une seconde chance à ceux qui n\'ont que de l\'amour à offrir.</p><a href="#catalogue" class="btn-action">🐾 Voir nos animaux à l\'adoption</a></div>', unsafe_allow_html=True)

# --- ONGLETS ---
tab1, tab_event, tab2, tab_pension, tab3, tab4, tab_urgence = st.tabs(["Le Refuge", "Actualités", "Adopter", "Pension", "Aider ❤️", "Contact", "🚨 Urgence"])

with tab1:
    st.markdown("<h3 style='color:#FF0000;'>📍 Notre Mission</h3>", unsafe_allow_html=True)
    st.write("L'association **LES ANIMAUX DU GRAND DAX** gère le refuge Médéric pour la protection et le placement des animaux.")
    st.info("ℹ️ SIREN : 993 900 000")

with tab_event:
    df_ev = charger_evenements_sheet()
    if not df_ev.empty:
        for i, row in df_ev.iterrows():
            st.markdown(f'<div class="event-card"><h3>{row["Cle"]}</h3>', unsafe_allow_html=True)
            img = get_image_data(str(row['Valeur']))
            if img: st.image(img, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.components.v1.iframe("https://refugemedb12-fuhsesxanqbpnqkdkxkaug.streamlit.app/?embed=true", height=900)

with tab_pension:
    st.write("### Tarifs Pension")
    tarifs = {"Prestation": ["1 chien", "2 chiens"], "Public": ["15€/j", "23€/j"], "Adopté chez nous": ["13€/j", "20€/j"]}
    st.table(pd.DataFrame(tarifs))

with tab3:
    st.markdown('<a href="https://www.helloasso.com/associations/animaux-du-grand-dax/formulaires/2" class="btn-don-vert">Faire un don ❤️</a>', unsafe_allow_html=True)
    if os.path.exists("info_benevole.pdf"):
        with open("info_benevole.pdf", "rb") as f:
            st.download_button("📄 Dossier Intégration (PDF)", f, "info_benevole.pdf", "application/pdf", use_container_width=True)

with tab4:
    st.markdown('<div class="contact-card"><h4>📍 ADRESSE</h4><p>182 chemin Lucien Viau, 40990 St-Paul-lès-Dax<br>📞 05 58 73 68 82</p></div>', unsafe_allow_html=True)
    st.map(pd.DataFrame({'lat': [43.72594], 'lon': [-1.05030]}))

with tab_urgence:
    c1, c2 = st.columns(2)
    with c1: 
        if st.button("🔍 J'ai perdu mon animal", use_container_width=True, type="primary"): modal_perdu()
    with c2:
        if st.button("🐾 J'ai trouvé un animal", use_container_width=True): modal_trouve()

# --- FOOTER ---
st.markdown("---")
cf1, cf2, cf3 = st.columns(3)
with cf2:
    st.write("📧 **Newsletter**")
    email = st.text_input("Email", key="news", label_visibility="collapsed")
    if st.button("S'inscrire"):
        if "@" in email:
            with open("liste_newsletter.txt", "a") as f: f.write(email + "\n")
            st.success("Inscrit !")

# --- ADMINISTRATION SÉCURISÉE ---
with st.expander("🔐 Administration"):
    pwd = st.text_input("Code secret", type="password")
    
    # Récupération sécurisée du mot de passe via les secrets Streamlit
    try:
        real_password = st.secrets["admin_password"]
        if pwd == real_password:
            if os.path.exists("liste_newsletter.txt"):
                with open("liste_newsletter.txt", "r") as f: contenu = f.read()
                st.download_button("📥 Télécharger les emails", contenu, "emails.txt")
                st.code(contenu)
            else:
                st.info("Liste vide.")
    except KeyError:
        st.error("Configuration requise : Veuillez définir 'admin_password' dans les Secrets Streamlit.")
