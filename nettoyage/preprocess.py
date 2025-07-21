import pandas as pd

def nettoyage_donnes(df: pd.DataFrame, df_cond: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:

    # Supprimer espaces colonnes
    df.columns = df.columns.str.strip()
    df_cond.columns = df_cond.columns.str.strip()

    # Supprimer colonnes inutiles (modification inplace)
    df.drop(columns=[
        "en_type_confie",
        "fo_ref_cli",
        "td_color_w",
        "num_fac",
        "facture",
        "en_valeur_devise",
        "num_br",
        "en_num_livraison",
        "en_mt_suppl",
        "ed_etat",
        "en_num_doc_ref",
        "en_frais_taxe",
        "en_frais_non_taxe",
        "en_acompte",
        "en_escompte",
        "en_transf_bij_psion",
        "fo_edi_type",
        "en_edi",
        "ed_code",
        "active"],
        axis=1, inplace=True)

    # Renommer colonnes
    df.rename(columns={
        'td_code': 'type_commande',
        'en_date_doc': 'date_document',
        'fo_code': 'code_fournisseur',
        'en_etat_facture': 'etat_facture',
        'en_num_doc': 'numero_document',
        'en_code': 'Inconnu',
        'en_num_ext': 'raison_commande',
        'de_code': 'devise',
        'fo_raison_soc': 'nom_fournisseur',
        'num_com': 'numero_commande',
        'etat_lib': 'etat_document',
        'en_date2': 'date_livraison',
        'en_qte_doc': 'quantites',
        'en_mt_doc': 'montant',
        'en_date_paye': 'date_depart',
        }, inplace=True)
    
    # Renommer fournisseur
    df["nom_fournisseur"] = df["nom_fournisseur"].replace({
    "VISTA KUYUMCULUK SAN. TIC. LTD": "VISTA",
    "Yiwu Bob Trading Co, LTD": "BOB",
    "YIWU LESON PACKING SHARE CO": "LESON",
    "RICCARDO ORSATO S.R.L": "RICCARDO",
    "Midas Hediyelik Esya": "MIDAS",
    "INAHVINA CO LTD": "INAH",
    "ARPAS IHRACAT ITHALAT VE PAZAR": "ARPAS",
    "RICHLINE ITALY SRL": "RICHLINE",
    "JOSE LOPEZ GARCIA S.L": "JOSE LOPEZ",
    "VEEKAY JEWELS": "VEEKAY",
    "DIVYA CREATIONS": "DIVYA",
    "The Jewelry Co.": "JEWELRY CO",
    "GALASSIA CO., LTD.": "GALASSIA",
    "MULINO D'ORO SRL": "MULINO",
    "J&G GIOIELLI CO LTD": "J&G"
})

    df_cond.rename(columns={
        'FO_CODE': 'code_fournisseur',
        }, inplace=True)

    # Conversion colonnes dates
    df["date_document"] = pd.to_datetime(df["date_document"], format="%d/%m/%Y %H:%M:%S", dayfirst=True, errors="coerce")
    df["date_livraison"] = pd.to_datetime(df["date_livraison"], format="%d/%m/%Y %H:%M:%S", dayfirst=True, errors="coerce")
    df["date_depart"] = pd.to_datetime(df["date_depart"], format="%d/%m/%Y %H:%M:%S", dayfirst=True, errors="coerce")

    # Merge conditions fournisseur
    df = df.merge(df_cond[["CONDITION DE PAIEMENTS", "code_fournisseur", "GAMME"]],
                  on="code_fournisseur", how="left")

    # Conversion montant en float
    df["montant"] = df["montant"].astype(str).str.replace(',', '.', regex=False).astype(float)
    df["montant"] = pd.to_numeric(df["montant"], errors="coerce")

    # Supprimer lignes sans condition de paiement
    df = df.dropna(subset=["CONDITION DE PAIEMENTS"])

    return df, df_cond


def nettoyer_df_paiements(df_paiements: pd.DataFrame) -> pd.DataFrame: # Supprime les lignes entièrement vides ou avec des dates manquantes
    df_paiements = df_paiements.dropna(how="all")
    df_paiements = df_paiements[df_paiements["date_paiement"].notna()]
    df_paiements = df_paiements[df_paiements["montant"].notna()]
    return df_paiements