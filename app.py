import streamlit as st
import pandas as pd
import requests
import base64
import re
import os
import streamlit as st
from PIL import Image
from io import BytesIO


import streamlit as st

# CETTE COMMANDE DOIT ÊTRE LA PREMIÈRE
st.set_page_config(
    page_title="Médéric Connect",
    page_icon="https://raw.githubusercontent.com/Firnaeth/Site_Refuge_Med_b0.1/main/logo_officiel-2.png",
    layout="wide" # Optionnel : pour que le site prenne toute la largeur
)

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


# Fonction pour charger les événements depuis le lien spécifique
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

/* Style adaptatif pour le champ newsletter */
div[data-testid="stTextInput"] input {
    background-color: rgba(128, 128, 128, 0.1) !important; /* Fond légèrement teinté transparent */
    color: inherit !important; /* Prend la couleur du texte du thème (blanc ou noir) */
    border: 1px solid rgba(128, 128, 128, 0.2) !important;
    border-radius: 8px !important;
}

/* Force la lisibilité du texte saisi */
div[data-testid="stTextInput"] input:focus {
    border-color: #FF0000 !important; /* Bordure rouge quand on clique dedans */
}
</style>
""", unsafe_allow_html=True)

# --- HEADER COMPLET (LOGO + NOM + BANNIÈRE) ---
# --- BLOC BANNIÈRE TOUT-EN-UN (FIXÉ) ---

# On définit les liens ici pour être sûr qu'ils fonctionnent
# --- 2. RESSOURCES ---
L_LOGO = "https://raw.githubusercontent.com/Firnaeth/Site_Refuge_Med_b0.1/main/logo_officiel-2.png"
L_FOND = "https://images.unsplash.com/photo-1450778869180-41d0601e046e?auto=format&fit=crop&q=80&w=1200"

# --- 3. BANNIÈRE IDENTITY-PUSH (PC & MOBILE) ---
st.markdown(f"""
    <style>
        /* Conteneur principal */
        .header-banner {{
            background-image: url('{L_FOND}');
            background-size: cover;
            background-position: center;
            height: 400px;
            border-radius: 15px;
            position: relative;
            margin-bottom: 30px;
            box-shadow: 0 10px 20px rgba(0,0,0,0.4);
        }}

        /* Voile de contraste */
        .banner-overlay {{
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            background-color: rgba(0, 0, 0, 0.4);
            border-radius: 15px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: flex-end; 
            padding-right: 60px;
            text-align: right;
        }}

        /* Ligne Logo + Titre */
        .identity-row {{
            display: flex;
            align-items: center;
            justify-content: flex-end;
            margin-bottom: 5px;
        }}

        .banner-logo {{
            height: 97px;
            margin-right: 20px;
            background: white;
            padding: 6px;
            border-radius: 12px;
            filter: drop-shadow(2px 2px 4px rgba(0,0,0,0.3));
        }}

        .banner-title {{
            color: #FF4B4B !important; 
            font-size: 3.5em !important;
            font-weight: 800 !important;
            margin: 0 !important;
            text-shadow: 3px 3px 10px rgba(0,0,0,0.8);
            line-height: 1;
        }}

        /* Sous-titre chaleureux */
        .banner-subtitle {{
            color: white !important;
            font-size: 1.4em !important;
            font-style: italic;
            margin-top: 10px !important;
            margin-bottom: 30px !important;
            max-width: 500px;
            text-shadow: 2px 2px 5px rgba(0,0,0,1);
        }}

        /* Le Bouton Interactif */
        .btn-action {{
            background-color: #FF4B4B !important;
            color: white !important;
            padding: 15px 35px !important;
            border-radius: 50px !important;
            text-decoration: none !important;
            font-weight: bold !important;
            font-size: 1.2em !important;
            display: inline-block !important;
            border: 2px solid #FF4B4B !important;
            transition: all 0.3s ease-in-out !important;
            box-shadow: 0 4px 15px rgba(255, 75, 75, 0.4);
        }}

        /* Effet au survol (PC) */
        .btn-action:hover {{
            background-color: white !important;
            color: #FF4B4B !important;
            border: 2px solid white !important;
            transform: scale(1.05);
        }}

        /* CONFIGURATION MOBILE (SMARTPHONE) */
        @media (max-width: 600px) {{
            .banner-overlay {{
                padding-right: 0px !important;
                align-items: center !important;
                text-align: center !important;
                justify-content: center !important;
            }}
            .identity-row {{
                flex-direction: column !important;
                margin-bottom: 15px;
            }}
            .banner-logo {{
                margin-right: 0 !important;
                height: 80px !important;
            }}
            .banner-title {{
                font-size: 2.2em !important;
            }}
            .banner-subtitle {{
                font-size: 1.1em !important;
                padding: 0 20px;
            }}
        }}
    </style>

