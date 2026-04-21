import streamlit as st
import pandas as pd
import requests
import base64
import re
from PIL import Image
from io import BytesIO

# --- 1. CONFIGURATION & STYLE ---
st.set_page_config(page_title="Refuge Médéric - Officiel", layout="wide", page_icon="🐾")

# Importation des icônes pour le pied de page
st.markdown('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">',
            unsafe_allow_html=True)


# Fonction pour récupérer l'image réelle (données binaires) pour contourner les blocages
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

/* Style du Header Hero */
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
transition: 0.3s;
display: inline-block;
margin-bottom: 10px;
}

.btn-mail {
background-color: #333333;
color: white !important;
padding: 15px 30px;
border-radius: 30px;
text-decoration: none;
font-weight: bold;
font-size: 1.2em;
transition: 0.3s;
display: inline-block;
}

/* Boutons de don */
.btn-don-vert {
    background-color: #62af05; color: white !important;
    padding: 15px 25px; border-radius: 15px;
    text-decoration: none; font-weight: bold; font-size: 1.1em;
    display: block; text-align: center; margin-bottom: 15px;
    transition: 0.3s; border: none;
}
.btn-don-vert:hover { opacity: 0.9; transform: scale(1.02); }

/* --- Style des cartes Aide --- */
.help-card-white {
    background-color: white !important; 
    padding: 25px; 
    border-radius: 15px;
    border-left: 5px solid #FF0000; 
    margin-bottom: 20px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    color: #1a1a1a !important;
    height: 100%;
}
.help-card-white h4 { color: #FF0000 !important; margin-top:0; font-weight: bold; }

.project-card-full {
    background-color: white !important; 
    padding: 20px; 
    border-radius: 15px;
    border-left: 5px solid #FF0000; 
    margin-bottom: 20px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    color: #1a1a1a !important;
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

.contact-card {
background-color: white !important;
padding: 35px;
border-radius: 20px;
box-shadow: 0 5px 20px rgba(0,0,0,0.1);
border-left: 6px solid #FF0000;
color: #1a1a1a !important;
margin-bottom: 25px;
}

div[data-testid="stTextInput"] input {
    background-color: #262626 !important;
    color: white !important;
    border: 1px solid #444 !important;
}
</style>
""", unsafe_allow_html=True)

# --- 2. BANNIÈRE D'ACCUEIL ---
st.markdown("""
<div class="hero">
<h1 style="font-size: 4em; margin-bottom: 10px; color: white;">REFUGE MÉDÉRIC</h1>
<p style="font-size: 1.5em; margin-bottom: 30px; color: white;">Donnez une seconde chance à ceux qui n'ont que de l'amour à offrir.</p>
<a href="#catalogue" class="btn-action">🐾 Voir nos animaux à l'adoption</a>
</div>
""", unsafe_allow_html=True)

# --- 3. PRÉSENTATION RAPIDE ---
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("<div style='text-align:center;'><h3>📍 Localisation</h3><p>Saint-Paul-lès-Dax (40)</p></div>", unsafe_allow_html=True)
with col2:
    st.markdown("<div style='text-align:center;'><h3>🐕 Nos Pensionnaires</h3><p>Chiens et chats de tous ages</p></div>", unsafe_allow_html=True)
with col3:
    st.markdown("<div style='text-align:center;'><h3>❤️ Notre Engagement</h3><p>Soins, protection et amour</p></div>", unsafe_allow_html=True)

st.markdown("---")

# --- 4. SECTIONS D'INFORMATION (ONGLETS) ---
tab1, tab_event, tab2, tab_pension, tab3, tab4, tab_urgence = st.tabs(
    ["Le Refuge", "Nos Actualités", "Nos Animaux", "Pension", "Nous Aider ❤️", "Contact & Accès", "🚨 Urgence/Fourrière"])

with tab1:
    col_refuge_1, col_refuge_2 = st.columns([1.2, 1])
    with col_refuge_1:
        st.markdown("<h3 style='color:#FF0000;'>📍 Notre Mission & Identité</h3>", unsafe_allow_html=True)
        st.write("""
        L'association **LES ANIMAUX DU GRAND DAX** (SIREN : 993 900 000) est une structure 
        reconnue qui gère le refuge Médéric. Notre mission principale est la protection, 
        les soins et le placement des animaux en détresse.
        """)
        
        st.markdown("<br><h3 style='color:#FF0000;'>🚀 Nos Projets & Événements</h3>", unsafe_allow_html=True)
        st.markdown("""<div class="project-card-full"><h4>📅 Journée Portes Ouvertes</h4><p>Venez rencontrer nos chiens et nos chats à l’adoption !</p></div>""", unsafe_allow_html=True)

    with col_refuge_2:
        st.markdown("<div class='contact-card' style='margin-top:0;'>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align:center; margin-top:0;'>🙏 NOUS SOUTENIR</h3>", unsafe_allow_html=True)
        st.markdown('<a href="https://www.helloasso.com/associations/animaux-du-grand-dax/formulaires/2" class="btn-don-vert">Faire un don (HelloAsso)</a>', unsafe_allow_html=True)
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
                        st.markdown('<div class="event-card">', unsafe_allow_html=True)
                        img_data = get_image_data(str(row['Valeur']))
                        if img_data: st.image(img_data, use_container_width=True)
                        st.markdown(f"<h3>{row['Cle']}</h3></div>", unsafe_allow_html=True)

with tab2:
    st.markdown("<h2 style='text-align:center; color:#FF0000;'>NOS ANIMAUX À L'ADOPTION</h2>", unsafe_allow_html=True)
    url_catalogue = "https://refugemedb12-fuhsesxanqbpnqkdkxkaug.streamlit.app/?embed=true"
    st.components.v1.iframe(url_catalogue, height=900, scrolling=True)

with tab_pension:
    st.markdown("<h2 style='text-align:center; color:#FF0000;'>SERVICE DE PENSION</h2>", unsafe_allow_html=True)
    col_p1, col_p2 = st.columns([1.5, 1])
    with col_p1:
        st.write("Notre pension accueille vos chiens toute l’année dans des box spacieux.")
    with col_p2:
        st.image("https://images.unsplash.com/photo-1516734212186-a967f81ad0d7?q=80&w=1000")
    tarifs_data = {"Prestation": ["1 chien", "2 chiens"], "Tout Public": ["15€ / jour", "23€ / jour"], "Chien adopté chez nous": ["13€ / jour", "20€ / jour"]}
    st.table(pd.DataFrame(tarifs_data))

with tab3: # --- SECTION NOUS AIDER / BÉNÉVOLAT ---
    st.markdown("<h2 style='text-align:center; color:#FF0000;'>NOUS AIDER</h2>", unsafe_allow_html=True)
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.markdown('<div class="help-card-white"><h4>🕒 Donner du temps</h4><p>Aidez au nourrissage, au nettoyage et aux balades.</p></div>', unsafe_allow_html=True)
    with col_b:
        st.markdown('<div class="help-card-white"><h4>💰 Don financier</h4><p>Soutenez-nous via HelloAsso, chèque ou Tookets.</p></div>', unsafe_allow_html=True)
    with col_c:
        st.markdown('<div class="help-card-white"><h4>📦 Don en nature</h4><p>Croquettes, litières, paniers et couvertures sont bienvenus.</p></div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("<h3 style='color:#FF0000; text-align:center;'>📝 Devenir Bénévole</h3>", unsafe_allow_html=True)
    
    # --- BLOC DE TÉLÉCHARGEMENT ---
    try:
        with open("info_benevole.pdf", "rb") as f:
            pdf_bytes = f.read()
        
        st.write("Pour devenir bénévole, veuillez prendre connaissance de notre dossier d'intégration ci-dessous :")
        st.download_button(
            label="📄 Télécharger le dossier d'intégration (PDF)",
            data=pdf_bytes,
            file_name="info_benevole.pdf",
            mime="application/pdf",
            use_container_width=True
        )
    except FileNotFoundError:
        st.warning("Le fichier 'info_benevole.pdf' n'a pas été trouvé. Assurez-vous qu'il est bien présent à la racine de votre projet.")

    st.info("Le formulaire d'inscription en ligne sera bientôt intégré ici. Pour le moment, n'hésitez pas à venir nous rencontrer !")

with tab4:
    st.markdown("<h2 style='text-align:center; color:#FF0000;'>INFORMATIONS & ACCÈS</h2>", unsafe_allow_html=True)
    c_info, c_map = st.columns([1, 1.2])
    with c_info:
        st.markdown('<div class="contact-card"><h4>📍 ADRESSE</h4><p>182 chemin Lucien Viau, 40990 Saint-Paul-lès-Dax</p><h4>⏰ HORAIRES</h4><p>Mer. au Dim. : 14h - 18h</p><h4>📞 CONTACT</h4><p>05 58 73 68 82</p></div>', unsafe_allow_html=True)
    with c_map:
        map_coords = pd.DataFrame({'lat': [43.72594], 'lon': [-1.05030]})
        st.map(map_coords, zoom=14)

with tab_urgence:
    st.markdown("<h2 style='text-align:center; color:#FF0000;'>🚨 SERVICE DE FOURRIÈRE</h2>", unsafe_allow_html=True)
    if st.button("🔍 J'ai perdu mon animal", use_container_width=True, type="primary"): modal_perdu()
    if st.button("🐾 J'ai trouvé un animal errant", use_container_width=True): modal_trouve()

# --- 5. PIED DE PAGE ---
st.markdown("---")
col_f1, col_f2, col_f3, col_f4 = st.columns([1.5, 1, 1.2, 1])
with col_f1:
    st.markdown("<h4 style='color: #FF0000;'>🐾 REFUGE MÉDÉRIC</h4>", unsafe_allow_html=True)
    st.write("Association Les Animaux du Grand Dax.")
with col_f3:
    st.text_input("Newsletter", placeholder="votre@email.com", key="mail_footer")
    if st.button("S'inscrire"): st.success("Merci !")
with col_f4:
    st.markdown("📞 05 58 73 68 82")

st.markdown("<p style='text-align: center; color: #888; font-size: 0.85em;'>© 2026 Tous droits réservés.</p>", unsafe_allow_html=True)
