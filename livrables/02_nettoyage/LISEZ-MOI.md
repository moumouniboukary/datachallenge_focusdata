# Dépôt 02 - Nettoyage et Harmonisation des données (Défi 2)

## 📌 Description du dépôt
Ce dépôt contient le journal des opérations de nettoyage ainsi que la table principale consolidée et nettoyée pour l'ensemble des indicateurs régionaux du Burkina Faso.

## 📂 Fichiers inclus
* `journal_nettoyage.md` : Détail rigoureux des anomalies détectées, corrections appliquées et choix méthodologiques.
* `D2_02-nettoyage_engineer_indicateurs-primaire-propres_v1.csv` : Table harmonisée au format tabulaire propre (140 observations : 14 entités géographiques x 10 années).

## ⚙️ Synthèse des traitements appliqués
1. **Suppression des en-têtes parasites** et des lignes de séparation présentes dans les fichiers bruts.
2. **Harmonisation de la toponymie régionale** : Remplacement des graphies variables (ex: "HAUT-BASSINS" ➔ "HAUTS-BASSINS", "BURKINA FASO" ➔ "NATIONAL").
3. **Standardisation des types de données** : Nettoyage des espaces insécables, virgules flottantes et conversion des valeurs en types numériques stricts (`float64`, `int64`).
4. **Détection et traitement des valeurs manquantes** : Analyse d'intégrité sur les séries temporelles 2016-2025.
