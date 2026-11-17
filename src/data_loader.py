"""
Module de chargement et de prétraitement des données de l'éducation (DGESS / MENAPLN).
Structure les tables officielles brutes (2015/2016 à 2024/2025) en jeux de données nettoyés.
"""

import os
import re
import pandas as pd
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DATA_PATH = os.path.join(BASE_DIR, "data", "raw", "donnees_officielles_brutes.csv")
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")
LIVRABLES_02_DIR = os.path.join(BASE_DIR, "livrables", "02_nettoyage")
LIVRABLES_03_DIR = os.path.join(BASE_DIR, "livrables", "03_transformation")

os.makedirs(PROCESSED_DIR, exist_ok=True)
os.makedirs(LIVRABLES_02_DIR, exist_ok=True)
os.makedirs(LIVRABLES_03_DIR, exist_ok=True)


def normalize_region_name(name):
    """Normalise rigoureusement la toponymie des 13 régions et de la référence nationale."""
    if not isinstance(name, str):
        return name
    n = name.strip().upper()
    if n in ["BURKINA FASO", "BURKINA", "TOTAL GENERAL", "TOTAL", "NATIONAL"]:
        return "NATIONAL"
    if n in ["HAUT-BASSINS", "HAUTS-BASSINS", "HAUTS BASSINS", "HAUT BASSINS"]:
        return "HAUTS-BASSINS"
    if n in ["BOUCLE DU MOUHOUN", "BOUCLE-DU-MOUHOUN"]:
        return "BOUCLE DU MOUHOUN"
    return n


def clean_num(val):
    """Convertit une chaîne en flottant ou entier propre."""
    if pd.isna(val):
        return np.nan
    s = str(val).strip().replace(" ", "").replace("\xa0", "")
    if s == "" or s.lower() == "nan" or s == "-":
        return np.nan
    try:
        return float(s)
    except ValueError:
        return np.nan


def parse_raw_blocks(file_path):
    """Découpe le fichier brut en blocs de tableaux distincts."""
    with open(file_path, "r", encoding="utf-8") as f:
        lines = [line.rstrip("\r\n") for line in f]

    blocks = []
    current_title = None
    current_lines = []

    for line in lines:
        if line.strip().startswith("Tableau ") or line.strip().startswith('"Tableau '):
            if current_title and current_lines:
                blocks.append((current_title, current_lines))
            current_title = line.strip().strip('"').split(",,,")[0].strip()
            current_lines = []
        else:
            if current_title is not None:
                current_lines.append(line)

    if current_title and current_lines:
        blocks.append((current_title, current_lines))

    return blocks


def extract_primary_effectifs_region(lines):
    """Extrait Tableau 1 Primaire : Effectifs par région et par sexe."""
    records = []
    years = ["2015-2016", "2016-2017", "2017-2018", "2018-2019", "2019-2020",
             "2020-2021", "2021-2022", "2022-2023", "2023-2024", "2024-2025"]
    
    current_region = None
    for line in lines:
        parts = [p.strip().strip('"') for p in line.split(",")]
        if len(parts) < 12:
            continue
        region_col, sexe_col = parts[0], parts[1]
        if region_col != "" and region_col.upper() != "REGION":
            current_region = normalize_region_name(region_col)
        
        if sexe_col.upper() in ["GARCONS", "FILLES", "TOTAL"] and current_region:
            sexe = "Garçons" if "GAR" in sexe_col.upper() else ("Filles" if "FIL" in sexe_col.upper() else "Total")
            for idx, year in enumerate(years):
                val = clean_num(parts[2 + idx])
                records.append({
                    "Region": current_region,
                    "Sexe": sexe,
                    "Annee_Scolaire": year,
                    "Effectif": val
                })
    return pd.DataFrame(records)


def extract_primary_milieu(lines):
    """Extrait Tableau 3 Primaire : Urbain vs Rural."""
    records = []
    years = ["2015-2016", "2016-2017", "2017-2018", "2018-2019", "2019-2020",
             "2020-2021", "2021-2022", "2022-2023", "2023-2024", "2024-2025"]
    current_milieu = None
    for line in lines:
        parts = [p.strip().strip('"') for p in line.split(",")]
        if len(parts) < 12:
            continue
        milieu_col, sexe_col = parts[0], parts[1]
        if milieu_col != "" and milieu_col.upper() not in ["MILIEU"]:
            current_milieu = milieu_col.strip()
        if sexe_col.upper() in ["GARCONS", "FILLES", "TOTAL"] and current_milieu:
            sexe = "Garçons" if "GAR" in sexe_col.upper() else ("Filles" if "FIL" in sexe_col.upper() else "Total")
            for idx, year in enumerate(years):
                val = clean_num(parts[2 + idx])
                records.append({
                    "Milieu": current_milieu.title(),
                    "Sexe": sexe,
                    "Annee_Scolaire": year,
                    "Effectif": val
                })
    return pd.DataFrame(records)


