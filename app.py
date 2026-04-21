import streamlit as st
import pandas as pd
import requests
import re
import os
import base64
from PIL import Image
from io import BytesIO

# --- 1. CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="Refuge Médéric - Officiel",
    layout="wide",
    page_icon="🐾",
    initial_sidebar_state="collapsed"
)

# --- 2. FONCTIONS TECHNIQUES ---

@st.cache_data(ttl=600)
def get_image_data(url):
    """Récupère l'image depuis Google Drive avec contournement des blocages."""
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
    """Charge les actualités depuis le Google Sheet spécifié."""
    URL_EV = "https://docs.google.com/spreadsheets/d/1XZXKwCfJ_922HAkAANzpXyyZL97uJzcu84viFWdtgpA/export?format=csv&gid=1825198513"
    try:
        df = pd.read_csv(URL_EV)
        df.columns = df.columns.str.strip()
        return df.iloc[::-1].reset_index(drop=True)
    except:
        return pd.DataFrame()

# --- 3. MODALES (DIALOGS) ---

@st.dialog("🔍 Que faire si vous avez perdu votre animal ?", width="large")
def modal_perdu():
    st.markdown("""
    ### 🏠 1. Fouillez CHEZ VOUS
    Cherchez partout : placards, sous les lits, garages. Si la tête passe, le chat passe !
    ### 🗣️ 2. Appelez-le en début de soirée
    Le calme aide l'animal à vous entendre. Secouez une boîte de croquettes.
    ### 💻 3. Déclarez la perte
    * **I-CAD** (Fichier National)
    * **Pet Alert 40** et **Chat-perdu.org**
    """)

@st.dialog("🐾 Que faire si vous avez trouvé un animal ?", width="large")
def modal_trouve():
    st.markdown("""
    ### 🏥 1. Vérifiez l'identification
    Amenez-le chez un vétérinaire (gratuit) pour vérifier s'il est pucé.
    ### 🚨 2. Contactez la mairie ou la police
    **Important :** Le refuge n'est pas habilité à récupérer les animaux directement sur la voie publique. Vous devez obtenir l'accord des autorités.
    """)

# --- 4. STYLE CSS ÉPURÉ (SANS BOXES) ---
st.markdown("""
<style>
/* Masquage des éléments Streamlit */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Global */
.stApp { background-color: #ffffff; }

/* Hero Section */
.hero {
    background: linear-gradient(rgba(0,0,0,0.4), rgba(0,0,0,0.4)),
    url('https://images.unsplash.com/photo-1548199973-03cce0bbc87b?q=80&w=2000');
    background-size: cover; background-position: center;
    padding: 120px 20px; text-align: center; color: white;
    border-radius: 0 0 40px 40px; margin-bottom: 40px;
}

.hero h1 { font-size: 4.5em; font-weight: 800; margin-bottom: 10px; }

/* Boutons */
.btn-action {
    background-color: #FF0000; color: white !important;
    padding: 15px 35px; border-radius: 50px; text-decoration: none;
    font-weight: bold; font-size: 1.2em; transition: 0.3s; display: inline-block;
}

.btn-don-vert {
    background-color: #62af05; color: white !important;
    padding: 18px; border-radius: 12px; text-decoration: none;
    font-weight: bold; font-size: 1.1em; display: block; text-align: center; margin-bottom: 12px;
}

.btn-don-bleu {
    background-color: #000091; color: white !important;
    padding: 18px; border-radius: 12px; text-decoration: none;
    font-weight: bold; font-size: 1.1em; display: block; text-align: center; margin-bottom: 12px;
}

/* Texte & Titres */
h3 { color: #FF0000 !important; font-weight: 700 !important; }
.info-text { font-size: 1.1em; line-height: 1.6; color: #333; }

/* Footer Custom */
.footer-text { text-align: center; color: #888; font-size: 0.9em; padding: 40px 0; border-top: 1px solid #eee; }
</style>
""", unsafe_allow_html=True)

# --- 5. STRUCTURE DU SITE ---

# Banner
st.markdown("""
<div class="hero">
    <h1>REFUGE MÉDÉRIC</h1>
    <p style="font-size: 1.5em;">Une seconde chance pour nos amis à quatre pattes</p><br>
    <a href="#catalogue" class="btn-action">🐾 Consulter les Adoptions</a>
</div>
""", unsafe_allow_html=True)

# Navigation
tabs = st.tabs(["Le Refuge", "Actualités", "Nos Animaux", "Pension", "Nous Aider", "Contact", "🚨 Urgence"])

# --- ONGLET 1 : LE REFUGE ---
with tabs[0]:
    col1, col2 = st.columns([1.5, 1])
    with col1:
        st.markdown("### 📍 Notre Mission")
        st.markdown("""
        L'association **LES ANIMAUX DU GRAND DAX** gère le refuge Médéric à Saint-Paul-lès-Dax. 
        Depuis des années, nous nous battons pour offrir soins, sécurité et amour aux chiens et chats abandonnés.
        
        **Nos engagements :**
        * Accueil et soins vétérinaires.
        * Socialisation des animaux traumatisés.
        * Accompagnement rigoureux des familles adoptantes.
        """)
        
        st.markdown("### 🚀 Projets prioritaires")
        st.write("**• Rénovation de la fourrière chat :** Nos locaux félins ont besoin d'une remise à neuf urgente pour garantir le confort des pensionnaires.")
        st.write("**• Journées Portes Ouvertes :** Des moments d'échange réguliers pour sensibiliser à la cause animale.")
        
    with col2:
        st.markdown("<h3 style='text-align:center;'>❤️ Soutenir l'Action</h3>", unsafe_allow_html=True)
        st.markdown("""
            <a href="https://www.helloasso.com/associations/animaux-du-grand-dax/formulaires/2" class="btn-don-vert" target="_blank">
                FAIRE UN DON (HELLOASSO)
            </a>
            <a href="https://www.ouijagi.com/refuge-mederic" class="btn-don-bleu" target="_blank">
                SOUTENIR VIA OUIJAGI
            </a>
        """, unsafe_allow_html=True)
        st.info("📢 Actuellement : Nous recherchons des dons de matériaux (grillage, peinture, bois) pour nos travaux.")

