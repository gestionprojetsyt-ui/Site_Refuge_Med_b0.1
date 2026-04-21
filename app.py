import streamlit as st
import pandas as pd
import requests
import re
from io import BytesIO
from streamlit_gsheets import GSheetsConnection

# --- 1. CONFIGURATION & STYLE ---
st.set_page_config(page_title="Refuge Médéric - Officiel", layout="wide", page_icon="🐾")

# Importation des icônes
st.markdown('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">', unsafe_allow_html=True)

# CSS Personnalisé
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.main { background-color: #fdfdfd; }

.hero {
    background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), url('https://images.unsplash.com/photo-1548199973-03cce0bbc87b?q=80&w=2000');
    background-size: cover; background-position: center; padding: 100px 20px; text-align: center; color: white; border-radius: 0 0 50px 50px; margin-bottom: 50px;
}

.btn-action { background-color: #FF0000; color: white !important; padding: 15px 30px; border-radius: 30px; text-decoration: none; font-weight: bold; font-size: 1.2em; transition: 0.3s; display: inline-block; }
.btn-don-vert { background-color: #62af05; color: white !important; padding: 15px 25px; border-radius: 15px; text-decoration: none; font-weight: bold; display: block; text-align: center; margin-bottom: 15px; }

.help-card-white { background-color: white; padding: 25px; border-radius: 15px; border-left: 5px solid #FF0000; margin-bottom: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); color: #1a1a1a; }
.contact-card { background-color: white; padding: 35px; border-radius: 20px; box-shadow: 0 5px 20px rgba(0,0,0,0.1); border-left: 6px solid #FF0000; color: #1a1a1a; }

div[data-testid="stTextInput"] input { background-color: #262626 !important; color: white !important; border: 1px solid #444 !important; }
</style>
""", unsafe_allow_html=True)

# --- 2. FONCTIONS UTILES ---
@st.cache_data(ttl=600)
def get_image_data(url):
    try:
        file_id = re.search(r'(?:id=|[/\b])([a-zA-Z0-9_-]{25,})', url).group(1)
        direct_url = f'https://drive.google.com/uc?export=download&id={file_id}'
        response = requests.get(direct_url, timeout=10)
        return BytesIO(response.content) if response.status_code == 200 else None
    except: return None

@st.cache_data(ttl=300)
def charger_evenements_sheet():
    URL_EV = "https://docs.google.com/spreadsheets/d/1XZXKwCfJ_922HAkAANzpXyyZL97uJzcu84viFWdtgpA/export?format=csv&gid=1825198513"
    try:
        df = pd.read_csv(URL_EV)
        return df.iloc[::-1].reset_index(drop=True)
    except: return pd.DataFrame()

# --- 3. DIALOGS ---
@st.dialog("🔍 Perdu votre animal ?")
def modal_perdu():
    st.write("Agissez vite ! Vérifiez les recoins, sortez la litière et contactez l'I-CAD.")

@st.dialog("🐾 Animal trouvé ?")
def modal_trouve():
    st.write("Vérifiez l'identification chez un véto. Contactez la mairie avant de nous l'amener.")

# --- 4. HEADER ---
st.markdown("""<div class="hero"><h1>REFUGE MÉDÉRIC</h1><p>Donnez une seconde chance à ceux qui n'ont que de l'amour à offrir.</p><a href="#catalogue" class="btn-action">🐾 Voir nos animaux</a></div>""", unsafe_allow_html=True)

# --- 5. ONGLETS ---
tab1, tab_event, tab2, tab_pension, tab3, tab4, tab_urgence = st.tabs(["Le Refuge", "Actualités", "Nos Animaux", "Pension", "Nous Aider ❤️", "Contact", "🚨 Urgence"])

with tab1:
    st.markdown("<h3 style='color:#FF0000;'>📍 Notre Mission</h3>", unsafe_allow_html=True)
    st.write("L'association LES ANIMAUX DU GRAND DAX protège et soigne les animaux en détresse.")
    st.markdown("<div class='help-card-white'><h4>🐈 Projet Fourrière Chats</h4><p>Nous rénovons nos locaux félins, aidez-nous !</p></div>", unsafe_allow_html=True)

with tab_event:
    df_ev = charger_evenements_sheet()
    if not df_ev.empty:
        for i, row in df_ev.iterrows():
            st.image(get_image_data(str(row['Valeur'])), caption=row['Cle'])
    else: st.info("Aucune actualité.")

with tab2:
    st.components.v1.iframe("https://refugemedb12-fuhsesxanqbpnqkdkxkaug.streamlit.app/?embed=true", height=900)

with tab_pension:
    st.write("Pension chiens ouverte toute l'année. 15€/jour (13€ pour nos adoptés).")

with tab3:
    st.markdown("<h2 style='text-align:center;'>Comment nous aider ?</h2>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    c1.markdown("<div class='help-card-white'><h4>🕒 Temps</h4><p>Devenez bénévole pour les promenades.</p></div>", unsafe_allow_html=True)
    c2.markdown("<div class='help-card-white'><h4>📦 Nature</h4><p>Dons de croquettes et couvertures.</p></div>", unsafe_allow_html=True)

with tab4:
    st.markdown("<div class='contact-card'><h3>Contact</h3><p>📍 182 chemin Lucien Viau, Saint-Paul-lès-Dax<br>📞 05 58 73 68 82</p></div>", unsafe_allow_html=True)

with tab_urgence:
    if st.button("J'ai perdu mon animal"): modal_perdu()
    if st.button("J'ai trouvé un animal"): modal_trouve()

# --- 6. PIED DE PAGE & NEWSLETTER ---
st.markdown("---")
f1, f2, f3 = st.columns([1.5, 1, 1.5])

with f1:
    st.markdown("<h4 style='color: #FF0000;'>🐾 REFUGE MÉDÉRIC</h4>", unsafe_allow_html=True)
    st.write("Association Les Animaux du Grand Dax.")

with f2:
    st.markdown("<h4 style='color: #FF0000;'>LIENS</h4>", unsafe_allow_html=True)
    st.write("[Facebook](https://www.facebook.com/refuge.mederic)")

with f3:
    st.markdown("<h4 style='color: #FF0000;'>📧 NEWSLETTER</h4>", unsafe_allow_html=True)
    email_user = st.text_input("Votre e-mail", placeholder="votre@email.com", key="mail_input", label_visibility="collapsed")
    
    if st.button("S'inscrire 🐾"):
        if "@" in email_user and "." in email_user:
            try:
                # Tentative de connexion
                conn = st.connection("gsheets", type=GSheetsConnection)
                # On lit les données existantes
                df_existing = conn.read()
                # On ajoute le nouvel email
                new_row = pd.DataFrame({"email": [email_user]})
                df_updated = pd.concat([df_existing, new_row], ignore_index=True)
                # On renvoie tout au Google Sheet
                conn.update(data=df_updated)
                st.success("Inscrit avec succès !")
            except Exception as e:
                # Affiche l'erreur réelle pour diagnostiquer
                st.error(f"Erreur technique : {e}")
        else:
            st.error("Email invalide.")

st.markdown("<p style='text-align: center; color: #888; font-size: 0.8em;'>© 2026 Refuge Médéric</p>", unsafe_allow_html=True)
