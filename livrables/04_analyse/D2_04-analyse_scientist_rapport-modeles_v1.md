# Rapport d'Analyse et de Modélisation Prédictive (Défi 2)

## 1. Typologie territoriale des disparités (K-Means)
Les 13 régions du Burkina Faso ont été segmentées en 3 groupes homogènes :

| Region            | Typologie_Equite                             |   Score_Vulnerabilite_SCVE |
|:------------------|:---------------------------------------------|---------------------------:|
| BOUCLE DU MOUHOUN | Zone en Transition (Vulnérabilité Moyenne)   |                       47.2 |
| CASCADES          | Zone en Transition (Vulnérabilité Moyenne)   |                       43.3 |
| CENTRE            | Pôle Résilient / Avancé (Équité Favorable)   |                       19.4 |
| CENTRE-EST        | Zone en Transition (Vulnérabilité Moyenne)   |                       42.8 |
| CENTRE-NORD       | Zone en Transition (Vulnérabilité Moyenne)   |                       50.2 |
| CENTRE-OUEST      | Pôle Résilient / Avancé (Équité Favorable)   |                       24.7 |
| CENTRE-SUD        | Pôle Résilient / Avancé (Équité Favorable)   |                       24.6 |
| EST               | Zone d'Urgence Prioritaire (Très Vulnérable) |                       44.4 |
| HAUTS-BASSINS     | Pôle Résilient / Avancé (Équité Favorable)   |                       28.7 |
| NORD              | Zone en Transition (Vulnérabilité Moyenne)   |                       59.8 |
| PLATEAU CENTRAL   | Zone en Transition (Vulnérabilité Moyenne)   |                       35.6 |
| SAHEL             | Zone d'Urgence Prioritaire (Très Vulnérable) |                       50.2 |
| SUD-OUEST         | Zone en Transition (Vulnérabilité Moyenne)   |                       40.5 |

## 2. Modèle Prédictif de Rétention des Filles (Random Forest Regressor)
### Performances statistiques du modèle sur données de test (Validation temporelle) :
- **R2_Score** : 0.9439
- **RMSE** : 6.13
- **MAE** : 4.36
- **Nb_Observations_Train** : 104
- **Nb_Observations_Test** : 26

### Facteurs déterminants expliquant l'achèvement des filles :

| Variable          |   Importance_Pct |
|:------------------|-----------------:|
| TBS_Total         |            80.36 |
| TBA_Filles        |             9.07 |
| Deperdition_Total |             4.4  |
| TBA_Garcons       |             4.35 |
| IPS_TBA           |             1.25 |
| IPS_TBS           |             0.56 |