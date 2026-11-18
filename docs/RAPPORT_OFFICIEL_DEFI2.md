# FocusEduc : Mesurer et Réduire les Disparités d'Accès et d'Achèvement à l'Éducation au Burkina Faso
> **Data Challenge Burkina 2026 — Édition Éducation**  
> **Défi 2 : Analyse des disparités d'accès à l'éducation (parité fille-garçon, écart urbain-rural)**  
> *Dossier de documentation technique et décisionnelle (Conforme au plan officiel du concours)*

---

## 1. Le Défi et la Question Centrale (1 page)

### 1.1 Cadrage du problème
Au Burkina Faso, le système éducatif fait face à une double fracture structurelle :
1. **Une fracture de genre** : Bien que l'accès initial au CP1 ait atteint des niveaux encourageants grâce aux campagnes de sensibilisation, le maintien des jeunes filles tout au long du cycle primaire reste fragile, marqué par une déperdition accélérée aux abords du certificat d'études primaires (CM1-CM2).
2. **Une fracture territoriale (Urbain vs Rural)** : Alors que plus de 63% des effectifs scolarisables résident en milieu rural, les infrastructures (salles de classe en dur, adduction d'eau, blocs de latrines hygiéniques séparées) demeurent concentrées dans les centres urbains et les chefs-lieux régionaux. Cette précarité rurale a été lourdement exacerbée par les chocs sécuritaires de ces dernières années.

### 1.2 La Question Officielle du Défi et la Réponse Synthétique
> **La Question du Défi : « Où les écarts d'accès à l'école sont-ils les plus grands (filles-garçons, ville-campagne) et évoluent-ils ? »**

Notre analyse sur 10 ans apporte une réponse claire, territorialisée et quantifiée :

1. **Où l'écart Filles-Garçons est-il le plus grand ?**
   * **En accès initial (TBS/TBA) :** C'est dans le **Sahel** ($IPS = 0.88$) et à l'**Est** ($IPS = 0.91$) que les filles accusent le retard d'accès le plus prononcé.
   * **En achèvement (TAP) :** Un contraste saisissant apparaît : dans les pôles urbains (**Centre, Hauts-Bassins**), la parité est favorable aux filles ($IPS_{TAP} > 1.15$), car les garçons décrochent précocement pour l'orpaillage ou le travail informel. En revanche, dans les zones sahéliennes et d'insécurité, le taux d'achèvement des filles s'effondre en-dessous de **25%**.

2. **Où l'écart Ville-Campagne est-il le plus grand ?**
   * La fracture est maximale entre le **Centre (Ouagadougou)**, pôle urbain où le TBS dépasse **95%** et l'achèvement **75%**, et la région rurale du **Sahel**, où le TBS chute à **28.5%** et l'achèvement à **18.2%** (différentiel de 1 à 4).
   * Le milieu rural scolarise plus de **63% des effectifs du pays**, mais subit **90% des déficits de rétention** et des fermetures de classes.

3. **Comment ces écarts évoluent-ils sur 10 ans (2015-2025) ?**
   * **Parité filles-garçons :** Évolution **positive et convergente**. L'Indice de Parité national est passé de `0.940` (2015) à `0.996` (2025), atteignant la parité quasi-stricte en scolarisation.
   * **Écart urbain-rural :** Évolution **divergente et heurtée par la crise**. Entre 2018 et 2023, le milieu rural a perdu plus de **583 000 élèves** (-24.5%), tandis que le milieu urbain a progressé (+32% d'effectifs avec l'accueil des élèves déplacés internes). Un rebond s'amorce nettement dès 2024-2025 avec la réouverture progressive des structures.

---

## 2. Les Données : Périmètre, Sources et Limites (2 pages)

### 2.1 Sources mobilisées
* **Données principales** : Annuaires statistiques officiels de l'éducation nationale (2015/2016 à 2024/2025) produits par la Direction Générale des Études et des Statistiques Sectorielles (DGESS / MENAPLN).
* **Niveaux couverts** : Préscolaire et Primaire.
* **Granularité géographique** : Échelle nationale et 13 régions administratives.

### 2.2 Variables clés retenues
* **Effectifs d'élèves** : Déclinés par sexe (Garçons, Filles), statut d'établissement (Public, Privé, Communautaire) et milieu d'implantation (Urbain, Rural).
* **Indicateurs d'accès et de flux** : Taux Brut d'Accès (TBA) au CP1, Taux Brut de Scolarisation (TBS) et Taux d'Achèvement au Primaire (TAP).
* **Indicateurs de parité** : Indice de Parité entre les Sexes (IPS) mesuré sur l'accès ($IPS_{TBA}$), la scolarisation ($IPS_{TBS}$) et l'achèvement ($IPS_{TAP}$).
* **Examens et certification** : Taux de réussite au CEP (2016 à 2025).
* **Capacité d'accueil** : Nombre d'écoles primaires et de salles de classe fonctionnelles.

### 2.3 Limites des données et esprit critique
1. **Sous-déclaration dans les zones à fort défi sécuritaire** : Entre 2019 et 2023, la fermeture temporaire de certains établissements dans le Sahel, l'Est ou la Boucle du Mouhoun a pu complexifier la collecte exhaustive des statistiques scolaires.
2. **Mobilité des Élèves Déplacés Internes (EDI)** : Les transferts massifs d'élèves vers les centres urbains plus sécurisés (Ouagadougou, Bobo-Dioulasso, Koudougou) expliquent en partie la hausse des effectifs urbains sans que cela ne traduise une progression endogène des taux de scolarisation locaux.

---

## 3. Préparation, Nettoyage et Harmonisation des Données (2 à 3 pages)

### 3.1 Pipeline de transformation (Data Engineering)
Le traitement s'est appuyé sur une architecture de nettoyage modulaire développée sous Python (`src/data_loader.py`) :
1. **Scission et parsing tabulaire** : Isolement de 21 tables composites issues du classeur général.
2. **Harmonisation toponymique** : Normalisation des graphies des régions administratives (résolution des doublons typographiques tels que `HAUT-BASSINS` standardisé en `HAUTS-BASSINS`).
3. **Nettoyage typologique** : Élimination des caractères invisibles, des espaces insécables et conversion rigoureuse en formats numériques flottants.
4. **Schéma relationnel cible** : Consolidation d'un jeu de données unique reliant chaque observation `(Region, Annee_Scolaire)`.

### 3.2 Nouvelles métriques créées (Data Analytics)
* **Écart de Parité Absolu ($EP_{pts}$)** :
  $$EP_{pts} = \text{Taux Filles} - \text{Taux Garçons}$$
* **Taux de Déperdition Primaire ($TDP$)** :
  $$TDP = \max(0, TBA_{CP1} - TAP_{CM2})$$
  Ce taux quantifie la proportion d'enfants ayant débuté l'école mais n'atteignant pas l'évaluation certificative du cycle.
* **Score Composite de Vulnérabilité Éducative ($SCVE$)** :
  Indice synthétique normé de 0 à 100 intégrant le déficit d'achèvement (35%), la déperdition globale (40%) et la pénalité de non-parité de genre (25%).

---

## 4. Méthodologie et Modélisation (3 pages)

### 4.1 Approche statistique et segmentation (K-Means)
Afin de dépasser la simple moyenne nationale, une classification non supervisée par K-Means a été appliquée sur l'ensemble des 13 régions. Le partitionnement optimal ($k=3$) fait émerger trois réalités territoriales distinctes :
* **Groupe 1 : Zones de Crise et d'Urgence Humanitaire (Sahel, Est)** : Caractérisées par un TBS inférieur à 35% et un TAP féminin sous la barre des 20%.
* **Groupe 2 : Zones en Transition Vulnérable (Boucle du Mouhoun, Centre-Nord, Nord)** : Accès initial moyen à élevé ($TBA > 80\%$), mais chute critique d'achèvement ($TDP > 50\text{ pts}$).
* **Groupe 3 : Pôles de Résilience et Centres Urbains (Centre, Hauts-Bassins, Plateau Central)** : Scolarisation élevée, parité de genre proche ou supérieure à 1,0.

### 4.2 Modèle Prédictif de Rétention Féminine (Random Forest)
Pour prédire le Taux d'Achèvement des Filles à partir des signaux précoces de scolarisation, un régresseur par Forêts Aléatoires a été calibré avec une stratégie de validation temporelle stricte (données antérieures pour l'apprentissage, 2 dernières années scolaires pour le test).

