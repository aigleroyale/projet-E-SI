import pandas as pd
from sqlalchemy import create_engine

# Connexion MySQL (SQLAlchemy)
engine = create_engine(
    "mysql+pymysql://root:Mr.41202243@localhost/data_platform",
    pool_recycle=3600
)

# Chargement des données clients dans la table src_client
df_clients = pd.read_csv("data_raw/clients.csv")

df_clients.to_sql(
    "src_client",
    engine,
    if_exists="append",
    index=False,
    chunksize=10000
)

# Chargement des données factures dans la table src_facture
df_factures = pd.read_csv("data_raw/factures.csv")

df_factures.to_sql(
    "src_facture",
    engine,
    if_exists="append",
    index=False,
    chunksize=20000
)

# Chargement des données paiements dans la table src_paiement
df_paiements = pd.read_csv("data_raw/paiements.csv")

df_paiements.to_sql(
    "src_paiement",
    engine,
    if_exists="append",
    index=False,
    chunksize=20000
)

print("Données chargées avec succès dans la base de données MySQL")


