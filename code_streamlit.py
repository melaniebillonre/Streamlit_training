import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_authenticator import Authenticate

CSV_FILE = 'users.csv'

# --- 1. Configuration des Comptes ---
try:
    df = pd.read_csv(CSV_FILE)
    
    usernames_dict = {}
    for index, row in df.iterrows():
        username_key = row['username']
        usernames_dict[username_key] = {
            'name': row['username'], 
            'password': row['password'],
            'email': row['email'],
            'failed_login_attemps': int(row['failed_login_attempts']), 
            'logged_in': str(row['logged_in']).lower() == 'true', 
            'role': row['role']
        }
        
    lesDonneesDesComptes = {'usernames': usernames_dict}
    
except FileNotFoundError:
    st.error(f"Erreur : Le fichier '{CSV_FILE}' est introuvable. Veuillez vérifier le chemin.")
    st.stop()
except KeyError as e:
    st.error(f"Erreur de colonne : Le fichier CSV doit contenir une colonne nommée '{e}'.")
    st.stop()
except Exception as e:
    st.error(f"Une erreur inattendue est survenue lors de la lecture du CSV: {e}")
    st.stop()

authenticator = Authenticate(
    lesDonneesDesComptes,
    "cookie name",
    "cookie key",
    30,
)

# --- 2. Fonctions pour le Contenu des Pages ---

def page_accueil_publique():
    """Contenu de la page 'Accueil' du menu de navigation."""
    st.title("Bienvenue sur la page d'accueil ! 👋")
    st.image("https://png.pngtree.com/thumb_back/fh260/background/20231221/pngtree-white-and-black-long-haired-cat-photo-image_15555008.png")

def page_photos():
    st.title(":smile_cat: Trouvez le chat qui représente votre émotion du moment :pouting_cat: ")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Heureux")
        st.image("https://static.cdnbridge.com/resources/18/160536/picture/10/85521936.jpg")
    with col2:
        st.header("Triste")
        st.image("https://www.shutterstock.com/image-photo/one-striped-sad-cat-green-600nw-2197555377.jpg")
    with col3: 
        st.header("Fâché")
        st.image("https://media.istockphoto.com/id/1310147575/photo/angry-cat-with-unhappy-expression-lying-on-the-windowsill-of-the-house.jpg?s=612x612&w=0&k=20&c=m6d1Pds3vvl5RvO2I1dkaaG9kMoUKTxaBXP2mbZoCrU=")

# --- 3. Affichage du Formulaire de Connexion ---
authenticator.login(
    fields={'Form name': 'Connexion', 'Username': 'Nom d\'utilisateur', 'Password': 'Mot de passe'}
)

st.text("Tester avec utilisateur et utilisateurMDP")

# On récupère les états depuis st.session_state
authentication_status = st.session_state.get("authentication_status")
name = st.session_state.get("name") 
username = st.session_state.get("username") 


# --- 4. Affichage après authentification ---

if authentication_status:
    with st.sidebar:
        selection = option_menu(
            menu_title=None,
            options=["Accueil", "Photos"],
        )
        authenticator.logout("Déconnexion", "sidebar") 
    
    # B. Affichage du Contenu Principal en fonction de la sélection
    if selection == "Accueil":
        page_accueil_publique()
    elif selection == "Photos":
        page_photos()
        
elif authentication_status is False:
    st.error("L'username ou le password est/sont incorrect")
    
elif authentication_status is None:
    st.warning('Veuillez entrer votre nom d\'utilisateur et mot de passe')