def extract_primary_rates(lines, indicator_name):
    """Extrait les taux TBA, TBS, TAP du primaire."""
    records = []
    years = ["2015-2016", "2016-2017", "2017-2018", "2018-2019", "2019-2020",
             "2020-2021", "2021-2022", "2022-2023", "2023-2024", "2024-2025"]
    for line in lines:
        parts = [p.strip().strip('"') for p in line.split(",")]
        if len(parts) < 31:
            continue
        region = parts[0].strip()
        if region == "" or region.lower().startswith("région") or region.lower().startswith("region"):
            continue
        norm_region = normalize_region_name(region)
        for idx, year in enumerate(years):
            g_idx = 1 + idx * 3
            f_idx = g_idx + 1
            t_idx = g_idx + 2
            g_val = clean_num(parts[g_idx])
            f_val = clean_num(parts[f_idx])
            t_val = clean_num(parts[t_idx])
            records.append({
                "Region": norm_region,
                "Annee_Scolaire": year,
                f"{indicator_name}_Garcons": g_val,
                f"{indicator_name}_Filles": f_val,
                f"{indicator_name}_Total": t_val
            })
    return pd.DataFrame(records)


def extract_primary_ips(lines, indicator_name):
    """Extrait les indices de parité (IPS)."""
    records = []
    years = ["2015-2016", "2016-2017", "2017-2018", "2018-2019", "2019-2020",
             "2020-2021", "2021-2022", "2022-2023", "2023-2024", "2024-2025"]
    for line in lines:
        parts = [p.strip().strip('"') for p in line.split(",")]
        if len(parts) < 11:
            continue
        region = parts[0].strip()
        if region == "" or region.lower().startswith("région") or region.lower().startswith("region"):
            continue
        norm_region = normalize_region_name(region)
        for idx, year in enumerate(years):
            val = clean_num(parts[1 + idx])
            records.append({
                "Region": norm_region,
                "Annee_Scolaire": year,
                f"IPS_{indicator_name}": val
            })
    return pd.DataFrame(records)


def extract_cep_rates(lines):
    """Extrait le taux de réussite au CEP (2016 à 2025)."""
    records = []
    years = ["2015-2016", "2016-2017", "2017-2018", "2018-2019", "2019-2020",
             "2020-2021", "2021-2022", "2022-2023", "2023-2024", "2024-2025"]
    current_region = None
    for line in lines:
        parts = [p.strip().strip('"') for p in line.split(",")]
        if len(parts) < 12:
            continue
        region_col, sexe_col = parts[0], parts[1]
        if region_col != "" and not region_col.lower().startswith("région"):
            current_region = normalize_region_name(region_col)
        if sexe_col.upper() in ["GARÇONS", "GARCONS", "FILLES", "TOTAL"] and current_region:
            sexe = "Garçons" if "GAR" in sexe_col.upper() else ("Filles" if "FIL" in sexe_col.upper() else "Total")
            for idx, year in enumerate(years):
                val = clean_num(parts[2 + idx])
                records.append({
                    "Region": current_region,
                    "Sexe": sexe,
                    "Annee_Scolaire": year,
                    "Taux_Reussite_CEP": val
                })
    return pd.DataFrame(records)


def extract_schools(lines):
    """Extrait le nombre d'écoles primaires par statut et région."""
    records = []
    years = ["2015-2016", "2016-2017", "2017-2018", "2018-2019", "2019-2020",
             "2020-2021", "2021-2022", "2022-2023", "2023-2024", "2024-2025"]
    current_region = None
    for line in lines:
        parts = [p.strip().strip('"') for p in line.split(",")]
        if len(parts) < 12:
            continue
        region_col, statut_col = parts[0], parts[1]
        if region_col != "" and not region_col.lower().startswith("region"):
            current_region = normalize_region_name(region_col)
        if statut_col.upper() in ["PUBLIC", "PRIVÉ", "PRIVE", "TOTAL"] and current_region:
            statut = "Public" if "PUB" in statut_col.upper() else ("Privé" if "PRIV" in statut_col.upper() else "Total")
            for idx, year in enumerate(years):
                val = clean_num(parts[2 + idx])
                records.append({
                    "Region": current_region,
                    "Statut": statut,
                    "Annee_Scolaire": year,
                    "Nombre_Ecoles": val
                })
    return pd.DataFrame(records)


