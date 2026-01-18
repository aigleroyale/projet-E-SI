import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker("fr_FR")
random.seed(42)
np.random.seed(42)

OUTPUT_DIR = "data_raw/"

NB_CLIENTS = 1000
NB_FACTURES = 5000
NB_PAIEMENTS = 3000

# GÉNÉRATION DES CLIENTS (clients.csv)
# secteurs mal orthographiés
# pays manquants
# dates futures
# doublons logiques possibles
def generate_clients():
    secteurs_valides = ["Santé", "Transport", "Industrie"]
    secteurs_invalides = ["SANTE", "transport ", "Industri", None]

    data = []

    for client_id in range(1, NB_CLIENTS + 1):
        secteur = random.choice(
            secteurs_valides + secteurs_invalides if random.random() < 0.1 else secteurs_valides
        )

        pays = random.choice(["FR", "DE", "ES", None]) if random.random() < 0.05 else "FR"

        date_creation = fake.date_between(start_date="-10y", end_date="+1y")

        data.append({
            "client_id": client_id,
            "nom": fake.company(),
            "secteur": secteur,
            "pays": pays,
            "date_creation": date_creation
        })

    df = pd.DataFrame(data)
    df.to_csv(f"{OUTPUT_DIR}clients.csv", index=False)

# GÉNÉRATION DES FACTURES (factures.csv)
# montants négatifs
# montants nuls
# montants aberrants
# clients inexistants
# dates future

def generate_factures():
    data = []

    for facture_id in range(1, NB_FACTURES + 1):
        client_id = (
            random.randint(1, NB_CLIENTS)
            if random.random() > 0.03
            else random.randint(NB_CLIENTS + 1, NB_CLIENTS + 5000)
        )

        montant = round(np.random.normal(2500, 4000), 2)

        if random.random() < 0.03:
            montant = -abs(montant)
        elif random.random() < 0.02:
            montant = None
        elif random.random() < 0.01:
            montant = montant * 100

        date_facture = fake.date_between(start_date="-3y", end_date="+1y")

        data.append({
            "facture_id": facture_id,
            "client_id": client_id,
            "date_facture": date_facture,
            "montant_ht": montant
        })

    df = pd.DataFrame(data)
    df.to_csv(f"{OUTPUT_DIR}factures.csv", index=False)

#GÉNÉRATION DES PAIEMENTS (paiements.csv)
def generate_paiements():
    data = []

    for paiement_id in range(1, NB_PAIEMENTS + 1):
        facture_id = (
            random.randint(1, NB_FACTURES)
            if random.random() > 0.05
            else random.randint(NB_FACTURES + 1, NB_FACTURES + 10_000)
        )

        montant_paye = round(abs(np.random.normal(2000, 3000)), 2)

        if random.random() < 0.05:
            montant_paye = montant_paye * 2

        date_paiement = fake.date_between(start_date="-2y", end_date="+1y")

        data.append({
            "paiement_id": paiement_id,
            "facture_id": facture_id,
            "date_paiement": date_paiement,
            "montant_paye": montant_paye
        })

    df = pd.DataFrame(data)
    df.to_csv(f"{OUTPUT_DIR}paiements.csv", index=False)


# LANCEMENT GLOBAL
if __name__ == "__main__":
    import os
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print("Génération des clients...")
    generate_clients()

    print("Génération des factures...")
    generate_factures()

    print("Génération des paiements...")
    generate_paiements()

    print("Données brutes générées avec succès")
