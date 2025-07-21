import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta



# Dataframe
def afficher_tableau(df): 
    df_sorted = df.sort_values("date_paiement", ascending=True) # Trier par date du plus ancien au plus récent (colonne "date_paiement" reste colonne normale)
    df_sorted["montant"] = df_sorted["montant"].apply(lambda x: f"{x:,.0f}".replace(",", " "))
    df_sorted["mois"] = pd.to_datetime(df_sorted["mois"], format="%Y-%m").dt.strftime("%B-%Y").str.capitalize() # Renommer valeur colonne mois
    df_sorted = renommer_colonnes_affichage(df_sorted)
    styled_df = df_sorted.style.set_properties(**{'text-align': 'center'})\
                                .set_table_styles([{'selector': 'th', 'props': [('text-align', 'center')]}]) # Appliquer le style centré (colonnes et en-têtes)
    st.dataframe(styled_df, use_container_width=True, height=600) # Afficher dans Streamlit avec scrolling et largeur dynamique

# Mettre les colonnes dans l'ordre dans le DF du premier onglet
def selectionner_colonnes(df_paiements):
    colonnes = [
        "date_commande",
        "date_paiement_formatee",
        "mois",
        "gamme",
        "Gamme2",
        "code_fournisseur",
        "fournisseur",
        "montant",
        "devise",
        "numero_commande",
        "raison_commande",
        "condition",
        "date_paiement"
    ]
    return df_paiements[colonnes]

# Renommer mes colonnes du DF du premier onglet
def renommer_colonnes_affichage(df):
    return df.rename(columns={
        "date_paiement_formatee": "Date de paiement",
        "mois": "Mois",
        "gamme": "Gamme",
        "code_fournisseur": "Code fournisseur",
        "fournisseur": "Fournisseur",
        "montant": "Montant",
        "devise": "Devise",
        "numero_commande": "Commande n°",
        "raison_commande": "Raison de commande",
        "condition": "Condition de paiement",
        "date_paiement": "Date brute",
        "date_commande": "Date Commande"
    })


# Etablir les différents graphique dans l'onglet Analyse

# 1. Graphique du top 10 fournisseur 
def afficher_top10four(df_paiements):
    top_frn = df_paiements.groupby("fournisseur")["montant"].sum().sort_values(ascending=True).head(10).reset_index()

    fig1 = px.bar(
            top_frn,
            x="montant",
            y="fournisseur",
            color="fournisseur",
            color_discrete_sequence=px.colors.qualitative.Set2,
            orientation="h",
            title="Top 10 des fournisseurs par montant à payer",
            labels={"montant": "Montant", "fournisseur": "Fournisseur"},
            text_auto=".0f"
        )

    fig1.update_layout(showlegend=False, yaxis_title=None)
    st.plotly_chart(fig1, use_container_width=True)



# 2. Montant par mois
def afficher_montant_mois(df_paiements):
    df_par_mois = df_paiements.groupby(["mois", "devise"])["montant"].sum().reset_index()
    fig2 = px.bar(
                df_par_mois,
                x="mois",
                y="montant",
                color="devise",
                title="Montant total des paiements par gamme et devise",
                barmode="group",
                text_auto=".0f"
            ) 
    fig2.update_layout(showlegend=True)  
    st.plotly_chart(fig2, use_container_width=True)

# 3. : Suivi des statuts
def afficher_suivi_statut(df_paiements):
    aujourd_hui = pd.to_datetime(datetime.today().date())

    df_paiements["statut"] = df_paiements["date_paiement"].apply(
        lambda d: "En retard" if d < aujourd_hui else
                  "Échéance < 7j" if d <= aujourd_hui + timedelta(days=7) else
                  "À venir"
    )

    statut_df = df_paiements["statut"].value_counts().reset_index()
    statut_df.columns = ["statut", "nombre"]

    fig = px.pie(
        statut_df,
        names="statut",
        values="nombre",
        color="statut",
        color_discrete_map={
            "En retard": "#661021",  
            "Échéance < 7j": "#cc708a",
            "À venir": "#70a0cc"
        },
        title="Statut des paiements",
        hole=0.4
        
    )
    st.plotly_chart(fig, use_container_width=True)


