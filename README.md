# FocusEduc 🇧🇫
> **Plateforme intelligente pour mesurer et réduire les inégalités d'accès à l'éducation au Burkina Faso**  
> *Data Challenge Burkina 2026 - Défi 2 (Semaine du Numérique)*

---

## 🎯 Contexte et Objectifs
Dans le cadre de la 21ᵉ édition de la Semaine du Numérique organisée par le MTDPCE et Africa Data Entry (ADE), **FocusEduc** répond au Défi 2 :
- **Mesurer les inégalités d'accès à l'éducation** : Parité fille-garçon & fracture territoriale urbain-rural.
- **Identifier l'intersection de vulnérabilité** : Mettre en lumière la situation spécifique des filles en milieu rural.
- **Aider à la décision publique** : Fournir une cartographie interactive, des indicateurs décisionnels et un simulateur d'impact ("What-If") pour les autorités éducatives et collectivités territoriales.

---

## 🏗️ Structure du Projet

```text
datachallenge_focusdata/
├── data/
│   ├── raw/            # Données brutes (annuaires statistiques MENAPLN, INSD, HDX)
│   └── processed/      # Données nettoyées, consolidées et enrichies
├── src/
│   ├── data_loader.py  # Ingestion, parsing et nettoyage des données
│   ├── metrics.py      # Calcul des indicateurs (IPG, ratios urbain/rural, scores de vulnérabilité)
│   ├── models.py       # Algorithmes de prédiction et d'explicabilité (XAI / SHAP)
│   └── simulation.py   # Moteur de simulation d'impact d'interventions
├── app.py              # Application interactive principale (Streamlit)
├── requirements.txt    # Dépendances Python
└── README.md           # Documentation du projet
```

---

## 🚀 Installation & Démarrage

```bash
# Installation des dépendances
pip install -r requirements.txt

# Lancement de l'application interactive
streamlit run app.py
```