<div class="header-banner">
        <div class="banner-overlay">
            <div class="identity-row">
                <img src="{L_LOGO}" class="banner-logo">
                <h1 class="banner-title">Refuge Médéric</h1>
            </div>
            <div style="color: white; font-size: 1.5rem; font-weight: bold; margin-bottom: 10px;">
                Médéric Connect
            </div>
            <p class="banner-subtitle">"Offrez une seconde chance à ceux qui n'attendent que votre amour."</p>
            <a href="https://s8befjprptpdkcqvddw7ke.streamlit.app/" target="_blank" class="btn-action">
                🐾 Rencontrez votre nouveau meilleur ami
            </a>
        </div>
    </div>
""", unsafe_allow_html=True)

# Séparation visuelle
st.write("---")

# --- Séparation avant les onglets ---
st.write("---")

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

# --- NOUVEL ORDRE DES ONGLETS ---
tab1, tab2, tab_event, tab_pension, tab4, tab_urgence, tab3 = st.tabs(
    ["🏠 Le Refuge", "🐾 Nos Protégés", "📅 Actualités", "🏨 Pension", "📍 Contact & Accès", "🚨 Urgence/Fourrière", "Nous Aider ❤️"]
)

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

# --- BLOC RÈGLEMENT INTÉRIEUR (STYLE INFOS LÉGALES) ---
# --- LIEN DE SECOURS (GITHUB) : https://github.com/Firnaeth/Site_Refuge_Med_b0.1/blob/main/Reglement_Interieur_Animaux_Grand_Dax.pdf
        st.markdown("""
        <div style="background-color: #f8f9fa; padding: 15px; border-radius: 10px; border-left: 4px solid #6c757d; margin-top: 20px;">
            <p style="margin:0; font-size: 0.9em; color: #555;">
                📜 <b>Règlement Intérieur :</b> Pour une transparence totale, vous pouvez consulter le cadre légal de notre association. 
                <a href="https://drive.google.com/file/d/1wDSqxya8IgqCYmpL1c3Obku2Q9Vt5UNY/view?usp=sharing" target="_blank" style="color: #FF0000; font-weight: bold; text-decoration: none;">
                    Cliquez ici pour lire le PDF
                </a>
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br><h3 style='color:#FF0000;'>📢 Nos Projets & Événements</h3>", unsafe_allow_html=True)

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
    # On utilise 'event-card' pour avoir exactement le même look que les actualités
    st.markdown("<div class='event-card' style='margin-top:0;'>", unsafe_allow_html=True)
    
    st.markdown("<h3 style='text-align:center; margin-top:0; color:#FF0000;'>🙏 NOUS SOUTENIR</h3>", unsafe_allow_html=True)
    
    st.write("Votre aide est essentielle pour la survie du refuge et le bien-être de nos protégés.")

    # --- BLOC BOUTONS AVEC LOGOS OFFICIELS ---
    st.markdown("""
        <a href="https://www.helloasso.com/associations/animaux-du-grand-dax/formulaires/2" class="btn-don-vert" target="_blank" style="display: flex; align-items: center; justify-content: center; text-decoration: none; margin-bottom: 12px;">
            <img src="https://cdn.prod.website-files.com/67164cc9484c7fb65c26915e/67867c1ba9f693d5f2d43eb5_webclip.png" width="22" style="border-radius: 4px; margin-right: 12px;">
            Soutenir via HelloAsso
        </a>
        
        <a href="https://www.ouijagi.org/" class="btn-don-bleu" target="_blank" style="display: flex; align-items: center; justify-content: center; text-decoration: none;">
            <img src="https://ca-ouijagi.fr/favicon.ico" width="22" style="background: white; border-radius: 4px; padding: 2px; margin-right: 12px;">
            Soutenir via OUIJAGI!
        </a>
        
        <p style='text-align:center; font-size:0.85em; color:#666; margin-top:15px;'>
            Dons sécurisés. Reçu fiscal disponible sur les plateformes.
        </p>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style='background:#f0f2f5; padding:15px; border-radius:10px; font-size:0.9em; color:#333; margin-top:10px;'>
        <b>Appel particulier :</b> Pour les travaux de la fourrière chats, nous recherchons activement des dons de matériaux !
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
with tab2:
    st.markdown("<h2 style='text-align:center; color:#FF0000;'>NOS ANIMAUX À L'ADOPTION</h2>", unsafe_allow_html=True)
    url_catalogue = "https://s8befjprptpdkcqvddw7ke.streamlit.app/?embed=true"
    st.components.v1.iframe(url_catalogue, height=900, scrolling=True)

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
<a href="https://www.facebook.com/refuge.mederic?locale=fr_FR" class="btn-action" style="width:100%; text-align:center; display:block;">Notre page Facebook</a>
<a href="mailto:animauxdugranddax@gmail.com" class="btn-mail" style="width:100%; text-align:center; display:block;">Nous envoyer un e-mail</a>
</div>
""", unsafe_allow_html=True)
                
