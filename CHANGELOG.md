# 📝 Notes de Version (Changelog)

## [vAlpha_5] - 24 Avril 2026
### ✨ Ajouté
- **Nouvelle Bannière Identity-Push** : Fusion complète du logo, du titre et de l'appel à l'action dans une bannière visuelle unifiée à droite.
  - Bouton CTA "Coup de Cœur" : Intégration d'un bouton d'action chaleureux ("Rencontrez votre nouveau meilleur ami") avec redirection vers le catalogue.
  - Protection Visuelle du Logo : Ajout d'un cadre protecteur blanc (border-radius) et d'une ombre portée pour garantir la visibilité du logo sur fonds complexes.
- **Effets CSS Dynamiques** : Mise en place d'animations au survol (hover scale) sur les boutons pour une interface plus vivante.

⚡ Optimisé
- **Lisibilité Textuelle** : Application d'un voile de contraste (overlay) de 40% et de text-shadow sur l'ensemble de la bannière pour une lecture parfaite.
- **Harmonie des Couleurs** : Alignement du titre sur le rouge officiel Streamlit (#FF4B4B) pour une intégration native.
- **Équilibre Visuel** : Redimensionnement du logo à 97px pour un ratio titre/image optimal.

🔧 Corrigé
- **Bug d'affichage HTML** : Correction de l'interprétation des balises via l'activation de unsafe_allow_html=True.
- **Alignement Responsive** : Fixation de la disposition flex-column pour éviter le chevauchement du texte sur les petits écrans.

## [v0.05] - Avril 2026
### ✨ Ajouté
- **Sécurité des Documents** : Mise en place d'une double sauvegarde (Redondance) pour le Règlement Intérieur.
  - Lien  Google Drive : Utilisé pour la rapidité et la stabilité sur le site.
  - Lien GitHub : Conservé en secours en cas de panne ou de maintenance.
- **Règlement Intérieur** : Intégration du PDF officiel avec un design cohérent (cadre gris à liseré) pour plus de transparence.
- **Système Anti-Veille** : Configuration de deux moniteurs UptimeRobot (intervalle 15 min) pour garantir que le site reste éveillé 24h/24.
- **Boutons de soutien officiels** : Intégration de HelloAsso et OuiJ'agis avec logos.
- **Cartes d'urgence** : Restructuration de l'onglet Fourrière pour une meilleure lisibilité.
- **Documentation** : Création du README et du Changelog pour GitHub.

### ⚡ Optimisé
- **Temps de reconnexion** : Ajout du système de cache (@st.cache_data) pour accélérer le chargement des images et des événements.

### 🔧 Corrigé
- **Erreurs d'indentation** : Correction des bugs Python qui bloquaient l'affichage de l'onglet Urgence.
- **Design Responsive** : Alignement des icônes dans les boutons d'action.

## [v0.02] - Avril 2026
- Mise en place du catalogue d'adoption via Iframe.
- Ajout de la carte interactive du refuge.
- Création du système de newsletter avec accès Admin.

## [v0.01] - Mars 2026
- Lancement de la version Alpha du site.
