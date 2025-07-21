import streamlit as st
import pandas as pd

def charger_fichier_commandes():
    uploader_container = st.empty()  # Créer un conteneur pour le file_uploader

    if 'file_uploaded' not in st.session_state:  # Variable pour contrôler l'affichage
        st.session_state.file_uploaded = False

    if not st.session_state.file_uploaded:   # Afficher le file_uploader seulement si aucun fichier n'a été chargé
        uploaded_file = uploader_container.file_uploader(
        "📁 Veuillez charger les commandes fournisseurs : Odeis > Achat > Séléctionner Commande fournisseur > Enlever la date > Excel (tonneau)", 
        type=["csv", "xlsx"]
    )
    else:
        uploaded_file = st.session_state.uploaded_file  # Récupérer le fichier depuis session_state

    if uploaded_file is not None:  # Sauvegarder le fichier dans session_state
        st.session_state.uploaded_file = uploaded_file
        st.session_state.file_uploaded = True
        uploader_container.empty()  # Vider le conteneur pour ne pas afficher à nouveau le file_uploader 
    
        if uploaded_file.name.endswith(".csv"):  # Lire le fichier selon son extension
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        if df.shape[1] < 35:
            st.warning("Le fichier semble vide ou mal formé.")
        else:
            st.sidebar.caption("Fichier chargé avec succès ✅")

            if  st.sidebar.button("🔄 Nouveau fichier"):  #Ajouter un bouton pour recharger un nouveau fichier
                st.session_state.file_uploaded = False
                st.session_state.uploaded_file = None
                st.rerun()
            return df  # Retourner le DataFrame chargé
        
    return None


def charger_conditions_fournisseur(sheet_id: str, sheet_name: str) -> pd.DataFrame:
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
    return pd.read_csv(url)