with c_map:
    # --- MISE À JOUR DE LA CARTE ---
    st.markdown(
        '<div style="background-color: white; padding: 15px; border-radius: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); color: black;"><h4>🗺️ Plan d\'accès</h4>',
        unsafe_allow_html=True)
    
    # Coordonnées réelles du 182 Chemin Lucien Viau
    map_coords = pd.DataFrame({'lat': [43.75835], 'lon': [-1.05776]})
    
    #  carte native (stable et robuste)
    st.map(map_coords, zoom=14, use_container_width=True)
    
    # Bouton GPS pour mobile
    st.markdown("""
        <a href="https://wego.here.com/directions/drive/mylocation/43.75835,-1.05776" target="_blank" style="text-decoration:none;">
            <div style="background-color: #FF0000; color: white; padding: 10px; border-radius: 10px; text-align: center; margin-top: 10px; font-weight: bold;">
                🚀 Lancer l'itinéraire sur HERE WeGo
            </div>
        </a>
        </div>
    """, unsafe_allow_html=True)
            
with tab_urgence:
    st.markdown("<h2 style='text-align:center; color:#FF0000;'>🚨 SERVICE DE FOURRIÈRE & URGENCE</h2>",
                unsafe_allow_html=True)

    col_btn_1, col_btn_2 = st.columns(2)
    with col_btn_1:
        if st.button("🔍 Que faire si vous avez perdu votre animal ?", use_container_width=True, type="primary"):
            modal_perdu()
    with col_btn_2:
        if st.button("🐾 Que faire si vous avez trouvé un animal errant ?", use_container_width=True):
            modal_trouve()

    st.markdown("<br>", unsafe_allow_html=True)

    col_u1, col_u2 = st.columns([1.5, 1])

    with col_u1:
        st.markdown("""
        <div class="help-card-white">
            <h4>🐕 Fonctionnement de la Fourrière</h4>
            <p>La fourrière permet d’accueillir les chiens et les chats trouvés errants sur les communes du Grand Dax.</p>
            <p style="background:#fff3f3; padding:15px; border-radius:10px; border:1px solid #ffcccc;">
                ⚠️ <b>Avertissement :</b> Nous ne nous déplaçons pas pour venir chercher un animal. L’animal doit nous être déposé par la <b>police ou les autorités compétentes</b>.
            </p>
            <p>Si vous trouvez un animal : vous devez impérativement contacter la police ou la mairie avant de nous le déposer.</p>
            <p><i>Si votre animal a disparu, il est peut-être chez nous ! N’hésitez pas à nous contacter au 05 58 73 68 82.</i></p>
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

with tab_urgence:
    # ... garde tes boutons Perdu/Trouvé en haut ...
# --- C'EST ICI QUE ÇA BUGGAIT (L'INDENTATION) ---
    st.markdown("---")
    st.markdown("<h4 style='text-align:center; color:#FF0000;'>💻 SIGNALER SUR LES PLATEFORMES NATIONALES</h4>", unsafe_allow_html=True)
    
    col_s1, col_s2, col_s3 = st.columns(3)
    
    with col_s1:
        st.markdown("""
            <a href="https://www.chien-perdu.org/fr-fr/" target="_blank" style="text-decoration:none;">
                <div style="background-color: white; padding: 15px; border-radius: 10px; border: 1px solid #ddd; text-align: center; height: 110px; display: flex; flex-direction: column; justify-content: center; align-items: center;">
                    <img src="https://www.chien-perdu.org/favicon.ico" width="25" style="margin-bottom:8px;">
                    <b style="color: #333; font-size: 0.9em;">Chien-Perdu.org</b>
                </div>
            </a>
        """, unsafe_allow_html=True)

    with col_s2:
        st.markdown("""
            <a href="https://www.chat-perdu.org/fr-fr/" target="_blank" style="text-decoration:none;">
                <div style="background-color: white; padding: 15px; border-radius: 10px; border: 1px solid #ddd; text-align: center; height: 110px; display: flex; flex-direction: column; justify-content: center; align-items: center;">
                    <img src="https://www.chat-perdu.org/favicon.ico" width="25" style="margin-bottom:8px;">
                    <b style="color: #333; font-size: 0.9em;">Chat-Perdu.org</b>
                </div>
            </a>
        """, unsafe_allow_html=True)

    with col_s3:
        st.markdown("""
            <div style="background-color: #f8f9fa; padding: 10px; border-radius: 10px; border: 1px solid #ddd; text-align: center; height: 110px; display: flex; flex-direction: column; justify-content: center; gap: 6px;">
                <b style="color: #333; font-size: 0.85em;">PET ALERT 40</b>
                <a href="https://www.petalertglobal.com/" target="_blank" style="text-decoration:none; background-color: white; color: #333; padding: 4px; border-radius: 5px; border: 1px solid #ccc; font-size: 0.8em; font-weight: bold; display: flex; align-items: center; justify-content: center;">
                    <img src="https://cdn.prod.website-files.com/63fa7acd7ca2c4dee752e5fb/6500b9f65a3fe05ee57f9311_favicon-32x32.png" width="18" style="margin-right:8px;"> Site Web
                </a>
                <a href="https://www.facebook.com/Pet.Alert.Fr.40?locale=fr_FR" target="_blank" style="text-decoration:none; background-color: #1877F2; color: white; padding: 4px; border-radius: 5px; font-size: 0.8em; font-weight: bold; display: flex; align-items: center; justify-content: center;">
                    <img src="https://upload.wikimedia.org/wikipedia/commons/b/b8/2021_Facebook_icon.svg" width="14" style="margin-right:8px;"> Facebook
                </a>
            </div>
        """, unsafe_allow_html=True)
    
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
            <p><b>• OUIJAGI! :</b> Sociétaires du Crédit Agricole, offrez-nous vos points ! C’est gratuit pour vous et précieux pour nous.</p>
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

# --- SECTION RÉCUPÉRER ---
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

    # TEXTE D'INFORMATION INSÉRÉ ICI
    st.info(
        "Le formulaire d'inscription en ligne sera bientôt intégré ici. Pour le moment, n'hésitez pas à venir nous rencontrer directement au refuge !"
    )


# --- 5. PIED DE PAGE ---
st.markdown("---")
col_f1, col_f2, col_f3, col_f4 = st.columns([1.5, 1, 1.2, 1])

with col_f1:
    st.markdown("<h4 style='color: #FF0000; margin-bottom:10px;'>🐾 REFUGE MÉDÉRIC</h4>", unsafe_allow_html=True)
    st.write("L’association Animaux du Grand Dax s’occupe de la gestion du Refuge Médéric, de sa fourrière et de sa pension avec l’aide de salariés dévoués et de bénévoles déterminés !")

with col_f2:
    st.markdown("<h4 style='color: #FF0000; margin-bottom:10px;'>PLAN DU SITE</h4>", unsafe_allow_html=True)
    st.markdown("[Accueil](#)  \n[Actualités](#)  \n[Adopter](#)  \n[Nous Aider](#)")

with col_f3:
    st.markdown("<h4 style='color: #FF0000; margin-bottom:10px;'>📧 NEWSLETTER</h4>", unsafe_allow_html=True)
    entree_texte = st.text_input("Votre e-mail", placeholder="votre@email.com", label_visibility="collapsed", key="newsletter_secret")
    
    if st.button("S'inscrire 🐾", use_container_width=True, key="btn_news_final"):
        if "password_admin" in st.secrets and entree_texte == st.secrets["password_admin"]:
            st.session_state.access_admin = True
            st.success("Accès Admin déverrouillé !")
        elif "@" in entree_texte:
            with open("liste_newsletter.txt", "a") as f:
                f.write(entree_texte + "\n")
            st.success("Enregistré !")

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

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
    <p style='text-align: center; color: #888; font-size: 0.85em; border-top: 1px solid #eee; padding-top: 20px;'>
        Développé avec passion ❤️ pour nos amis à quatre pattes, du <b>Refuge Médéric</b> - Association Animaux du Grand Dax<br>
        © 2026 Tous droits réservés. | Version Alpha_5
    </p>
""", unsafe_allow_html=True)
