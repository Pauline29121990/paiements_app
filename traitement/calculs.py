import pandas as pd
import streamlit as st
from datetime import datetime

# === Construire un nouveau dataframe de prévisions === #

def creation_df_paiements(df: pd.DataFrame) -> pd.DataFrame:
    paiements = []

    for index, row in df.iterrows():
        fournisseur = row["nom_fournisseur"]
        condition = row["CONDITION DE PAIEMENTS"]
        montant_total = row["montant"]
        date_commande = row["date_document"]
        date_livraison = row["date_livraison"]
        numero_commande = row["numero_commande"]
        devise = row['devise']
        gamme = row['GAMME']
        code_four = row['code_fournisseur']
        raison = row['raison_commande']
        

        
        condition = str(condition).strip().upper()

        if condition == "60J":
            date_paiement = date_livraison + pd.Timedelta(days=60)
            paiements.append({
                "index_commande": index,
                "numero_commande": numero_commande,
                "date_paiement": date_paiement,
                "montant": montant_total,
                "condition": condition,
                "devise": devise,
                "fournisseur": fournisseur,
                "gamme": gamme,
                "code_fournisseur": code_four,
                "raison_commande": raison,
                "date_commande":date_commande
            })

        elif condition == "J30":
            date_paiement = date_livraison + pd.Timedelta(days=30)
            paiements.append({
                "index_commande": index,
                "numero_commande": numero_commande,
                "date_paiement": date_paiement,
                "montant": montant_total,
                "condition": condition,
                "devise": devise,
                "fournisseur": fournisseur,
                "gamme": gamme,
                "code_fournisseur": code_four,
                "raison_commande": raison,
                "date_commande":date_commande
            })

        elif condition == "AVANT EXPEDITION":
            date_paiement = date_livraison
            paiements.append({
                "index_commande": index,
                "numero_commande": numero_commande,
                "date_paiement": date_paiement,
                "montant": montant_total,
                "condition": condition,
                "devise": devise,
                "fournisseur": fournisseur,
                "gamme": gamme,
                "code_fournisseur": code_four,
                "raison_commande": raison,
                "date_commande":date_commande
            })

        elif condition in ["30% DEPOSIT 70% J60", "DEPOSIT 30% + J+60"]:
            montant_deposit = montant_total * 0.30
            montant_restant = montant_total - montant_deposit

            paiements.append({
                "index_commande": index,
                "numero_commande": numero_commande,
                "date_paiement": date_commande,
                "montant": montant_deposit,
                "condition": condition,
                "devise": devise,
                "fournisseur": fournisseur,
                "gamme": gamme,
                "code_fournisseur": code_four,
                "raison_commande": raison,
                "date_commande":date_commande
            })

            date_solde = date_commande + pd.Timedelta(days=60)
            paiements.append({
                "index_commande": index,
                "numero_commande": numero_commande,
                "date_paiement": date_solde,
                "montant": montant_restant,
                "condition": condition,
                "devise": devise,
                "fournisseur": fournisseur,
                "gamme": gamme,
                "code_fournisseur": code_four,
                "raison_commande": raison,
                "date_commande":date_commande
            })

        elif condition in ["30 %COMMANDE 70 %LIVRAISON", "30% COMMANDE 70% LIVRAISON"]:
            montant_deposit = montant_total * 0.30
            montant_restant = montant_total - montant_deposit

            paiements.append({
                "index_commande": index,
                "numero_commande": numero_commande,
                "date_paiement": date_commande,
                "montant": montant_deposit,
                "condition": condition,
                "devise": devise,
                "fournisseur": fournisseur,
                "gamme": gamme,
                "code_fournisseur": code_four,
                "raison_commande": raison,
                "date_commande":date_commande
            })

            date_solde = date_livraison
            paiements.append({
                "index_commande": index,
                "numero_commande": numero_commande,
                "date_paiement": date_solde,
                "montant": montant_restant,
                "condition": condition,
                "devise": devise,
                "fournisseur": fournisseur,
                "gamme": gamme,
                "code_fournisseur": code_four,
                "raison_commande": raison,
                "date_commande":date_commande
            })

        else:
            st.warning(f"❗ Condition non gérée : '{condition}' à l'index {index}")

    df_paiements = pd.DataFrame(paiements) # Création du nouveau DataFrame avec les lignes de paiement
    return df_paiements

# Ajouter des colonnes pour enrichir le DataFrame des paiements
def enrichir_df_paiements(df_paiements: pd.DataFrame) -> pd.DataFrame:
        # On crée les deux colonnes montant_eur et montant_usd en fonction de la devise
    df_paiements["montant_eur"] = df_paiements.apply(lambda row: row["montant"] if row["devise"] == "E" else 0, axis=1)
    df_paiements["montant_usd"] = df_paiements.apply(lambda row: row["montant"] if row["devise"] == "$" else 0, axis=1)

    #Convertir la colonne date de paiement en format date 
    df_paiements["date_paiement"] = pd.to_datetime(df_paiements["date_paiement"], errors="coerce")
    df_paiements['date_paiement_formatee'] = df_paiements['date_paiement'].dt.strftime('%d/%m/%Y')
    df_paiements["date_commande"] = pd.to_datetime(df_paiements["date_commande"], errors="coerce").dt.strftime("%d/%m/%Y")

    #Convertir les dates en semaines et en mois
    df_paiements["semaine"] = df_paiements["date_paiement"].dt.to_period('W').astype(str)
    df_paiements["mois"] = df_paiements["date_paiement"].dt.to_period('M').astype(str)


    #Ajouter une colonne Gamme2 (test) à partir de la raison commande
    df_paiements["Gamme2"] = df_paiements.apply(
    lambda x: "PIQUE" if "PK" in str(x["raison_commande"]) 
    else "OR" if "OR" in str(x["raison_commande"]) 
    else "HSI" if "HSI" in str(x["raison_commande"]) 
    else x["gamme"],
    axis=1
)

    return df_paiements


# Afficher uniquement les paiements à partir de la date du jour
def filtrer_paiements_a_venir(df_paiements, colonne_date="date_paiement"):
    df_paiements[colonne_date] = pd.to_datetime(df_paiements[colonne_date]) # S'assurer que la colonne est bien en datetime
    aujourd_hui = pd.to_datetime(datetime.today().date()) # Filtrer à partir d'aujourd'hui inclus
    df_filtre = df_paiements[df_paiements[colonne_date] >= aujourd_hui]
    return df_filtre

# Calculer les prévisions de paiements par gamme, mois et semaine dans l'onglet Prévisions
def calculer_previsions(df_paiements: pd.DataFrame):
    df_gamme = df_paiements.groupby("gamme")[["montant_usd", "montant_eur"]].sum().reset_index()
    for col in ["montant_usd", "montant_eur"]:
        df_gamme[col] = df_gamme[col].apply(lambda x: f"{x:,.0f}".replace(",", " "))
    df_mois = df_paiements.groupby("mois")[["montant_usd", "montant_eur"]].sum().reset_index()
    for col in ["montant_usd", "montant_eur"]:
        df_mois[col] = df_mois[col].apply(lambda x: f"{x:,.0f}".replace(",", " "))
    df_semaine = df_paiements.groupby("semaine")[["montant_usd", "montant_eur"]].sum().reset_index()
    for col in ["montant_usd", "montant_eur"]:
        df_semaine[col] = df_semaine[col].apply(lambda x: f"{x:,.0f}".replace(",", " "))
    return df_gamme, df_mois, df_semaine