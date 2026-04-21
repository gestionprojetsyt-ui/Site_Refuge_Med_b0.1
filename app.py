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


# Fonction pour récupérer l'image réelle (données binaires) avec simulation de navigateur
@st.cache_data(ttl=600)
def get_image_data(url):
    try:
        if not isinstance(url, str) or 'drive.google.com' not in url:
            return None
        file_id = re.search(r'(?:id=|[/\b])([a-zA-Z0-9_-]{25,})', url).group(1)
        direct_url = f'https://drive.google.com/uc?export=download&id={file_id}'
        # Ajout du User-Agent pour éviter les blocages Google Drive
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        response = requests.get(direct_url, headers=headers, timeout=10)
        if response.status_code == 200:
            return BytesIO(response.content)
    except Exception:
        return None
    return None


# Fonction pour charger les événements depuis ton lien spécifique
@st.cache_data(ttl=300)
def charger_evenements_sheet():
    URL_EV = "https://docs.google.com/spreadsheets/d/1XZXKwCfJ_922HAkAANzpXyyZL97uJzcu84viFWdtgpA/export?format=csv&gid=1825198513"
    try:
        df = pd.read_csv(URL_EV)
        df.columns = df.columns.str.strip()
        # Inversion pour avoir les plus récents en premier
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
    Cherchez sous les lits, dans les placards, sous les meubles de cuisine... **si la tête passe, tout passe !** Une fois l’intérieur retourné, faites le tour du jardin, vérifiez sous les haies, dans les arbres et même sous les voitures ou dans le moteur.

    ### 👃 2. Sortez sa litière (pour les chats)
    Astuce étrange mais efficace : ne lavez pas la litière. Les odeurs peuvent voyager suffisamment loin pour guider votre compagnon vers sa maison.

    ### 🗣️ 3. Appelez-le en début de soirée
    Appelez surtout en fin de journée (moins de bruit). N’hésitez pas à crier fort et à agiter une boîte de croquettes.

    ### 🏘️ 4. Faites le tour du quartier
    Tapez aux portes, laissez des mots dans les boîtes aux lettres avec une photo. Pensez à vérifier les garages des voisins où un animal curieux a pu se faire enfermer.

    ### 💻 5. Contactez les sites spécialisés
    * **I-CAD :** Déclarez la perte (gratuit).
    * **Pet Alert 40 / Chat-perdu.org / Chien-perdu.org**

    ### 📞 6. Appelez les autorités
    Fourrière en priorité, puis le refuge, les mairies et les vétérinaires alentours.

    ---
    ### ✨ Les bons gestes à l'avenir
    * **Identification :** Obligatoire, elle offre 75% de chances en plus de retrouver votre animal.
    * **Stérilisation :** Calme les envies d'évasion et de fugues.
    * **Sécurité :** Gardez votre chat à l'intérieur la nuit et ne sortez pas les nouveaux arrivants trop tôt.
    """)


@st.dialog("🐾 Que faire si vous avez trouvé un animal errant ?", width="large")
def modal_trouve():
    st.markdown("""
    *Publié par animauxdugranddax le 1 janvier 2026*

    ⚠️ **Rappel important :** Nous ne sommes pas habilités à nous déplacer. L'animal doit nous être déposé par la police ou les autorités compétentes après accord de la mairie.

    ### 🚫 1. Ne prenez pas l'animal chez vous si vous n'en voulez pas
    Vous pourriez vous mettre en danger ou vous retrouver coincé si la fourrière est pleine. Laissez-le dehors mais nourrissez-le à heures fixes pour qu'il reste sur le secteur.

    ### 🏘️ 2. Faites le tour du quartier
    Toquez aux portes ou laissez un mot. Les chiens fugueurs sont souvent connus des voisins immédiats.

    ### 💻 3. Vérifiez les sites spécialisés
    Cherchez s'il est déclaré perdu sur **Pet Alert 40**, **Chat-perdu.org** ou **Chien-perdu.org**.

    ### 🏥 4. Amenez-le chez un vétérinaire (Gratuit)
    Si l'animal est docile, tout vétérinaire peut vérifier gratuitement et sans rendez-vous si l'animal possède une puce électronique.

    ### 🚨 5. Contactez les autorités pour la fourrière
    C’est le dernier recours. Vous devez impérativement passer par la **mairie ou la police** pour obtenir l'autorisation de nous amener l'animal.
    """)


st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.main { background-color: #fdfdfd; }

.hero {
background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)),
url('https://images.unsplash.com/photo-1548199973-03cce0bbc87b?q=80&w=2000');
background-size: cover;
background-position: center;
padding: 100px 20px;
text-align: center;
color: white;
border-radius: 0 0 50px 50px;
margin-bottom: 50px;
}

.btn-action {
background-color: #FF0000;
color: white !important;
padding: 15px 30px;
border-radius: 30px;
text-decoration: none;
font-weight: bold;
font-size: 1.2em;
display: inline-block;
}

.btn-don-vert {
    background-color: #62af05; color: white !important;
    padding: 15px 25px; border-radius: 15px;
    text-decoration: none; font-weight: bold; font-size: 1.1em;
    display: block; text-align: center; margin-bottom: 15px;
    transition: 0.3s;
}
.btn-don-bleu {
    background-color: #000091; color: white !important;
    padding: 15px 25px; border-radius: 15px;
    text-decoration: none; font-weight: bold; font-size: 1.1em;
    display: block; text-align: center; margin-bottom: 15px;
    transition: 0.3s;
}

.help-card-white {
    background-color: white !important; 
    padding: 25px; 
    border-radius: 15px;
    border-left: 5px solid #FF0000; 
    margin-bottom: 20px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    color: #1a1a1a !important;
}

.contact-card {
background-color: white !important;
padding: 35px;
border-radius: 20px;
box-shadow: 0 5px 20px rgba(0,0,0,0.1);
border-left: 6px solid #FF0000;
color: #1a1a1a !important;
margin-bottom: 25px;
}

.event-card {
background-color: white !important;
padding: 20px;
border-radius: 15px;
border-bottom: 5px solid #FF0000;
box-shadow: 0 4px 15px rgba(0,0,0,0.05);
margin-bottom: 20px;
text-align: center;
color: #1a1a1a !important;
}

/* STYLE ADAPTATIF NEWSLETTER */
div[data-testid="stTextInput"] input {
    background-color: #262626 !important;
    color: white !important;
    border: 1px solid #444 !important;
}
</style>
""", unsafe_allow_html=True)

