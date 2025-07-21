import streamlit as st
from datetime import datetime
from PIL import Image
import pandas as pd
import os

from data_loader.chargement import charger_fichier_commandes, charger_conditions_fournisseur
from nettoyage.preprocess import nettoyage_donnes, nettoyer_df_paiements
from traitement.calculs import creation_df_paiements, enrichir_df_paiements, filtrer_paiements_a_venir, calculer_previsions
from filtres.sidebar import appliquer_filtres, get_fournisseurs_par_gamme, get_numerocmde_par_frn
from interface.affichage import afficher_tableau, selectionner_colonnes, afficher_suivi_statut, afficher_montant_mois, afficher_top10four
from interface.kpis import afficher_kpi_montant



st.set_page_config(
    page_title="Prévisions paiements fournisseurs",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': 'https://mon-site-aide.com',
        'Report a bug': 'https://mon-site-bugs.com',
        'About': 'Application créée par Pauline'
    }
)


aujourd_hui_str = datetime.today().strftime("%d/%m/%Y") #définir la date du jour


st.title("Prévisions des paiements fournisseurs") # Titre

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Chemin absolu vers le dossier contenant app.py
image_path = os.path.join(BASE_DIR, "assets", "logo.png") # Chemin vers l’image relatif à ce dossier
image = Image.open(image_path)
st.sidebar.image(image,  use_container_width=True)

st.sidebar.title("Filtres") # Titre filtres


# Chargement des données et conditions fournisseur
df = charger_fichier_commandes()  # Chargement fichier commandes


if df is not None:  # Si df est bien chargé, on continue
    sheet_id = "1E6jf5bBgCz_k_pY13iGoSLtd2vrQDnuV"
    sheet_name = "ALL_GAMME"
    df_cond = charger_conditions_fournisseur(sheet_id, sheet_name)

    # Nettoyage des données
    df, df_cond = nettoyage_donnes(df, df_cond)

    # Dataframe des prévisions de paiements
    df_paiements = creation_df_paiements(df)

    # Nettoyage et enrichissement df_paiements
    df_paiements = nettoyer_df_paiements(df_paiements)
    df_paiements = enrichir_df_paiements(df_paiements)

    # Appliquer les filtres du Sidebar
    gamme = st.sidebar.selectbox("Choisir une gamme", options=["Toutes"] + df_paiements["gamme"].unique().tolist())
    fournisseurs_disponibles = get_fournisseurs_par_gamme(df_paiements, gamme)
    fournisseur = st.sidebar.selectbox("Choisir un fournisseur", options=["Toutes"] + fournisseurs_disponibles)
    devise = st.sidebar.selectbox("Choisir une devise", options=["Toutes"] + df_paiements["devise"].unique().tolist())
    condition = st.sidebar.selectbox("Choisir une condition", options=["Toutes"] + df_paiements["condition"].unique().tolist())
    numcmde_disponibles = get_numerocmde_par_frn(df_paiements, fournisseur)
    numero_commande = st.sidebar.selectbox("Choisir une commande", options=["Toutes"] + numcmde_disponibles)

    df_paiements = appliquer_filtres(df_paiements, gamme, fournisseur, devise, condition, numero_commande)


    # Filtre les données à partir de la date du jour
    df_paiements = filtrer_paiements_a_venir(df_paiements)


    # Affichage des différents onglets
    tab_donnees, tab_previsions, tab_analyse = st.tabs(["📋 Données", "⏳ Prévisions", "📊 Analyse"])

   
    with tab_donnees:

         # === Slicer Date de paiement avant le tableau ===
        min_date = df_paiements["date_paiement"].dt.date.min()
        max_date = df_paiements["date_paiement"].dt.date.max()

        date_debut, date_fin = st.slider(
            "Filtrer par Date de paiement",
            min_value=min_date,
            max_value=max_date,
            value=(min_date, max_date),
            format="DD/MM/YYYY")

        # On applique le filtre
        df_paiements_filtré = df_paiements[
            (df_paiements["date_paiement"].dt.date >= date_debut) &
            (df_paiements["date_paiement"].dt.date <= date_fin)]

        #Affichage des KPI's
        col1, col2 = st.columns(2)

        with col1:
            total_usd = df_paiements_filtré["montant_usd"].sum()
            afficher_kpi_montant("Montant paiement à prévoir en Dollars", total_usd, "$")

        with col2:
            total_eur = df_paiements_filtré["montant_eur"].sum()
            afficher_kpi_montant("Montant paiement à prévoir en Euros", total_eur, "€")


        st.markdown("<hr style='border:1px solid #ccc'/>", unsafe_allow_html=True)


        # Affichage du tableau des paiements à venir    
        st.write(f"**Affichage des paiements à venir à partir du : {aujourd_hui_str}**")
        df_tableau = selectionner_colonnes(df_paiements_filtré)
        afficher_tableau(df_tableau)




    
    with tab_previsions:
        df_gamme, df_mois, df_semaine = calculer_previsions(df_paiements)

        st.subheader("📦 Prévisions par gamme")
        st.dataframe(
        df_gamme.rename(columns={
            "gamme": "Gamme",
            "montant_usd": "Montant USD",
            "montant_eur": "Montant EUR"
        }),
        use_container_width=True)

        st.subheader("🗓️ Prévisions par mois")
        st.dataframe(
        df_mois.rename(columns={
            "mois": "Mois",
            "montant_usd": "Montant USD",
            "montant_eur": "Montant EUR"
        }),
        use_container_width=True)

        st.subheader("📅 Prévisions par semaine")
        st.dataframe(
        df_semaine.rename(columns={
            "semaine": "Semaine",
            "montant_usd": "Montant USD",
            "montant_eur": "Montant EUR"
        }),
        use_container_width=True)

   
    with tab_analyse:
        st.header("Analyse des données")
        col1, col2 = st.columns([1,1])

        with col1:
            afficher_top10four(df_paiements)
        
        with col2:
            afficher_suivi_statut(df_paiements)

        afficher_montant_mois(df_paiements)
        
    

else:
    st.info("Veuillez importer un fichier pour afficher les prévisions de paiement.")

    