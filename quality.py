import pandas as pd
from sqlalchemy import create_engine

# Connexion MySQL (SQLAlchemy)
engine = create_engine(
    "mysql+pymysql://root:Mr.41202243@localhost/data_platform",
    pool_recycle=3600
)

df_client = pd.read_sql("SELECT * FROM src_client", engine)
df_facture = pd.read_sql("SELECT * FROM src_facture", engine)
df_paiement = pd.read_sql("SELECT * FROM src_paiement", engine)

#RÈGLE : CLIENT INEXISTANT
facture_sans_client = df_facture[
    ~df_facture["client_id"].isin(df_client["client_id"])
]

facture_sans_client["motif_rejet"] = "CLIENT_INEXISTANT"
facture_sans_client["date_rejet"] = pd.Timestamp.now()

facture_sans_client.to_sql(
    "dq_rejets_facture",
    engine,
    if_exists="append",
    index=False
)

# RÈGLE : MONTANT INVALIDES
facture_montant_invalide = df_facture[
    (df_facture["montant_ht"] <= 0) |
    (df_facture["montant_ht"] > 100000) |
    (df_facture["montant_ht"].isnull())
]

facture_montant_invalide["motif_rejet"] = "MONTANT_INVALID"
facture_montant_invalide["date_rejet"] = pd.Timestamp.now()

facture_montant_invalide.to_sql(
    "dq_rejets_facture",
    engine,
    if_exists="append",
    index=False
)

#CALCUL DES MÉTRIQUES
def save_metric(table, metric, value, seuil):
    statut = "OK" if value <= seuil else "KO"

    pd.DataFrame([{
        "table_name": table,
        "metric_name": metric,
        "metric_value": round(value, 2),
        "seuil": seuil,
        "statut": statut,
        "date_mesure": pd.Timestamp.now()
    }]).to_sql("dq_metrics", engine, if_exists="append", index=False)


taux_client_inexistant = len(facture_sans_client) / len(df_facture) * 100
taux_montant_invalide = len(facture_montant_invalide) / len(df_facture) * 100

save_metric("src_facture", "TAUX_CLIENT_INEXISTANT", taux_client_inexistant, 0)
save_metric("src_facture", "TAUX_MONTANT_INVALID", taux_montant_invalide, 1)

# ÉTAPE 6 – STAGING (DONNÉES EXPLOITABLES)
# Données cohérentes, standardisées, jointables