# --- 2. HERO ---
st.markdown("""
<div class="hero">
<h1 style="font-size: 4em; margin-bottom: 10px; color: white;">REFUGE MÉDÉRIC</h1>
<p style="font-size: 1.5em; margin-bottom: 30px; color: white;">Donnez une seconde chance à ceux qui n'ont que de l'amour à offrir.</p>
<a href="#catalogue" class="btn-action">🐾 Voir nos animaux à l'adoption</a>
</div>
""", unsafe_allow_html=True)

# --- 3. PRÉSENTATION ---
col1, col2, col3 = st.columns(3)
with col1: st.markdown("<div style='text-align:center;'><h3>📍 Localisation</h3><p>Saint-Paul-lès-Dax (40)</p></div>", unsafe_allow_html=True)
with col2: st.markdown("<div style='text-align:center;'><h3>🐕 Nos Pensionnaires</h3><p>Chiens et chats de tous âges</p></div>", unsafe_allow_html=True)
with col3: st.markdown("<div style='text-align:center;'><h3>❤️ Notre Engagement</h3><p>Soins, protection et amour</p></div>", unsafe_allow_html=True)

st.markdown("---")

# --- 4. ONGLETS ---
tab1, tab_event, tab2, tab_pension, tab3, tab4, tab_urgence = st.tabs(
    ["Le Refuge", "Nos Actualités", "Nos Animaux", "Pension", "Nous Aider ❤️", "Contact & Accès", "🚨 Urgence/Fourrière"])

