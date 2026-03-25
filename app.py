import streamlit as st
import pandas as pd
import requests
import re
from PIL import Image
from io import BytesIO

# --- 1. CONFIGURATION & STYLE ---
st.set_page_config(page_title="Refuge Médéric - Officiel", layout="wide", page_icon="🐾")

# Importation des icônes pour le pied de page
st.markdown('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">',
            unsafe_allow_html=True)

# Fonction pour récupérer l'image réelle (données binaires)
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
    ### 🏠 1. Si c’est un chat, fouillez CHEZ VOUS
    ### 👃 2. Sortez sa litière
    ### 🗣️ 3. Appelez-le en début de soirée
    ### 🏘️ 4. Faites le tour du quartier
    ### 💻 5. Contactez les sites spécialisés (I-CAD, Pet Alert)
    ### 📞 6. Appelez les autorités (Fourrière, Refuge)
    """)

@st.dialog("🐾 Que faire si vous avez trouvé un animal errant ?", width="large")
def modal_trouve():
    st.markdown("""
    ⚠️ **Rappel :** Nous ne sommes pas habilités à nous déplacer.
    ### 🚫 1. Ne le prenez pas chez vous sans réfléchir
    ### 🏥 2. Amenez-le chez un vétérinaire (Vérification puce gratuite)
    ### 🚨 3. Contactez la mairie ou la police pour la fourrière
    """)

# --- STYLE CSS ---
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.main { background-color: #fdfdfd; }

.hero {
    background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)),
    url('https://images.unsplash.com/photo-1548199973-03cce0bbc87b?q=80&w=2000');
    background-size: cover; background-position: center;
    padding: 100px 20px; text-align: center; color: white;
    border-radius: 0 0 50px 50px; margin-bottom: 50px;
}

.btn-action {
    background-color: #FF0000; color: white !important;
    padding: 15px 30px; border-radius: 30px;
    text-decoration: none; font-weight: bold; display: inline-block;
}

.help-card-white {
    background-color: white; padding: 25px; border-radius: 15px;
    border-left: 5px solid #FF0000; box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    color: #1a1a1a; margin-bottom: 20px;
}

.event-card {
    background-color: white; padding: 20px; border-radius: 15px;
    border-bottom: 5px solid #FF0000; box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    margin-bottom: 20px; text-align: center;
}

.contact-card {
    background-color: white; padding: 35px; border-radius: 20px;
    box-shadow: 0 5px 20px rgba(0,0,0,0.1); border-left: 6px solid #FF0000;
}
</style>
""", unsafe_allow_html=True)

# --- 2. BANNIÈRE D'ACCUEIL ---
st.markdown("""
<div class="hero">
    <h1 style="font-size: 4em; color: white;">REFUGE MÉDÉRIC</h1>
    <p style="font-size: 1.5em; color: white;">Donnez une seconde chance à ceux qui n'ont que de l'amour à offrir.</p>
    <a href="#catalogue" class="btn-action">🐾 Voir nos animaux à l'adoption</a>
</div>
""", unsafe_allow_html=True)

# --- 3. ONGLETS ---
tab1, tab_event, tab2, tab_pension, tab3, tab4, tab_urgence = st.tabs(
    ["Le Refuge", "Actualités", "Adopter", "Pension", "Aider ❤️", "Contact", "🚨 Urgence"])

with tab1:
    col_refuge_1, col_refuge_2 = st.columns([1.2, 1])
    with col_refuge_1:
        st.markdown("<h3 style='color:#FF0000;'>📍 Notre Mission</h3>", unsafe_allow_html=True)
        st.write("L'association 'Les Animaux du Grand Dax' gère le refuge Médéric depuis 1980.")
    with col_refuge_2:
        st.markdown("<div class='contact-card'><h3>🙏 NOUS SOUTENIR</h3>", unsafe_allow_html=True)
        st.write("Votre aide est essentielle.")
        st.markdown('<a href="https://www.helloasso.com/associations/animaux-du-grand-dax/formulaires/2" style="background-color:#62af05; color:white; padding:15px; display:block; text-align:center; border-radius:10px; text-decoration:none;">Faire un don</a>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

with tab_event:
    st.markdown("<h2 style='text-align:center;'>ACTUALITÉS</h2>", unsafe_allow_html=True)
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
    st.markdown("<h2 style='text-align:center; color:#FF0000;'>NOS ANIMAUX À L'ADOPTION</h2>", unsafe_allow_html=True)
    # Ton lien de catalogue mis à jour
    url_catalogue = "https://apprefugemedb12py-edxprzycfpyjfmezl6y2em.streamlit.app/"
    st.components.v1.iframe(url_catalogue, height=900, scrolling=True)

with tab_pension:
    st.markdown("## Service de Pension")
    st.write("Nous accueillons vos chiens toute l'année.")
    st.table(pd.DataFrame({
        "Prestation": ["1 chien", "2 chiens"],
        "Tarif": ["15€ / jour", "23€ / jour"]
    }))

with tab3:
    st.markdown("## Comment nous aider ?")
    c1, c2, c3 = st.columns(3)
    c1.info("🕒 Temps (Bénévolat)")
    c2.info("💰 Argent (Dons)")
    c3.info("📦 Nature (Croquettes, couvertures)")

with tab4:
    st.markdown("## Contact & Accès")
    c_info, c_map = st.columns(2)
    with c_info:
        st.write("📍 182 chemin Lucien Viau, 40990 St-Paul-lès-Dax")
        st.write("📞 05 58 73 68 82")
    with c_map:
        map_data = pd.DataFrame({'lat': [43.72594], 'lon': [-1.05030]})
        st.map(map_data)

with tab_urgence:
    st.error("🚨 Section Urgence / Fourrière")
    if st.button("J'ai perdu un animal"): modal_perdu()
    if st.button("J'ai trouvé un animal"): modal_trouve()

# --- PIED DE PAGE ---
st.markdown("---")
col_f1, col_f2, col_f3, col_f4 = st.columns(4)
with col_f1: st.write("🐾 REFUGE MÉDÉRIC")
with col_f2: st.write("[Facebook](https://www.facebook.com/refuge.mederic)")
with col_f3: st.write("📞 05 58 73 68 82")
with col_f4: st.write("© 2026 - Alpha 1")

# --- FIN DU CODE ---
