"""
Module d'apprentissage automatique et d'analyse statistique avancée (Data Scientist).
Implémente :
1. Un clustering K-Means pour cartographier la typologie des profils régionaux d'inégalité.
2. Un modèle prédictif du Taux d'Achèvement des Filles (TAP) avec évaluation de performance (R2, RMSE).
3. L'analyse d'importance des variables (Explicabilité / Facteurs déterminants).
"""

import os
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")
LIVRABLES_04_DIR = os.path.join(BASE_DIR, "livrables", "04_analyse")
os.makedirs(LIVRABLES_04_DIR, exist_ok=True)


def train_clustering_model(df):
    """Effectue une segmentation K-Means des régions sur la dernière cohorte (2024-2025)."""
    latest_year = df["Annee_Scolaire"].max()
    df_latest = df[(df["Annee_Scolaire"] == latest_year) & (df["Region"] != "NATIONAL")].copy()

    features = [
        "TBS_Total",
        "TAP_Filles",
        "IPS_TBS",
        "IPS_TAP",
        "Deperdition_Filles",
        "Taux_CEP_Filles"
    ]

    X = df_latest[features].fillna(df_latest[features].mean())
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    df_latest["Cluster_Id"] = kmeans.fit_predict(X_scaled)

    # Attribution de labels compréhensibles aux clusters
    cluster_means = df_latest.groupby("Cluster_Id")["Score_Vulnerabilite_SCVE"].mean()
    sorted_clusters = cluster_means.sort_values(ascending=False).index

    label_map = {
        sorted_clusters[0]: "Zone d'Urgence Prioritaire (Très Vulnérable)",
        sorted_clusters[1]: "Zone en Transition (Vulnérabilité Moyenne)",
        sorted_clusters[2]: "Pôle Résilient / Avancé (Équité Favorable)"
    }
    df_latest["Typologie_Equite"] = df_latest["Cluster_Id"].map(label_map)

    return df_latest[["Region", "Cluster_Id", "Typologie_Equite", "Score_Vulnerabilite_SCVE"] + features]


def train_predictive_model(df):
    """Entraîne un modèle Random Forest pour anticiper le Taux d'Achèvement des Filles (TAP)."""
    df_model = df[df["Region"] != "NATIONAL"].copy()

    features = [
        "TBS_Total",
        "TBA_Filles",
        "TBA_Garcons",
        "IPS_TBA",
        "IPS_TBS",
        "Deperdition_Total"
    ]
    target = "TAP_Filles"

    data = df_model.dropna(subset=features + [target])
    X = data[features]
    y = data[target]

    # Séparation temporelle train / test (8 premières années pour l'entraînement, 2 dernières pour le test)
    years = sorted(df_model["Annee_Scolaire"].unique())
    train_years = years[:-2]
    test_years = years[-2:]

    train_mask = data["Annee_Scolaire"].isin(train_years)
    test_mask = data["Annee_Scolaire"].isin(test_years)

    X_train, y_train = X[train_mask], y[train_mask]
    X_test, y_test = X[test_mask], y[test_mask]

    rf = RandomForestRegressor(n_estimators=100, max_depth=5, random_state=42)
    rf.fit(X_train, y_train)

    y_pred = rf.predict(X_test)

    r2 = r2_score(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    mae = mean_absolute_error(y_test, y_pred)

    # Feature Importance
    importances = pd.DataFrame({
        "Variable": features,
        "Importance_Pct": (100 * rf.feature_importances_).round(2)
    }).sort_values(by="Importance_Pct", ascending=False)

    metrics_summary = {
        "R2_Score": round(float(r2), 4),
        "RMSE": round(float(rmse), 2),
        "MAE": round(float(mae), 2),
        "Nb_Observations_Train": len(X_train),
        "Nb_Observations_Test": len(X_test)
    }

    return rf, metrics_summary, importances


def run_models_pipeline():
    """Exécute les modèles, enregistre les résultats et prépare le livrable 04."""
    print("--- Exécution des modèles de Data Science (Défi 2) ---")
    data_path = os.path.join(PROCESSED_DIR, "indicateurs_equite_complets.csv")
    if not os.path.exists(data_path):
        print("Erreur : Le fichier indicateurs_equite_complets.csv est requis.")
        return

    df = pd.read_csv(data_path)

    # 1. Clustering
    df_clusters = train_clustering_model(df)
    clusters_path = os.path.join(PROCESSED_DIR, "typologie_regions_clusters.csv")
    df_clusters.to_csv(clusters_path, index=False, encoding="utf-8")
    print(f"-> Typologie des régions (Clustering K-Means) enregistrée : {clusters_path}")

    # 2. Modèle prédictif
    model, perf, importances = train_predictive_model(df)
    print("\nPerformances du modèle prédictif (TAP Filles) :")
    for k, v in perf.items():
        print(f"  • {k}: {v}")

    print("\nImportance des facteurs déterminants (Explicabilité) :")
    for _, row in importances.iterrows():
        print(f"  • {row['Variable']} : {row['Importance_Pct']}%")

    importances_path = os.path.join(PROCESSED_DIR, "importance_facteurs_tap_filles.csv")
    importances.to_csv(importances_path, index=False, encoding="utf-8")

    # Livrable 04 : Rapport d'évaluation du modèle
    livrable_04_md = os.path.join(LIVRABLES_04_DIR, "D2_04-analyse_scientist_rapport-modeles_v1.md")
    with open(livrable_04_md, "w", encoding="utf-8") as f:
        f.write("# Rapport d'Analyse et de Modélisation Prédictive (Défi 2)\n\n")
        f.write("## 1. Typologie territoriale des disparités (K-Means)\n")
        f.write("Les 13 régions du Burkina Faso ont été segmentées en 3 groupes homogènes :\n\n")
        f.write(df_clusters[["Region", "Typologie_Equite", "Score_Vulnerabilite_SCVE"]].to_markdown(index=False))
        f.write("\n\n## 2. Modèle Prédictif de Rétention des Filles (Random Forest Regressor)\n")
        f.write("### Performances statistiques du modèle sur données de test (Validation temporelle) :\n")
        for k, v in perf.items():
            f.write(f"- **{k}** : {v}\n")
        f.write("\n### Facteurs déterminants expliquant l'achèvement des filles :\n\n")
        f.write(importances.to_markdown(index=False))

    print(f"\n-> Livrable Étape 04 enregistré : {livrable_04_md}")
    print("--- Modélisation terminée avec succès ! ---")


if __name__ == "__main__":
    run_models_pipeline()
