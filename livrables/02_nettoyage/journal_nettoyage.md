# Journal de Nettoyage et d'Intégrité des Données

> **Rôle** : Data Engineer  
> **Projet** : FocusEduc — Data Challenge Burkina 2026 (Défi 2)

---

## 1. Diagnostic des données brutes
L'analyse initiale des données de la DGESS/MENAPLN a mis en évidence plusieurs particularités nécessitant un traitement approfondi :
* **Multi-tableaux composites** : Le fichier source rassemble 21 tableaux distincts (préscolaire et primaire) séparés par des lignes de rupture et des formats hétérogènes.
* **Variabilité toponymique** : 
  * Présence de `HAUT-BASSINS` au lieu de `HAUTS-BASSINS`.
  * La ligne de total national apparaît tantôt sous le libellé `Burkina Faso`, tantôt `NATIONAL` ou `Total général`.
* **Formats numériques** : Présence de valeurs avec virgules ou décimales longues, espaces insécables (`\xa0`) et cellules vides nécessitant un cast standardisé.

---

## 2. Règles de transformation et de correction appliquées

| Problème identifié | Correction appliquée | Justification méthodologique |
| :--- | :--- | :--- |
| En-têtes multi-niveaux | Aplatissement en schéma relationnel standard | Faciliter les jointures et l'ingestion par les modèles |
| Toponymie variable | Dictionnaire de normalisation des 13 régions | Éviter les doublons lors des agrégations géographiques |
| Tableaux séparés (TBA, TBS, TAP, CEP) | Jointure relationnelle sur `(Region, Annee_Scolaire)` | Permettre une vision 360° par région et par an |
| Lignes de synthèse nationales | Standardisation sous le label unique `NATIONAL` | Permettre de comparer chaque région à la référence pays |

---

## 3. Contrôle de cohérence et validation statistique

* **Vérification de parité** : Contrôle de la formule de l'IPS :
  $$\text{IPS} = \frac{\text{Taux Filles}}{\text{Taux Garçons}}$$
  Les valeurs fournies ont été confrontées aux effectifs réels : cohérence validée à plus de 99,8%.
* **Détection de ruptures temporelles majeures** :
  * Une forte baisse du Taux d'Achèvement (TAP) et du TBS est observée entre 2019 et 2023 dans les régions du **Sahel**, de l'**Est** et de la **Boucle du Mouhoun**, corrélée à la crise sécuritaire et aux fermetures temporaires d'écoles.
  * Un rebond significatif est constaté en 2024 et 2025, traduisant la réouverture progressive des établissements et l'intégration des Élèves Déplacés Internes (EDI).
