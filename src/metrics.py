"""
Module de calcul des indicateurs avancés d'équité et de disparités éducatives.
Calcule les indices de parité de genre, ratios urbain-rural, déperdition et scores de vulnérabilité.
"""

import os
import pandas as pd
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")
LIVRABLES_03_DIR = os.path.join(BASE_DIR, "livrables", "03_transformation")


def compute_equity_metrics(df_consolidated):
    """Calcule l'ensemble des métriques d'équité pour chaque région et chaque année."""
    df = df_consolidated.copy()

    # 1. Écart absolu de genre en points de pourcentage (Filles - Garçons)
    df["Ecart_Genre_TBS_pts"] = df["TBS_Filles"] - df["TBS_Garcons"]
    df["Ecart_Genre_TBA_pts"] = df["TBA_Filles"] - df["TBA_Garcons"]
    df["Ecart_Genre_TAP_pts"] = df["TAP_Filles"] - df["TAP_Garcons"]
    df["Ecart_Genre_CEP_pts"] = df["Taux_CEP_Filles"] - df["Taux_CEP_Garcons"]

    # 2. Taux de déperdition scolaire globale et par sexe (TBA CP1 - TAP CM2)
    # Mesure la proportion d'enfants entrés au CP1 qui n'atteignent pas la fin du primaire
    df["Deperdition_Total"] = np.maximum(0, df["TBA_Total"] - df["TAP_Total"])
    df["Deperdition_Garcons"] = np.maximum(0, df["TBA_Garcons"] - df["TAP_Garcons"])
    df["Deperdition_Filles"] = np.maximum(0, df["TBA_Filles"] - df["TAP_Filles"])
    df["Ecart_Deperdition_F_G"] = df["Deperdition_Filles"] - df["Deperdition_Garcons"]

    # 3. Qualification officielle de la parité selon les standards UNESCO
    # Parité stricte : 0.97 <= IPS <= 1.03
    def classify_ips(val):
        if pd.isna(val):
            return "Non disponible"
        if val < 0.90:
            return "Défaveur sévère des filles"
        elif val < 0.97:
            return "Défaveur modérée des filles"
        elif val <= 1.03:
            return "Parité atteinte"
        else:
            return "Défaveur des garçons"

    df["Statut_Parite_TBS"] = df["IPS_TBS"].apply(classify_ips)
    df["Statut_Parite_TAP"] = df["IPS_TAP"].apply(classify_ips)

    # 4. Score Composite de Vulnérabilité Éducative (SCVE - échelle 0 à 100)
    # Plus le score est élevé, plus la région est en situation critique d'inégalité
    # Poids : Déperdition (40%), Écart de scolarisation au TBS (30%), Faible achèvement (30%)
    tap_max = df[df["Region"] != "NATIONAL"]["TAP_Total"].max()
    tap_min = df[df["Region"] != "NATIONAL"]["TAP_Total"].min()
    tap_norm = 100 * (1 - (df["TAP_Total"] - tap_min) / (tap_max - tap_min + 1e-5))

    dep_max = df[df["Region"] != "NATIONAL"]["Deperdition_Total"].max()
    dep_norm = 100 * (df["Deperdition_Total"] / (dep_max + 1e-5))

    ips_penalty = np.where(df["IPS_TAP"] < 0.97, 100 * (0.97 - df["IPS_TAP"]) / 0.97, 0)

    df["Score_Vulnerabilite_SCVE"] = (
        0.40 * dep_norm +
        0.35 * tap_norm +
        0.25 * ips_penalty
    ).clip(0, 100).round(1)

    return df


def compute_urban_rural_metrics():
    """Calcule les indicateurs comparatifs Urbain vs Rural."""
    path_milieu = os.path.join(PROCESSED_DIR, "effectifs_primaire_milieu.csv")
    if not os.path.exists(path_milieu):
        return None

    df_milieu = pd.read_csv(path_milieu)
    pivoted = df_milieu.pivot_table(
        index=["Annee_Scolaire", "Sexe"],
        columns="Milieu",
        values="Effectif"
    ).reset_index()

    pivoted["Total_Zone"] = pivoted["Urbain"] + pivoted["Rural"]
    pivoted["Part_Rural_Pct"] = (100 * pivoted["Rural"] / pivoted["Total_Zone"]).round(1)
    pivoted["Part_Urbain_Pct"] = (100 * pivoted["Urbain"] / pivoted["Total_Zone"]).round(1)
    pivoted["Ratio_Rural_Urbain"] = (pivoted["Rural"] / pivoted["Urbain"]).round(2)

    return pivoted


def run_metrics_pipeline():
    """Génère la table complète enrichie et l'exporte pour l'analyse."""
    print("--- Calcul des métriques d'équité et de disparités ---")
    consolidated_path = os.path.join(PROCESSED_DIR, "consolide_primaire_indicateurs.csv")
    if not os.path.exists(consolidated_path):
        print("Erreur : La table consolidée n'existe pas encore.")
        return

    df_raw = pd.read_csv(consolidated_path)
    df_metrics = compute_equity_metrics(df_raw)

    out_metrics_path = os.path.join(PROCESSED_DIR, "indicateurs_equite_complets.csv")
    df_metrics.to_csv(out_metrics_path, index=False, encoding="utf-8")
    print(f"-> Table enrichie enregistrée : {out_metrics_path} ({len(df_metrics)} lignes)")

    # Export pour le livrable 03
    livrable_03_csv = os.path.join(LIVRABLES_03_DIR, "D2_03-transformation_analyst_indicateurs-equite_v1.csv")
    df_metrics.to_csv(livrable_03_csv, index=False, encoding="utf-8")
    print(f"-> Livrable Étape 03 enregistré : {livrable_03_csv}")

    df_urban_rural = compute_urban_rural_metrics()
    if df_urban_rural is not None:
        out_ur_path = os.path.join(PROCESSED_DIR, "synthese_urbain_rural.csv")
        df_urban_rural.to_csv(out_ur_path, index=False, encoding="utf-8")
        print(f"-> Synthèse Urbain vs Rural enregistrée : {out_ur_path}")

    print("--- Calcul des métriques terminé avec succès ! ---")


if __name__ == "__main__":
    run_metrics_pipeline()