with tab1:
    col_refuge_1, col_refuge_2 = st.columns([1.2, 1])
    with col_refuge_1:
        st.markdown("<h3 style='color:#FF0000;'>📍 Notre Mission</h3>", unsafe_allow_html=True)
        st.write("L'association LES ANIMAUX DU GRAND DAX gère le refuge Médéric. Nous assurons la protection, les soins et le placement des animaux en détresse.")
        st.markdown("<br><h3 style='color:#FF0000;'>🚀 Nos Projets</h3>", unsafe_allow_html=True)
        st.markdown('<div class="help-card-white"><h4>📅 Portes Ouvertes</h4><p>Venez rencontrer nos équipes et nos protégés lors de nos événements annuels.</p></div>', unsafe_allow_html=True)
        st.markdown('<div class="help-card-white"><h4>🐈 Fourrière Chats</h4><p>Travaux de rénovation prévus pour améliorer l\'accueil des félins.</p></div>', unsafe_allow_html=True)
    
    with col_refuge_2:
        st.markdown("<div class='contact-card' style='margin-top:0;'>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align:center; margin-top:0;'>🙏 NOUS SOUTENIR</h3>", unsafe_allow_html=True)
        st.markdown("""
            <a href="https://www.helloasso.com/associations/animaux-du-grand-dax/formulaires/2" target="_blank" class="btn-don-vert">❤️ Faire un don (HelloAsso)</a>
            <a href="https://www.tookets.com/associations/association-les-animaux-du-grand-dax" target="_blank" class="btn-don-bleu">💰 Nous offrir vos Tookets</a>
            <div style='background:#f0f2f5; padding:15px; border-radius:10px; font-size:0.9em; color:#333; border-left: 4px solid #000091;'>
            <b>Appel :</b> Nous recherchons des dons de matériaux pour la fourrière chats !
            </div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

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
                        st.markdown(f'<div class="event-card">', unsafe_allow_html=True)
                        img_data = get_image_data(str(row['Valeur']))
                        if img_data: st.image(img_data, use_container_width=True)
                        st.markdown(f"<h3>{row['Cle']}</h3></div>", unsafe_allow_html=True)

with tab2:
    st.components.v1.iframe("https://refugemedb12-fuhsesxanqbpnqkdkxkaug.streamlit.app/?embed=true", height=900, scrolling=True)

with tab_pension:
    st.markdown("<h2 style='text-align:center; color:#FF0000;'>SERVICE DE PENSION</h2>", unsafe_allow_html=True)
    col_p1, col_p2 = st.columns([1.5, 1])
    with col_p1:
        st.write("Box spacieux avec espace extérieur. Accueil toute l'année.")
        tarifs_p = {"Prestation": ["1 chien", "2 chiens"], "Tarif": ["15€ / jour", "23€ / jour"]}
        st.table(pd.DataFrame(tarifs_p))
    with col_p2:
        st.info("📞 Réservation : 05 58 73 68 82")

with tab3:
    st.markdown("<h2 style='text-align:center; color:#FF0000;'>NOUS AIDER</h2>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1: st.markdown('<div class="help-card-white"><h4>🕒 Temps</h4><p>Bénévolat pour les promenades et les soins.</p></div>', unsafe_allow_html=True)
    with c2: st.markdown('<div class="help-card-white"><h4>💰 Argent</h4><p>Dons financiers (HelloAsso, Tookets).</p></div>', unsafe_allow_html=True)
    with c3: st.markdown('<div class="help-card-white"><h4>📦 Nature</h4><p>Croquettes, litière, couvertures.</p></div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("<h3 style='color:#FF0000; text-align:center;'>📝 Devenir Bénévole</h3>", unsafe_allow_html=True)
    try:
        with open("info_benevole.pdf", "rb") as f:
            pdf_bytes = f.read()
        st.download_button("📄 Télécharger le dossier d'intégration (PDF)", pdf_bytes, "info_benevole.pdf", "application/pdf", use_container_width=True)
    except:
        st.warning("Dossier PDF non disponible sur le serveur.")

with tab4:
    st.markdown("<h2 style='text-align:center; color:#FF0000;'>CONTACT & ACCÈS</h2>", unsafe_allow_html=True)
    c_info, c_map = st.columns([1, 1.2])
    with c_info:
        st.markdown("<div class='contact-card'><h4>📍 ADRESSE</h4><p>182 chemin Lucien Viau, 40990 Saint-Paul-lès-Dax</p><h4>⏰ HORAIRES</h4><p>Mer. au Dim. : 14h - 18h</p><h4>📞 CONTACT</h4><p>05 58 73 68 82</p></div>", unsafe_allow_html=True)
    with c_map:
        st.map(pd.DataFrame({'lat': [43.7431], 'lon': [-1.0664]}), zoom=14)

with tab_urgence:
    st.markdown("<h2 style='text-align:center; color:#FF0000;'>🚨 URGENCE & FOURRIÈRE</h2>", unsafe_allow_html=True)
    col_u1, col_u2 = st.columns([1, 1])
    with col_u1:
        if st.button("🔍 J'AI PERDU MON ANIMAL", use_container_width=True): modal_perdu()
        if st.button("🐾 J'AI TROUVÉ UN ANIMAL", use_container_width=True): modal_trouve()
    with col_u2:
        st.markdown("""
        <div class="help-card-white">
            <h4>💰 Nos Tarifs Fourrière</h4>
            <p><b>Animal Identifié (récupéré J-0) :</b> 40€</p>
            <p><b>Animal non-identifié (récupéré J-0) :</b> 125€<br>
            <small>(40€ de prise en charge + 85€ d'identification)</small></p>
            <p><b>Prix par jour supplémentaire :</b> 15€/jour</p>
            <hr>
            <p style="font-size:0.85em;"><i>Note : L’identification est obligatoire avant toute restitution.</i></p>
        </div>
        """, unsafe_allow_html=True)

# --- 5. PIED DE PAGE ---
st.markdown("---")
col_f1, col_f2, col_f3, col_f4 = st.columns([1.5, 1, 1.2, 1])

with col_f1:
    st.markdown("<h4 style='color: #FF0000;'>🐾 REFUGE MÉDÉRIC</h4>", unsafe_allow_html=True)
    st.write("Association Les Animaux du Grand Dax.")

with col_f2:
    st.markdown("<h4 style='color: #FF0000;'>PLAN DU SITE</h4>", unsafe_allow_html=True)
    st.markdown("[Accueil](#)  \n[Actualités](#)  \n[Adopter](#)  \n[Nous Aider](#)")

with col_f3:
    st.markdown("<h4 style='color: #FF0000;'>📧 NEWSLETTER</h4>", unsafe_allow_html=True)
    email = st.text_input("Email", placeholder="votre@email.com", label_visibility="collapsed", key="news_in")
    if st.button("S'inscrire 🐾", use_container_width=True):
        if "password_admin" in st.secrets and email == st.secrets["password_admin"]:
            st.session_state.access_admin = True
            st.rerun()
        else: st.success("Enregistré !")

if st.session_state.get("access_admin", False):
    st.warning("🔓 Mode Admin")
    if st.button("Quitter"): st.session_state.access_admin = False; st.rerun()

with col_f4:
    st.markdown("<h4 style='color: #FF0000;'>CONTACT</h4>", unsafe_allow_html=True)
    st.markdown("""
        <div style="margin-top: 10px;">
            <a href="https://www.facebook.com/refuge.mederic" target="_blank" style="text-decoration:none; color:inherit; display:flex; align-items:center; margin-bottom:12px;">
                <img src="https://upload.wikimedia.org/wikipedia/commons/b/b8/2021_Facebook_icon.svg" width="20" style="margin-right:10px;"> Facebook
            </a>
            <a href="https://www.instagram.com/refuge_mederic/" target="_blank" style="text-decoration:none; color:inherit; display:flex; align-items:center; margin-bottom:12px;">
                <img src="https://upload.wikimedia.org/wikipedia/commons/e/e7/Instagram_logo_2016.svg" width="20" style="margin-right:10px;"> Instagram
            </a>
            <a href="mailto:refuge.mederic@gmail.com" style="text-decoration:none; color:inherit; display:flex; align-items:center;">
                <img src="https://upload.wikimedia.org/wikipedia/commons/7/7e/Gmail_icon_%282020%29.svg" width="20" style="margin-right:10px;"> Gmail
            </a>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<p style='text-align:center; color:#888; font-size:0.8em; margin-top:50px;'>© 2026 Refuge Médéric | Saint-Paul-lès-Dax | Alpha_5</p>", unsafe_allow_html=True)
