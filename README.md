# Prévisions des paiements fournisseurs

## Description

Cette application Streamlit permet de charger un fichier de commandes fournisseurs, de nettoyer et d'enrichir les données, puis de visualiser :

* Les paiements à venir sous forme de tableau interactif
* Des indicateurs clés (montants totaux en USD/EUR)
* Des prévisions de paiement par gamme, mois et semaine
* Des analyses graphiques (top 10 des fournisseurs, suivi de statut, montants par mois et devise)

Elle intègre également des filtres (gamme, fournisseur, devise, condition, numéro de commande) pour affiner l’affichage.

## Installation

1. **Cloner le dépôt** :

   ```bash
   git clone <URL_DU_PROJET>
   cd <NOM_DU_REPERTOIRE>
   ```
2. **Créer un environnement virtuel** :

   ```bash
   python -m venv venv
   source venv/bin/activate  # sous Linux/macOS
   venv\Scripts\activate     # sous Windows
   ```
3. **Installer les dépendances** :

   ```bash
   pip install -r requirements.txt
   ```

## Structure du projet

```
├── app.py                # Point d’entrée Streamlit
├── data_loader/          # Chargement des données
│   └── chargement.py
├── nettoyage/            # Prétraitement et nettoyage
│   └── preprocess.py
├── traitement/           # Calculs des prévisions
│   └── calculs.py
├── filtres/              # Logique des filtres sidebar
│   └── sidebar.py
├── interface/            # Fonctions d’affichage (tableaux, graphiques, KPI)
│   ├── affichage.py
│   └── kpis.py
└── assets/               # Logo et ressources statiques
    └── logo.png
```

## Utilisation

```bash
streamlit run app.py
```

1. Charger un fichier CSV ou XLSX contenant les commandes fournisseurs.
2. Choisir les filtres dans la barre latérale.
3. Naviguer entre les onglets : Données, Prévisions, Analyse.

## Configuration

* Modifier le chemin d’accès au logo dans `app.py` si nécessaire.
* Spécifier l’ID et le nom de la feuille Google Sheets pour les conditions fournisseur.

## Contribuer

Les contributions sont les bienvenues ! Ouvrez une issue ou proposez un pull request.

## Licence

Ce projet est distribué sous licence MIT.
