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

/* Boutons de don spécifiques type Facebook */
.btn-don-vert {
    background-color: #62af05; color: white !important;
    padding: 15px 25px; border-radius: 15px;
    text-decoration: none; font-weight: bold; font-size: 1.1em;
    display: block; text-align: center; margin-bottom: 15px;
    transition: 0.3s; border: none;
}
.btn-don-bleu {
    background-color: #000091; color: white !important;
    padding: 15px 25px; border-radius: 15px;
    text-decoration: none; font-weight: bold; font-size: 1.1em;
    display: block; text-align: center; margin-bottom: 15px;
    transition: 0.3s; border: none;
}
.btn-don-vert:hover, .btn-don-bleu:hover { opacity: 0.9; transform: scale(1.02); }

/* --- Style des cartes Aide (Fond Blanc / Texte Noir) --- */
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
.help-card-white h3, .help-card-white h4 { color: #FF0000 !important; margin-top:0; font-weight: bold; }
.help-card-white p, .help-card-white li { color: #1a1a1a !important; font-size: 1em; line-height: 1.5; }

/* --- Style des cartes Projets --- */
.project-card-full {
    background-color: white !important; 
    padding: 20px; 
    border-radius: 15px;
    border-left: 5px solid #FF0000; 
    margin-bottom: 20px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    color: #1a1a1a !important;
}
.project-card-full h4, .project-card-full p {
    color: #1a1a1a !important;
}

/* --- Style des cartes Événements --- */
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
.event-card h3, .event-card p {
color: #1a1a1a !important;
margin-top: 15px;
}

/* SECTION CONTACT NOIR SUR BLANC */
.contact-card {
background-color: white !important;
padding: 35px;
border-radius: 20px;
box-shadow: 0 5px 20px rgba(0,0,0,0.1);
border-left: 6px solid #FF0000;
color: #1a1a1a !important;
margin-bottom: 25px;
}
.contact-card h4, .contact-card h3 {
color: #1a1a1a !important;
margin-top: 25px;
margin-bottom: 10px;
font-weight: 800;
text-transform: uppercase;
}
.contact-card p {
color: #1a1a1a !important;
font-size: 1.15em;
line-height: 1.6;
}
.contact-sep {
border: 0;
border-top: 2px solid #eee;
margin: 20px 0;
}

/* --- NOUVEAU PIED DE PAGE --- */
.footer-container {
background-color: #1a1a1a;
color: white;
padding: 60px 20px 20px 20px;
margin-top: 80px;
font-family: 'sans-serif';
}
.footer-column h4 {
color: #FF0000;
margin-bottom: 20px;
text-transform: uppercase;
font-size: 1.1em;
letter-spacing: 1px;
}
.footer-column p, .footer-column a {
color: #bbb;
text-decoration: none;
font-size: 0.95em;
line-height: 2;
}
.footer-column a:hover { color: white; }

.social-icons a {
font-size: 24px;
margin-right: 20px;
color: white;
transition: 0.3s;
}
.social-icons a:hover { color: #FF0000; transform: scale(1.2); display: inline-block; }

.bottom-bar {
text-align: center;
border-top: 1px solid #333;
margin-top: 40px;
padding-top: 20px;
color: #666;
font-size: 0.85em;
}

/* Style spécifique pour le champ newsletter dans le footer */
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
    st.markdown("<div style='text-align:center;'><h3>📍 Localisation</h3><p>Saint-Paul-lès-Dax (40)</p></div>",
                unsafe_allow_html=True)
with col2:
    st.markdown("<div style='text-align:center;'><h3>🐕 Nos Pensionnaires</h3><p>Chiens et chats de tous ages</p></div>",
                unsafe_allow_html=True)
with col3:
    st.markdown("<div style='text-align:center;'><h3>❤️ Notre Engagement</h3><p>Soins, protection et amour</p></div>",
                unsafe_allow_html=True)

st.markdown("---")

# --- 4. SECTIONS D'INFORMATION (ONGLETS) ---
tab1, tab_event, tab2, tab_pension, tab3, tab4, tab_urgence = st.tabs(
    ["Le Refuge", "Nos Actualités", "Nos Animaux", "Pension", "Nous Aider ❤️", "Contact & Accès",
     "🚨 Urgence/Fourrière"])

with tab1:
    col_refuge_1, col_refuge_2 = st.columns([1.2, 1])

    with col_refuge_1:
        st.markdown("<h3 style='color:#FF0000;'>📍 Notre Mission & Identité</h3>", unsafe_allow_html=True)
        st.write("""
        L'association **LES ANIMAUX DU GRAND DAX** (SIREN : 993 900 000) est une structure 
        reconnue qui gère le refuge Médéric. 
        
        Notre mission principale est la protection, les soins et le placement des animaux 
        en détresse. En tant qu'acteur central de la protection animale dans le Grand Dax, 
        nous assurons la transition entre l'abandon et une nouvelle vie dans une famille aimante.
        """)
        
        st.markdown("""
        <div style="background-color: #f8f9fa; padding: 15px; border-radius: 10px; border-left: 4px solid #6c757d;">
            <p style="margin:0; font-size: 0.9em; color: #555;">
                ℹ️ <b>Informations Légales :</b> Association déclarée sous le numéro SIREN 993900000. 
                Retrouvez nos informations officielles sur l'Annuaire des Entreprises de l'État.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br><h3 style='color:#FF0000;'>🚀 Nos Projets & Événements</h3>", unsafe_allow_html=True)

        # PROJET 1 : Portes Ouvertes
        st.markdown("""
        <div class="project-card-full">
            <h4 style="margin-top:0;">📅 Journée Portes Ouvertes</h4>
            <p>Venez rencontrer nos chiens et nos chats à l’adoption, voir nos installations et découvrir nos projets pour améliorer la vie de nos compagnons à quatre pattes.<br>
            Vous rencontrerez nos salariés et nos bénévoles et, qui sait, peut-être que vous rejoindrez notre formidable équipe de passionnés !<br>
            <small><i>Petit goûter offert pour les participants.</i></small></p>
        </div>
        """, unsafe_allow_html=True)

        # PROJET 2 : Fourrière Chats
        st.markdown("""
        <div class="project-card-full">
            <h4 style="margin-top:0;">🐈 Amélioration de la Fourrière Chats</h4>
            <p>Notre fourrière réservée aux chats est dans un très mauvais état. Les animaux ne peuvent plus y être accueillis dans de bonnes conditions.<br>
            Des travaux sont prévus très prochainement pour améliorer la situation de nos amis félins. 
            <b>Mais pour cela, nous allons avoir besoin de votre aide !</b><br>
            Dons de matériaux, de temps ou d’argent, tout nous sera utile pour atteindre notre objectif.</p>
        </div>
        """, unsafe_allow_html=True)

    with col_refuge_2:
        st.markdown("<div class='contact-card' style='margin-top:0;'>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align:center; margin-top:0;'>🙏 NOUS SOUTENIR</h3>", unsafe_allow_html=True)
        st.write("Votre aide est essentielle pour la survie du refuge et le bien-être de nos protégés.")

        st.markdown("""
            <a href="https://www.helloasso.com/associations/animaux-du-grand-dax/formulaires/2" class="btn-don-vert">
                <i class="fas fa-heart"></i> Faire un don (HelloAsso)
            </a>
            <p style='text-align:center; font-size:0.9em; color:#666;'>Pour d'autres formes d'aide (temps, nature), consultez l'onglet <b>Nous Aider</b>.</p>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style='background:#f0f2f5; padding:15px; border-radius:10px; font-size:0.9em; color:#333;'>
            <b>Appel particulier :</b> Pour les travaux de la fourrière chats, nous recherchons activement des dons de matériaux ou des bras volontaires !
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
                        if img_data:
                            st.image(img_data, use_container_width=True)
                        else:
                            st.warning("Chargement de l'image...")
                        st.markdown(f"<h3>{row['Cle']}</h3></div>", unsafe_allow_html=True)
    else:
        st.info("Aucun événement n'est programmé pour le moment.")

with tab2:
    st.markdown("<h2 style='text-align:center; color:#FF0000;'>NOS ANIMAUX À L'ADOPTION</h2>", unsafe_allow_html=True)
    url_catalogue = "https://refugemedb12-fuhsesxanqbpnqkdkxkaug.streamlit.app/?embed=true"
    st.components.v1.iframe(url_catalogue, height=900, scrolling=True)

with tab_pension:
    st.markdown("<h2 style='text-align:center; color:#FF0000;'>SERVICE DE PENSION</h2>", unsafe_allow_html=True)
    col_p1, col_p2 = st.columns([1.5, 1])
    with col_p1:
        st.markdown("### 🏠 Un accueil toute l'année")
        st.write("""
        Notre pension accueille vos chiens toute l’année ! 
        Nos box sont spacieux et peuvent accueillir jusqu’à **deux gros chiens d’une même famille**.

        Ils proposent à leurs pensionnaires :
        * **Un espace détente** à l’abri des intempéries.
        * **Un dodo confortable** nettoyé tous les jours et ses gamelles.
        * **Un espace extérieur attenant** pour se dégourdir les pattes après la sieste.
        * **Une sortie quotidienne** dans un parc de détente réservé à leur attention.
        """)
    with col_p2:
        st.image("https://images.unsplash.com/photo-1516734212186-a967f81ad0d7?q=80&w=1000")

    st.markdown("### 💰 Tarifs de la Pension")
    tarifs_data = {
        "Prestation": ["1 chien", "2 chiens"],
        "Tout Public": ["15€ / jour", "23€ / jour"],
        "Chien adopté chez nous": ["13€ / jour", "20€ / jour"]
    }
    st.table(pd.DataFrame(tarifs_data))
    st.info("📞 Pour toute réservation ou renseignement, contactez-nous au 05 58 73 68 82.")

with tab3:
    st.markdown("<h2 style='text-align:center; color:#FF0000;'>NOUS AIDER</h2>", unsafe_allow_html=True)
    st.markdown(
        "<p style='text-align:center; font-size:1.1em;'>Il existe de nombreuses manières de nous aider, adaptées à chaque individu.</p><br>",
        unsafe_allow_html=True)

    col_a, col_b, col_c = st.columns(3)

    with col_a:
        st.markdown("""
        <div class="help-card-white">
            <h4>🕒 Donner de son temps</h4>
            <p>Ce dont nos pensionnaires ont le plus besoin, c’est de présence humaine.</p>
            <p>En devenant bénévole, vous aidez au nourrissage, au nettoyage, mais aussi aux promenades et aux câlins pour préparer nos protégés à leur adoption.</p>
            <p><b>Participez aussi à nos collectes</b> pour faire connaître le refuge !</p>
        </div>
        """, unsafe_allow_html=True)

    with col_b:
        st.markdown("""
        <div class="help-card-white">
            <h4>💰 Don financier</h4>
            <p><b>• HelloAsso :</b> Simple, rapide et sécurisé. Reçu fiscal automatique. Dons uniques ou mensuels.</p>
            <p><b>• Par chèque :</b> À l’ordre de <i>Animaux du Grand Dax</i>, déposé ou envoyé au refuge (182 chemin Lucien Viau).</p>
            <p><b>• Tookets :</b> Sociétaires du Crédit Agricole, offrez-nous vos points ! C’est gratuit pour vous et précieux pour nous.</p>
        </div>
        """, unsafe_allow_html=True)

    with col_c:
        st.markdown("""
        <div class="help-card-white">
            <h4>📦 Don en nature</h4>
            <p>Dans un refuge, on a toujours besoin de tout !</p>
            <ul>
                <li>Croquettes & Pâtées</li>
                <li>Couvertures & Paniers</li>
                <li>Litières & Jouets</li>
            </ul>
            <p>Si cela prend de la place chez vous, nos pensionnaires seront heureux de vous en débarrasser ! ;)</p>
        </div>
        """, unsafe_allow_html=True)

# --- LA SECTION QUE TU VOULAIS RÉCUPÉRER ---
    st.markdown("---")
    st.markdown("<h3 style='color:#FF0000; text-align:center;'>📝 Devenir Bénévole</h3>", unsafe_allow_html=True)
    
    # ZONE DE TÉLÉCHARGEMENT DU PDF
    try:
        with open("info_benevole.pdf", "rb") as f:
            pdf_bytes = f.read()
        
        st.write("Pour nous rejoindre, veuillez télécharger et lire attentivement notre dossier d'intégration :")
        st.download_button(
            label="📄 Télécharger le dossier d'intégration (PDF)",
            data=pdf_bytes,
            file_name="info_benevole.pdf",
            mime="application/pdf",
            use_container_width=True
        )
    except FileNotFoundError:
        st.warning("Le fichier 'info_benevole.pdf' n'est pas encore disponible sur le serveur.")

    # TON TEXTE D'INFORMATION RÉINSÉRÉ ICI
    st.info(
        "Le formulaire d'inscription en ligne sera bientôt intégré ici. Pour le moment, n'hésitez pas à venir nous rencontrer directement au refuge !"
    )
            
with tab4:
    st.markdown("<h2 style='text-align:center; color:#FF0000;'>INFORMATIONS & ACCÈS</h2>", unsafe_allow_html=True)
    c_info, c_map = st.columns([1, 1.2])
    with c_info:
        st.markdown("""
<div class="contact-card">
<h4>📍 ADRESSE DU REFUGE</h4>
<p>Refuge Médéric - Association Les Animaux du Grand Dax<br>
182 chemin Lucien Viau<br>
40990 Saint-Paul-lès-Dax</p>
<div class="contact-sep"></div>
<h4>⏰ HORAIRES D'OUVERTURE</h4>
<p><b>Mercredi au Dimanche : 14h00 - 18h00</b><br>
<i>(Fermé le Lundi et le Mardi)</i></p>
<div class="contact-sep"></div>
<h4>📞 NOUS CONTACTER</h4>
<p>05 58 73 68 82<br>animauxdugranddax@gmail.com</p>
<br>
<a href="https://www.facebook.com/refuge.mederic?locale=fr_FR" class="btn-action" style="width:100%; text-align:center; display:block;">Notre page Facebook 🔵</a>
<a href="mailto:animauxdugranddax@gmail.com" class="btn-mail" style="width:100%; text-align:center; display:block;">✉️ Nous envoyer un e-mail</a>
</div>
""", unsafe_allow_html=True)
                
with c_map:
    st.markdown(
        '<div style="background-color: white; padding: 15px; border-radius: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); color: black;"><h4>🗺️ Plan d\'accès</h4>',
        unsafe_allow_html=True)
    
    # --- LES COORDONNÉES EXACTES DU REFUGE ---
    # Ici, on met les vraies coordonnées du 182 Chemin Lucien Viau
    map_coords = pd.DataFrame({'lat': [43.7431], 'lon': [-1.0664]})
    
    # On utilise la carte native (elle est incassable)
    st.map(map_coords, zoom=14, use_container_width=True)
    
    # --- LE PETIT BOUTON "GPS" POUR ÊTRE SÛR ---
    st.markdown("""
        <a href="https://wego.here.com/directions/drive/mylocation/43.7431,-1.0664" target="_blank" style="text-decoration:none;">
            <div style="background-color: #FF0000; color: white; padding: 10px; border-radius: 10px; text-align: center; margin-top: 10px; font-weight: bold;">
                🚀 Lancer l'itinéraire sur HERE WeGo
            </div>
        </a>
        </div>
    """, unsafe_allow_html=True)
            
    with col_u2:
        st.markdown("""
        <div class="help-card-white">
            <h4>💰 Nos Tarifs Fourrière</h4>
            <p><b>Animal Identifié (récupéré J-0) :</b> 40€</p>
            <p><b>Animal non-identifié (récupéré J-0) :</b> 125€<br>
            <small>(40€ de prise en charge + 85€ d'identification)</small></p>
            <p><b>Prix par jour supplémentaire :</b> 15€/jour</p>
            <hr>
            <p style="font-size:0.85em;"><i>Note : L’identification est obligatoire et sera réalisée par un vétérinaire avant que l’animal ne soit rendu.</i></p>
        </div>
        """, unsafe_allow_html=True)


# --- 5. PIED DE PAGE ---
st.markdown("---")
col_f1, col_f2, col_f3, col_f4 = st.columns([1.5, 1, 1.2, 1])

with col_f1:
    st.markdown("<h4 style='color: #FF0000; margin-bottom:10px;'>🐾 REFUGE MÉDÉRIC</h4>", unsafe_allow_html=True)
    st.write("Association Les Animaux du Grand Dax. Un refuge engagé pour offrir un avenir à ceux qui n'ont plus de foyer.")

with col_f2:
    st.markdown("<h4 style='color: #FF0000; margin-bottom:10px;'>PLAN DU SITE</h4>", unsafe_allow_html=True)
    st.markdown("[Accueil](#)  \n[Actualités](#)  \n[Adopter](#)  \n[Nous Aider](#)")

with col_f3:
    st.markdown("<h4 style='color: #FF0000; margin-bottom:10px;'>📧 NEWSLETTER</h4>", unsafe_allow_html=True)
    entree_texte = st.text_input("Votre e-mail", placeholder="votre@email.com", label_visibility="collapsed", key="newsletter_secret")
    
    if st.button("S'inscrire 🐾", use_container_width=True, key="btn_news_final"):
        # --- VÉRIFICATION VIA LES SECRETS ---
        # On vérifie si ce qui est tapé correspond au secret "password_admin"
        if "password_admin" in st.secrets and entree_texte == st.secrets["password_admin"]:
            st.session_state.access_admin = True
            st.success("Accès Admin déverrouillé !")
        elif "@" in entree_texte:
            with open("liste_newsletter.txt", "a") as f:
                f.write(entree_texte + "\n")
            st.success("Enregistré !")

# --- LA ZONE ADMIN APPARAÎT SEULEMENT SI LE CODE A ÉTÉ TAPÉ ---
if st.session_state.get("access_admin", False):
    st.warning("🔓 Mode Administration activé")
    if os.path.exists("liste_newsletter.txt"):
        with open("liste_newsletter.txt", "r") as f:
            contenu = f.read()
        st.download_button("📥 Télécharger la liste", data=contenu, file_name="liste_newsletter.txt")
        st.code(contenu)
    if st.button("Quitter l'admin"):
        st.session_state.access_admin = False
        st.rerun()

with col_f4:
    st.markdown("<h4 style='color: #FF0000; margin-bottom:10px;'>CONTACT</h4>", unsafe_allow_html=True)
    st.write("📞 05 58 73 68 82")
    st.write("📍 Saint-Paul-lès-Dax")
    
    # --- RÉSEAUX SOCIAUX AVEC TEXTE À CÔTÉ ---
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

st.markdown("<br>", unsafe_allow_html=True)

# --- COPYRIGHT SIMPLE ---
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
    <p style='text-align: center; color: #888; font-size: 0.85em; border-top: 1px solid #eee; padding-top: 20px;'>
        Refuge Médéric - Association Animaux du Grand Dax<br>
        © 2026 Tous droits réservés. | Version Alpha_5
    </p>
""", unsafe_allow_html=True)
