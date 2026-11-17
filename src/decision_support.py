"""
Module d'Aide à la Décision et Simulation d'Impact de Politiques Publiques (Étape 5).
Permet aux décideurs (Ministère, DREPS, Collectivités) de :
1. Simuler l'impact d'interventions ciblées (cantines scolaires, latrines filles, bourses).
2. Générer des fiches d'alerte et de décision territoriale prêtes à l'emploi.
"""

import os
import pandas as pd
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")
LIVRABLES_05_DIR = os.path.join(BASE_DIR, "livrables", "05_interpretation")
os.makedirs(LIVRABLES_05_DIR, exist_ok=True)


def simulate_impact(current_tap_f, current_tbs_f, current_ips, cantine_effort, latrine_effort, bourse_effort):
    """
    Simule l'impact d'un paquet d'interventions sur le maintien scolaire des filles.
    """
    gain_tap = (
        0.15 * (cantine_effort / 100.0) +
        0.22 * (latrine_effort / 100.0) +
        0.12 * (bourse_effort / 100.0)
    ) * (100.0 - current_tap_f)

    proj_tap_f = min(100.0, current_tap_f + gain_tap)
    proj_tbs_f = min(100.0, current_tbs_f + 0.6 * gain_tap)
    ratio_gain = proj_tap_f / (current_tap_f + 1e-5)
    proj_ips = min(1.05, current_ips * (1.0 + (gain_tap / (current_tap_f + 1e-5)) * 0.4))

    return {
        "TAP_Filles_Actuel": round(current_tap_f, 1),
        "TAP_Filles_Projete": round(proj_tap_f, 1),
        "Gain_Achèvement_pts": round(proj_tap_f - current_tap_f, 1),
        "IPS_Actuel": round(current_ips, 3),
        "IPS_Projete": round(proj_ips, 3)
    }


def generate_executive_action_plan(row):
    """Génère la fiche de synthèse décisionnelle pour une ligne de région."""
    region = row["Region"]
    tbs_t = row["TBS_Total"]
    tap_f = row["TAP_Filles"]
    tap_g = row["TAP_Garcons"]
    ips_tap = row["IPS_TAP"]
    deperdition_f = row["Deperdition_Filles"]
    vulnerabilite = row["Score_Vulnerabilite_SCVE"]

    actions = []
    if ips_tap < 0.95:
        actions.append("Priorité Urgente : Déploiement de latrines séparées et sécurisées pour filles dans les écoles rurales.")
    if deperdition_f > 30.0:
        actions.append("Rétention Scolaire : Renforcement des cantines scolaires régulières pour freiner l'abandon précoce.")
    if tbs_t < 60.0:
        actions.append("Accès & Capacité : Réouverture prioritaire des salles fermées et allocation ciblée d'enseignants.")
    if len(actions) == 0:
        actions.append("Consolidation : Maintien des acquis et renforcement de la transition vers le post-primaire.")

    return {
        "Region": region,
        "Niveau_Vulnerabilite": "Critique" if vulnerabilite > 60 else ("Modéré" if vulnerabilite > 35 else "Favorable"),
        "Score_SCVE": vulnerabilite,
        "TAP_Filles": tap_f,
        "TAP_Garcons": tap_g,
        "IPS_Achèvement": ips_tap,
        "Deperdition_Filles_pts": deperdition_f,
        "Actions_Prioritaires": actions
    }


def run_decision_pipeline():
    """Génère le livrable 05 complet avec les fiches territoriales."""
    print("--- Génération des fiches décisionnelles (Étape 05) ---")
    data_path = os.path.join(PROCESSED_DIR, "indicateurs_equite_complets.csv")
    if not os.path.exists(data_path):
        print("Erreur : Données manquantes.")
        return

    df = pd.read_csv(data_path)
    df_latest = df[(df["Annee_Scolaire"] == "2024-2025") & (df["Region"] != "NATIONAL")].sort_values("Score_Vulnerabilite_SCVE", ascending=False)

    out_md = os.path.join(LIVRABLES_05_DIR, "D2_05-interpretation_analyst_fiches-decisionnelles_v1.md")
    with open(out_md, "w", encoding="utf-8") as f:
        f.write("# Fiches Décisionnelles Territoriales par Région (Cohorte 2024-2025)\n\n")
        f.write("> **Défi 2 : Réduction des disparités d'accès et de réussite (Genre & Territoire)**\n")
        f.write("> **Outil d'aide à la décision territoriale pour les DREPS et les maires**\n\n---\n\n")

        for _, row in df_latest.iterrows():
            plan = generate_executive_action_plan(row)
            f.write(f"### Région : {plan['Region']}\n")
            f.write(f"- **Niveau de vulnérabilité :** `{plan['Niveau_Vulnerabilite']}` (Score SCVE : `{plan['Score_SCVE']}/100`)\n")
            f.write(f"- **Taux d'Achèvement Filles (TAP) :** `{plan['TAP_Filles']} %` (vs `{plan['TAP_Garcons']} %` garçons)\n")
            f.write(f"- **Indice de Parité à l'Achèvement (IPS) :** `{plan['IPS_Achèvement']}`\n")
            f.write(f"- **Taux de Déperdition Filles (CP1 ➔ CM2) :** `{plan['Deperdition_Filles_pts']} pts`\n")
            f.write("**Actions prioritaires recommandées :**\n")
            for act in plan["Actions_Prioritaires"]:
                f.write(f"  1. {act}\n")
            f.write("\n---\n\n")

    print(f"-> Fiches décisionnelles enregistrées : {out_md}")


if __name__ == "__main__":
    run_decision_pipeline()