def run_pipeline():
    """Exécute l'extraction et l'harmonisation complète avec toponymie unifiée préalable."""
    print("--- Démarrage du pipeline de structuration des données ---")
    blocks = parse_raw_blocks(RAW_DATA_PATH)

    dfs = {}

    for title, lines in blocks:
        t_clean = title.lower()
        if "effectifs du primaire" in t_clean and "par sexe et par région" in t_clean:
            dfs["effectifs_primaire_region"] = extract_primary_effectifs_region(lines)
        elif "effectifs du primaire" in t_clean and "milieu" in t_clean:
            dfs["effectifs_primaire_milieu"] = extract_primary_milieu(lines)
        elif "tba au primaire" in t_clean and "par sexe et par région" in t_clean:
            dfs["tba_primaire"] = extract_primary_rates(lines, "TBA")
        elif "tbs au primaire" in t_clean and "par sexe et par région" in t_clean:
            dfs["tbs_primaire"] = extract_primary_rates(lines, "TBS")
        elif "achèvement au primaire" in t_clean and "par sexe et par région" in t_clean:
            dfs["tap_primaire"] = extract_primary_rates(lines, "TAP")
        elif "ips du tba au primaire" in t_clean:
            dfs["ips_tba"] = extract_primary_ips(lines, "TBA")
        elif "ips du tbs au primaire" in t_clean:
            dfs["ips_tbs"] = extract_primary_ips(lines, "TBS")
        elif "ips du tap" in t_clean:
            dfs["ips_tap"] = extract_primary_ips(lines, "TAP")
        elif "réussite au cep" in t_clean:
            dfs["reussite_cep"] = extract_cep_rates(lines)
        elif "nombre d’écoles primaires" in t_clean:
            dfs["ecoles_primaire"] = extract_schools(lines)

    # Sauvegarde des tables individuelles
    for name, df in dfs.items():
        out_path = os.path.join(PROCESSED_DIR, f"{name}.csv")
        df.to_csv(out_path, index=False, encoding="utf-8")

    # Jointure avec toponymie déjà 100% normalisée
    merged = dfs["tbs_primaire"].merge(dfs["tba_primaire"], on=["Region", "Annee_Scolaire"], how="outer")
    merged = merged.merge(dfs["tap_primaire"], on=["Region", "Annee_Scolaire"], how="outer")
    merged = merged.merge(dfs["ips_tbs"], on=["Region", "Annee_Scolaire"], how="outer")
    merged = merged.merge(dfs["ips_tap"], on=["Region", "Annee_Scolaire"], how="outer")
    merged = merged.merge(dfs["ips_tba"], on=["Region", "Annee_Scolaire"], how="outer")

    # Effectifs
    eff_tot = dfs["effectifs_primaire_region"][dfs["effectifs_primaire_region"]["Sexe"] == "Total"].rename(
        columns={"Effectif": "Effectif_Total_Eleves"}
    ).drop(columns=["Sexe"])
    eff_f = dfs["effectifs_primaire_region"][dfs["effectifs_primaire_region"]["Sexe"] == "Filles"].rename(
        columns={"Effectif": "Effectif_Filles"}
    ).drop(columns=["Sexe"])
    eff_g = dfs["effectifs_primaire_region"][dfs["effectifs_primaire_region"]["Sexe"] == "Garçons"].rename(
        columns={"Effectif": "Effectif_Garcons"}
    ).drop(columns=["Sexe"])

    merged = merged.merge(eff_tot, on=["Region", "Annee_Scolaire"], how="left")
    merged = merged.merge(eff_f, on=["Region", "Annee_Scolaire"], how="left")
    merged = merged.merge(eff_g, on=["Region", "Annee_Scolaire"], how="left")

    # CEP
    cep_tot = dfs["reussite_cep"][dfs["reussite_cep"]["Sexe"] == "Total"].rename(
        columns={"Taux_Reussite_CEP": "Taux_CEP_Total"}
    ).drop(columns=["Sexe"])
    cep_f = dfs["reussite_cep"][dfs["reussite_cep"]["Sexe"] == "Filles"].rename(
        columns={"Taux_Reussite_CEP": "Taux_CEP_Filles"}
    ).drop(columns=["Sexe"])
    cep_g = dfs["reussite_cep"][dfs["reussite_cep"]["Sexe"] == "Garçons"].rename(
        columns={"Taux_Reussite_CEP": "Taux_CEP_Garcons"}
    ).drop(columns=["Sexe"])

    merged = merged.merge(cep_tot, on=["Region", "Annee_Scolaire"], how="left")
    merged = merged.merge(cep_f, on=["Region", "Annee_Scolaire"], how="left")
    merged = merged.merge(cep_g, on=["Region", "Annee_Scolaire"], how="left")

    consolidated_path = os.path.join(PROCESSED_DIR, "consolide_primaire_indicateurs.csv")
    merged.to_csv(consolidated_path, index=False, encoding="utf-8")

    livrable_02_csv = os.path.join(LIVRABLES_02_DIR, "D2_02-nettoyage_engineer_indicateurs-primaire-propres_v1.csv")
    merged.to_csv(livrable_02_csv, index=False, encoding="utf-8")
    print(f"-> Table consolidée parfaitement alignée : {len(merged)} lignes.")


if __name__ == "__main__":
    run_pipeline()