# --- ONGLET 2 : ACTUALITÉS ---
with tabs[1]:
    st.markdown("<h2 style='text-align:center;'>Dernières Nouvelles</h2>", unsafe_allow_html=True)
    df_ev = charger_evenements_sheet()
    if not df_ev.empty:
        for i in range(0, len(df_ev), 2):
            cols = st.columns(2)
            for j in range(2):
                if i + j < len(df_ev):
                    row = df_ev.iloc[i + j]
                    with cols[j]:
                        img = get_image_data(str(row['Valeur']))
                        if img: st.image(img, use_container_width=True)
                        st.markdown(f"<p style='text-align:center; font-weight:bold;'>{row['Cle']}</p>", unsafe_allow_html=True)
    else:
        st.write("Aucune actualité récente.")

# --- ONGLET 3 : NOS ANIMAUX ---
with tabs[2]:
    st.markdown("<div id='catalogue'></div>", unsafe_allow_html=True)
    st.components.v1.iframe("https://refugemedb12-fuhsesxanqbpnqkdkxkaug.streamlit.app/?embed=true", height=900, scrolling=True)

# --- ONGLET 4 : PENSION ---
with tabs[3]:
    st.markdown("### 🏠 Votre chien en vacances chez nous")
    st.write("Le refuge propose un service de pension canine pour financer ses actions de sauvetage.")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
        **Inclus dans le séjour :**
        * Box individuel nettoyé quotidiennement.
        * Parcs de détente pour les sorties.
        * Alimentation de qualité adaptée.
        * Surveillance et soins par des professionnels.
        """)
    with c2:
        tarifs = {
            "Type": ["1 Chien", "2 Chiens (même famille)", "Chien adopté au refuge"],
            "Prix/Jour": ["15 €", "23 €", "13 €"]
        }
        st.table(pd.DataFrame(tarifs))

# --- ONGLET 5 : NOUS AIDER ---
with tabs[4]:
    st.markdown("### Comment agir ?")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.write("**Bénévolat**")
        st.write("Promener les chiens, brosser les chats, aider au nettoyage ou aux collectes alimentaires.")
    with c2:
        st.write("**Dons en Nature**")
        st.write("Croquettes, litière, produits d'entretien, couvertures et paniers propres.")
    with c3:
        st.write("**Dons Financiers**")
        st.write("Déductibles d'impôts à hauteur de 66%.")
    
    st.markdown("---")
    st.write("📄 **Devenir Bénévole :** Téléchargez notre dossier d'accueil.")
    st.button("Télécharger le PDF d'intégration", disabled=True)

# --- ONGLET 6 : CONTACT ---
with tabs[5]:
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### 📞 Coordonnées")
        st.write("📍 182 chemin Lucien Viau, 40990 St-Paul-lès-Dax")
        st.write("📞 05 58 73 68 82")
        st.write("✉️ animauxdugranddax@gmail.com")
        st.markdown("### ⏰ Horaires")
        st.write("Du Mercredi au Dimanche : 14h00 - 18h00")
        st.write("*(Fermé Lundi et Mardi)*")
    with c2:
        st.markdown("### 🗺️ Nous trouver")
        map_data = pd.DataFrame({'lat': [43.7431], 'lon': [-1.0664]})
        st.map(map_data)

# --- ONGLET 7 : URGENCE ---
with tabs[6]:
    st.error("🚨 LIRE ATTENTIVEMENT AVANT TOUTE DÉMARCHE")
    st.write("Le refuge n'est pas un service d'urgence 24h/24. Pour les animaux errants, la loi impose de passer par les autorités.")
    colu1, colu2 = st.columns(2)
    with colu1:
        if st.button("🔍 J'AI PERDU MON ANIMAL", use_container_width=True, type="primary"):
            modal_perdu()
    with colu2:
        if st.button("🐾 J'AI TROUVÉ UN ANIMAL", use_container_width=True):
            modal_trouve()

# --- 6. FOOTER & NEWSLETTER ---
st.markdown("<br><br>", unsafe_allow_html=True)
f_col1, f_col2, f_col3 = st.columns([1, 1, 1])

with f_col1:
    st.markdown("### 🐾 Réseaux Sociaux")
    st.write("[Facebook](https://www.facebook.com/refuge.mederic)")
    st.write("[Instagram](https://www.instagram.com/refuge_mederic/)")

with f_col2:
    st.markdown("### 📧 Newsletter")
    mail = st.text_input("Saisissez votre e-mail", key="news", label_visibility="collapsed")
    if st.button("S'inscrire"):
        if "@" in mail:
            st.success("Merci pour votre inscription !")
            # Logique de sauvegarde optionnelle ici
        else:
            st.error("E-mail invalide.")

with f_col3:
    st.markdown("### 🏠 Le Refuge")
    st.write("Association Les Animaux du Grand Dax")
    st.write("Siret : 993 900 000")

st.markdown("""
<div class="footer-text">
    © 2026 Refuge Médéric - Association Les Animaux du Grand Dax | Réalisé avec passion pour nos protégés.
</div>
""", unsafe_allow_html=True)

# --- FIN DU CODE ---
