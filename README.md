# PROJET SPECIAL E-SI
Présentation lors de l'entretien du vendredi 23/01

🎯 Objectif

Mettre en place une chaîne data complète permettant :

- Intégrer des données métiers brutes (volumineuses et parfois incohérentes)

- Controler la qualité des données

- Construire un data warehouse fiable

-  Fournir à la direction des KPI clairs et exploitables via Power BI.

## Génération des données brutes (Python)

Simuler un environnement réel (données imparfaites)

Script Python génère :
- clients
- factures
- paiements

Introduction volontaire :
- montants négatifs
- paiements incohérents
- factures non payées
- dates invalides


## Chargement des données sources (MySQL – zone source)
Stocker les données telles quelles
Tables typiques :
+ src_client
+ src_facture
+ src_paiement
Dans une base de données nommée : `data_plateform`

##  ETL avec Python (Extraction – Transformation – Load)
🔹 Extraction
Lecture MySQL / CSV via pandas + SQLAlchemy
🔹 Transformations
Normalisation des données
🔹 Load 
Insertion des données sources dans la base de données `data_plateform` selon les tables


