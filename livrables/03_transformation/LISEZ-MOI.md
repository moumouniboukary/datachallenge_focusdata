# Dépôt 03 - Transformation des Données & Nouvelles Variables (Défi 2)

## 📌 Description du dépôt
Ce dépôt fournit les tables enrichies avec les variables d'équité calculées par l'équipe (Data Analyst / Data Architect).

## 📂 Fichiers inclus
* `dictionnaire_variables.md` : Définition formelle, formules mathématiques et unités de mesure de chaque variable.
* `D2_03-transformation_analyst_indicateurs-equite_v1.csv` : Jeu de données enrichi comportant les scores d'écart de genre, les taux de déperdition et le Score Composite de Vulnérabilité Éducative (SCVE).

## 🎯 Nouvelles variables créées
1. **Écarts de genre absolus (`Ecart_Genre_TBS_pts`, `Ecart_Genre_TAP_pts`)** : Différence en points de pourcentage entre filles et garçons.
2. **Déperdition scolaire (`Deperdition_Total`, `Deperdition_Filles`, `Deperdition_Garcons`)** : Écart entre le Taux Brut d'Accès au CP1 et le Taux d'Achèvement au CM2 ($TBA - TAP$).
3. **Score Composite de Vulnérabilité Éducative (`Score_Vulnerabilite_SCVE`)** : Score territorial d'aide à la décision (0 à 100).
4. **Classification officielle UNESCO (`Statut_Parite_TBS`, `Statut_Parite_TAP`)** : Catégorisation qualitative de l'équité de genre.
