# Dictionnaire des Variables et Indicateurs

> **Projet** : FocusEduc — Data Challenge Burkina 2026 (Défi 2)  
> **Auteur** : Data Architect & Data Analyst

---

### 1. Variables d'identification
| Variable | Type | Description | Exemple |
| :--- | :--- | :--- | :--- |
| `Region` | Chaîne | Nom de la région administrative (13 régions du Burkina Faso ou `NATIONAL`) | `CENTRE-NORD`, `SAHEL` |
| `Annee_Scolaire` | Chaîne | Cohorte de l'année scolaire | `2024-2025` |

---

### 2. Indicateurs d'accès, scolarisation et rétention
| Variable | Type | Unité | Définition & Formule |
| :--- | :--- | :--- | :--- |
| `TBA_Total` | Flottant | % | Taux Brut d'Accès : proportion des nouveaux inscrits au CP1 par rapport à la population d'âge officiel (6 ans). |
| `TBA_Garcons` / `TBA_Filles` | Flottant | % | Taux Brut d'Accès désagrégé selon le sexe. |
| `TBS_Total` | Flottant | % | Taux Brut de Scolarisation : effectif total scolarisé au primaire rapporté à la population scolarisable (6-11 ans). |
| `TBS_Garcons` / `TBS_Filles` | Flottant | % | Taux Brut de Scolarisation selon le sexe. |
| `TAP_Total` | Flottant | % | Taux d'Achèvement au Primaire : proportion d'élèves atteignant la dernière année du primaire (CM2) hors redoublants. |
| `TAP_Garcons` / `TAP_Filles` | Flottant | % | Taux d'Achèvement désagrégé par sexe. |
| `Taux_CEP_Total` | Flottant | % | Taux d'admission à l'examen du Certificat d'Études Primaires (CEP). |

---

### 3. Indicateurs de parité et de disparités (Défi 2)
| Variable | Type | Formule de calcul | Interprétation |
| :--- | :--- | :--- | :--- |
| `IPS_TBS` | Flottant | $\frac{\text{TBS Filles}}{\text{TBS Garçons}}$ | Indice de Parité entre les Sexes au TBS. $<1$ : défaveur des filles ; $>1$ : défaveur des garçons. |
| `IPS_TAP` | Flottant | $\frac{\text{TAP Filles}}{\text{TAP Garçons}}$ | Indice de Parité au stade final du primaire (achèvement). |
| `Ecart_Genre_TBS_pts` | Flottant | $\text{TBS Filles} - \text{TBS Garçons}$ | Écart direct en points de pourcentage. |
| `Deperdition_Total` | Flottant | $\max(0, \text{TBA Total} - \text{TAP Total})$ | Taux d'élèves perdus entre l'entrée au CP1 et la fin du CM2. |
| `Deperdition_Filles` | Flottant | $\max(0, \text{TBA Filles} - \text{TAP Filles})$ | Déperdition spécifique aux jeunes filles. |
| `Score_Vulnerabilite_SCVE` | Flottant | Score composite pondéré de 0 à 100 | Synthèse d'alerte pour les décideurs : combine faible achèvement, déperdition et inégalités de genre. |