**Résultats de validation :**
* Coefficient de détermination ($R^2$) : **0.9439**
* Erreur quadratique moyenne (RMSE) : **6.13 points**
* Erreur absolue moyenne (MAE) : **4.36 points**

### 4.3 Facteurs déterminants (Explicabilité / XAI)
L'analyse de l'importance des variables démontre que la déperdition scolaire globale et le ratio d'accès initial expliquent à plus de **90%** l'achèvement final des filles, confirmant que l'abandon se joue dès les premières classes intermédiaires (CE1-CE2).

---

## 5. Résultats et Visualisations Clés (3 pages)

### 5.1 La dynamique temporelle (2016-2025)
L'analyse sur 10 ans révèle une dynamique en trois phases :
1. **2015-2018 : Progression continue** des effectifs nationaux (atteignant 3,23 millions d'élèves au primaire).
2. **2019-2022 : Fléchissement sévère** concentré sur les zones rurales (perte nette de près de 580 000 élèves ruraux).
3. **2023-2025 : Rebond et résilience**, les effectifs ruraux repassant au-dessus de 2,1 millions d'élèves en 2025 grâce aux stratégies alternatives de scolarisation et aux réouvertures.

### 5.2 L'Indice de Parité des Sexes (IPS)
Au niveau national, l'IPS du TBS est passé de `1.006` en 2016 à `0.996` en 2025, traduisant une parité globale en accès. Toutefois, l'IPS du Taux d'Achèvement (TAP) oscille entre `1.10` et `1.21` dans plusieurs régions, révélant que là où les filles parviennent à rester à l'école, elles terminent souvent leur cycle avec une assiduité supérieure à celle des garçons, ces derniers étant parfois retirés pour des activités de subsistance (orpaillage, pastoralisme).

---

## 6. Réponse au Défi et Aide à la Décision (1 à 2 pages)

### 6.1 Un outil opérationnel pour les directeurs régionaux (DREPS)
Pour répondre concrètement à l'attente du jury, la plateforme **FocusEduc** intègre un **simulateur de scénarios (« What-If »)** :
* Il permet d'estimer en direct le gain en achèvement et en parité selon le niveau d'équipement alloué (pourcentage d'écoles dotées de cantines scolaires régulières, de blocs de latrines séparées filles et de bourses de kits scolaires).

### 6.2 Recommandations de politiques publiques ciblées
1. **Priorité 1 : Infrastructures d'assainissement genrées** : La construction de blocs sanitaires séparés pour filles est le facteur physique le plus corrélé à la réduction de l'abandon en CM1-CM2.
2. **Priorité 2 : Sécurisation des cantines scolaires en milieu rural** : La cantine scolaire constitue un filet social indispensable pour maintenir les enfants scolarisés, particulièrement dans les régions sahéliennes et septentrionales.
3. **Priorité 3 : Dispositif de passerelle pour les Élèves Déplacés Internes (EDI)** : Stabiliser l'intégration des cohortes déplacées dans les écoles d'accueil sans dégrader le ratio élèves/enseignant.

---

## 7. Guide de Reproduction Technique (1 page)

Pour reproduire l'ensemble des analyses, des métriques et faire tourner la solution en local ou sur un serveur :

```bash
# 1. Cloner ou ouvrir le répertoire du projet
cd datachallenge_focusdata

# 2. Installer les dépendances certifiées
pip install -r requirements.txt

# 3. Exécuter la chaîne de traitement (dans l'ordre)
python src/data_loader.py        # Étape 1 & 2 : Nettoyage et consolidation
python src/metrics.py            # Étape 3 : Calcul des indicateurs d'équité
python src/models.py             # Étape 4 : Modélisation K-Means et Random Forest
python src/decision_support.py   # Étape 5 : Production des fiches décisionnelles

# 4. Lancer le tableau de bord interactif
streamlit run app.py
```
