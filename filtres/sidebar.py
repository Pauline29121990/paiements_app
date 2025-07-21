import streamlit as st
import pandas as pd

# Filtre sidebar
def appliquer_filtres(df_paiements, gamme, fournisseur, devise, condition,numero_commande):
    if gamme != "Toutes":
        df_paiements = df_paiements[df_paiements["gamme"] == gamme]
    if fournisseur != "Toutes":
        df_paiements = df_paiements[df_paiements["fournisseur"] == fournisseur]
    if devise != "Toutes":
        df_paiements = df_paiements[df_paiements["devise"] == devise]
    if condition != "Toutes":
        df_paiements = df_paiements[df_paiements["condition"] == condition]
    if numero_commande != "Toutes":
        df_paiements = df_paiements[df_paiements["numero_commande"] == numero_commande]
    return df_paiements

# Filtre side bar (dépendance)
def get_fournisseurs_par_gamme(df_paiements, gamme): #venir rendre dépendant le filtre frn par la gamme
    if gamme == "Toutes":
        return df_paiements["fournisseur"].unique().tolist()
    else:
        return df_paiements[df_paiements["gamme"] == gamme]["fournisseur"].unique().tolist()
    
def get_numerocmde_par_frn(df_paiements, fournisseur):
    if fournisseur == "Toutes":
        return df_paiements["numero_commande"].unique().tolist()
    else:
        return df_paiements[df_paiements["fournisseur"] == fournisseur]["numero_commande"].unique().tolist()
    
