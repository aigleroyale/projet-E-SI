# CONTRÔLES DE PARITÉ (OBLIGATOIRE)
# Parité CSV vs MySQL


import pandas as pd
from sqlalchemy import create_engine


# Connexion MySQL (SQLAlchemy)
engine = create_engine(
    "mysql+pymysql://root:Mr.41202243@localhost/data_platform",
    pool_recycle=3600
)

def check_parity(csv_path, table_name):
    csv_count = sum(1 for _ in open(csv_path)) - 1
    sql_count = pd.read_sql(
        f"SELECT COUNT(*) c FROM {table_name}",
        engine
    )["c"][0]

    print(f"{table_name} | CSV={csv_count} | DB={sql_count}")

    if csv_count != sql_count:
        raise Exception(f"Parité KO pour {table_name}")
    else:
        print("Parité OK")

check_parity("data_raw/clients.csv", "src_client")
check_parity("data_raw/factures.csv", "src_facture")
check_parity("data_raw/paiements.csv", "src_paiement")
