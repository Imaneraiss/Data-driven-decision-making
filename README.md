<<<<<<< HEAD
# Projet DDM — Data-Driven Decision Making

---
=======
Projet DDM — Data-Driven Decision Making
>>>>>>> a972d35c668de2dabc8e291631dc536eddb849fd

## Hafsa — Phases 1, 2 & 3 : Analyse des Données

Réalisé par : Hafsa ABBAR — Data Analyst

### Ce qui a été fait

<<<<<<< HEAD
**Phase 1 — Définition du Problème & KPIs**
=======
Phase 1 — Définition du Problème & KPIs
>>>>>>> a972d35c668de2dabc8e291631dc536eddb849fd
- Question décisionnelle centrale définie
- KPI Tree hiérarchique (CA, Rétention, NPS)
- Business Case : ROI estimé à +9.4% si churn réduit de 10%

<<<<<<< HEAD
**Phase 2 — Collecte & Audit des Données**
=======
Phase 2 — Collecte & Audit des Données
>>>>>>> a972d35c668de2dabc8e291631dc536eddb849fd
- Cartographie de 9 sources de données (100K+ lignes)
- Audit de qualité : colonnes manquantes, doublons, données fantômes
- Data Dictionary complet
- Stratégies d'imputation définies

<<<<<<< HEAD
**Phase 3 — Exploration & Analyse Statistique (EDA)**
=======
Phase 3 — Exploration & Analyse Statistique (EDA)
>>>>>>> a972d35c668de2dabc8e291631dc536eddb849fd
- Dataset analytique consolidé : 96 478 commandes × 25 variables
- Statistiques descriptives + détection d'outliers
- Matrice de corrélations + 4 tests statistiques
- Segmentation RFM : 2 clusters (Champions 3% / One-shot 97%)
- Analyses métier : satisfaction vs livraison, CA mensuel, top catégories

### Résultats clés

- Churn estimé : 96.9%
- Satisfaction moyenne : 4.16/5
- Livraison tardive → score moyen 2.27 vs 4.29 à temps
- São Paulo = 42% des clients (biais géographique)

### Fichiers produits

<<<<<<< HEAD
- `olist_analytical_dataset.csv` → dataset principal nettoyé (96 478 lignes)
- `olist_rfm_clusters.csv` → segmentation RFM + clusters
- `data_dictionary.csv` → dictionnaire des données
- `kpi_tree.png` → arbre des KPIs
- `correlation_heatmap.png` → matrice de corrélations
- `kmeans_clusters.png` → visualisation des clusters

---
=======
- olist_analytical_dataset.csv  → dataset principal nettoyé (96 478 lignes)
- olist_rfm_clusters.csv        → segmentation RFM + clusters
- data_dictionary.csv           → dictionnaire des données
- kpi_tree.png                  → arbre des KPIs
- correlation_heatmap.png       → matrice de corrélations
- kmeans_clusters.png           → visualisation des clusters
>>>>>>> a972d35c668de2dabc8e291631dc536eddb849fd

## Imane — Phase 4 : Modélisation Prédictive

Réalisé par : Raiss Imane — Data Scientist & ML Engineer

### Ce qui a été fait

1. Feature Engineering — 18 variables préparées pour les modèles
2. Définition du churn — clients inactifs depuis > 180 jours
3. Gestion du déséquilibre — SMOTE (66% churners / 34% non-churners)
4. Entraînement de 3 modèles de classification :
   - Régression Logistique (baseline)
   - Random Forest
   - XGBoost (modèle retenu)
5. Validation croisée 5-fold + tuning GridSearch
6. Interprétabilité SHAP — identification des leviers du churn
7. Export des scores de risque par client

### Résultats

| Modèle                | AUC-ROC | F1-Score |
|-----------------------|---------|----------|
| Régression Logistique | 0.749   | 0.749    |
| Random Forest         | 0.971   | 0.927    |
| XGBoost (optimisé) ✅ | 0.977   | 0.938    |

### Fichiers produits

<<<<<<< HEAD
- `churn_scores.csv` → scores de risque par client
- `xgb_churn_model.pkl` → modèle sauvegardé
- `shap_importance_globale.png` → leviers du churn

---

## Halima — Phases 5 & 6 : Dashboard & Décision Analytics

Réalisé par : Halima — Data Storyteller & Décision Analyst

# 🛒 Olist Churn & LTV Dashboard

> **Projet DDM — Data-Driven Decision Making**  
> Membre 3 · Data Storyteller & Décision Analyst  
> Dataset : Olist Brazilian E-commerce · 96 478 commandes · 93 358 clients

---

## 📋 Description

Dashboard analytique interactif développé avec **Streamlit** et **Plotly** pour visualiser et piloter la stratégie de réduction du churn client sur la plateforme Olist (e-commerce brésilien, 2016-2018).

Le dashboard couvre les phases 5 & 6 du projet DDM :
- **Phase 5** — Data Storytelling : 7 vues distinctes dont 3 vues par profil utilisateur
- **Phase 6** — Décision Analytics : recommandations actionnables et impact financier

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                          Utilisateur                            │
│                      (Navigateur Web)                           │
└─────────────────────────────┬───────────────────────────────────┘
                              │ HTTP localhost:8501
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Streamlit Server                           │
│  ┌─────────────┐   ┌───────────────┐   ┌─────────────────────┐ │
│  │   Sidebar   │   │  Page Router  │   │   CSS / Styling     │ │
│  │  (Filtres)  │   │   (7 pages)   │   │   (dark theme)      │ │
│  └─────────────┘   └──────┬────────┘   └─────────────────────┘ │
│                           │                                     │
│          ┌────────────────┼─────────────────┐                   │
│          ▼                ▼                 ▼                   │
│  ┌──────────────┐ ┌─────────────┐ ┌─────────────────┐          │
│  │ Vue Générale │ │ Analyse     │ │  Modèles ML     │          │
│  │ CA · Géo    │ │ du Churn    │ │  XGBoost · SHAP │          │
│  │ Heures/Jrs  │ │ Scores·RFM  │ │  ROC · Params   │          │
│  └──────────────┘ └─────────────┘ └─────────────────┘          │
│                           │                                     │
│              ┌────────────┼────────────┐                        │
│              ▼            ▼            ▼                        │
│     ┌──────────────┐ ┌─────────┐ ┌──────────┐                  │
│     │Recommandations│ │Direction│ │Opérations│                  │
│     │ROI · Financier│ │Exécutif │ │Livraison │                  │
│     └──────────────┘ └─────────┘ └──────────┘                  │
│                                       │                         │
│                               ┌───────────────┐                 │
│                               │   Marketing   │                 │
│                               │ Segmentation  │                 │
│                               └───────────────┘                 │
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │             generate_data()  @st.cache_data               │  │
│  │     NumPy · Pandas (données simulées phases 1–4)          │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                       Plotly (Charts)                           │
│    go.Figure · px · make_subplots · Scatter · Bar · Pie        │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📁 Structure des Fichiers

```
olist-dashboard/
│
├── app.py                  # Point d'entrée principal — application Streamlit
=======
- churn_scores.csv          → scores de risque par client
- xgb_churn_model.pkl       → modèle sauvegardé
- shap_importance_globale.png → leviers du churn

## Halima · Data Storyteller & Décision Analyst
Dataset : Olist Brazilian E-commerce · 96 478 commandes · 93 358 clients

📋 Description
Dashboard analytique interactif développé avec Streamlit et Plotly pour visualiser et piloter la stratégie de réduction du churn client sur la plateforme Olist (e-commerce brésilien, 2016-2018).

Le dashboard couvre les phases 5 & 6 du projet DDM :

Phase 5 — Data Storytelling : visualisation des insights clés
Phase 6 — Décision Analytics : recommandations actionnables et impact financier
🏗️ Architecture
┌─────────────────────────────────────────────────────────────┐
│                        Utilisateur                          │
│                    (Navigateur Web)                         │
└───────────────────────────┬─────────────────────────────────┘
                            │ HTTP localhost:8501
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                   Streamlit Server                          │
│  ┌─────────────┐  ┌──────────────┐  ┌───────────────────┐  │
│  │   Sidebar   │  │  Page Router │  │   CSS / Styling   │  │
│  │  (Filtres)  │  │  (4 pages)   │  │  (dark theme)     │  │
│  └─────────────┘  └──────┬───────┘  └───────────────────┘  │
│                          │                                  │
│          ┌───────────────┼───────────────┐                  │
│          ▼               ▼               ▼                  │
│  ┌──────────────┐ ┌────────────┐ ┌─────────────────┐       │
│  │ Vue Générale │ │  Churn     │ │  Modèles ML     │       │
│  │  CA · Géo   │ │  Analyse   │ │  XGBoost · SHAP │       │
│  │  Heures/Jrs │ │  Scores    │ │  ROC · Params   │       │
│  └──────────────┘ └────────────┘ └─────────────────┘       │
│                          │                                  │
│                          ▼                                  │
│                ┌──────────────────┐                         │
│                │ Recommandations  │                         │
│                │ ROI · Financier  │                         │
│                └──────────────────┘                         │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              generate_data()  @st.cache_data         │   │
│  │   NumPy · Pandas (données simulées phases 1-4)       │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    Plotly (Charts)                          │
│   go.Figure · px · make_subplots · Scatter · Bar · Pie     │
└─────────────────────────────────────────────────────────────┘
📁 Structure des Fichiers
olist-dashboard/
│
├── dashboard.py            # Point d'entrée principal — application Streamlit
>>>>>>> a972d35c668de2dabc8e291631dc536eddb849fd
│   ├── CSS custom          # Dark theme complet (Inter font, KPI cards, badges)
│   ├── generate_data()     # Génération des données simulées (seed=42, @cache)
│   ├── CHART_THEME         # Config Plotly globale (couleurs, grilles, fonts)
│   ├── kpi()               # Composant carte KPI réutilisable
<<<<<<< HEAD
│   │
│   ├── ── Vues Analytiques ──
│   ├── Page 1 : Vue Générale
│   ├── Page 2 : Analyse du Churn
│   ├── Page 3 : Modèles ML
│   ├── Page 4 : Recommandations
│   │
│   └── ── Vues par Profil ──
│       ├── Page 5 : Direction
│       ├── Page 6 : Opérations
│       └── Page 7 : Marketing
│
├── rapport_ab_test.tex     # Source LaTeX du plan A/B Test (2 pages)
├── requirements.txt        # Dépendances Python
└── README.md               # Ce fichier
```

---

## ⚙️ Installation

### Prérequis

- Python **3.9+**
- pip ou conda

### 1. Cloner le projet

```bash
git clone https://github.com/votre-repo/olist-dashboard.git
cd olist-dashboard
```

### 2. Créer un environnement virtuel

```bash
=======
│   ├── Page 1 : Vue Générale
│   ├── Page 2 : Analyse du Churn
│   ├── Page 3 : Modèles ML
│   └── Page 4 : Recommandations
│
├── requirements.txt        # Dépendances Python (voir ci-dessous)
├── README.md               # Ce fichier
│
└── (optionnel)
    └── data/
        └── olist_*.csv     # Données réelles Olist si disponibles
⚙️ Installation
Prérequis
Python 3.9+
pip ou conda
1. Cloner le projet
git clone https://github.com/votre-repo/olist-dashboard.git
cd olist-dashboard
2. Créer un environnement virtuel
>>>>>>> a972d35c668de2dabc8e291631dc536eddb849fd
# Avec venv
python -m venv .venv
source .venv/bin/activate        # Linux / macOS
.venv\Scripts\activate           # Windows

# Ou avec conda
conda create -n olist python=3.11
conda activate olist
<<<<<<< HEAD
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Lancer le dashboard

```bash
streamlit run app.py
```

Le dashboard s'ouvre automatiquement sur **http://localhost:8501**

---

## 📦 Dépendances (`requirements.txt`)

```txt
=======
3. Installer les dépendances
pip install -r requirements.txt
4. Lancer le dashboard
streamlit run dashboard.py
Le dashboard s’ouvre automatiquement sur http://localhost:8501

📦 Dépendances (requirements.txt)
>>>>>>> a972d35c668de2dabc8e291631dc536eddb849fd
streamlit>=1.32.0
pandas>=2.0.0
numpy>=1.24.0
plotly>=5.18.0
<<<<<<< HEAD
scikit-learn>=1.3.0
```

---

## 🗂️ Pages du Dashboard

### Vues Analytiques

| Page | Contenu | Composants clés |
|------|---------|-----------------|
| **📊 Vue Générale** | KPIs globaux, CA mensuel, répartition géographique, comportement temporel, top catégories | Line chart, Donut, Bar charts |
| **🔴 Analyse du Churn** | Zones de risque, distribution des scores, satisfaction vs retard, RFM K-Means, tests statistiques | Histogram, Pie, Scatter, Subplots |
| **🤖 Modèles ML** | Comparaison des 3 modèles, courbe ROC, SHAP values, configuration XGBoost | Bar groupé, Scatter ROC, Bar horizontal |
| **💡 Recommandations** | 3 leviers actionnables, impact financier, ROI par levier, timeline | Cards HTML, Bar groupé, KPI cards |

### Vues par Profil Utilisateur

| Profil | Audience | Contenu | Focus |
|--------|----------|---------|-------|
| **🏢 Direction** | CODIR, DG | Synthèse exécutive, CA projeté sur 12 mois, ROI des 3 leviers, points d'attention stratégiques | Décision, ROI, risques |
| **⚙️ Opérations** | Responsables logistique, Ops | Taux de retard par État, courbe satisfaction vs délai, plan d'action terrain (SLA, notifications) | Livraison, qualité service |
| **📣 Marketing** | CMO, équipes CRM | Segments RFM ciblables, zones de risque actionnables, créneaux d'envoi optimaux, plan de ciblage | Campagnes, segmentation |

---

## 🎛️ Filtres Disponibles (Sidebar)

| Filtre | Type | Valeur par défaut | Impact |
|--------|------|-------------------|--------|
| **Seuil de risque churn** | Slider [0.0 – 1.0] | `0.70` | Ligne de seuil sur l'histogramme des scores |
| **Segment client** | Multiselect | Tous | Filtrage par cluster K-Means (Champions / One-shot) |

---

## 📊 Données & Métriques Clés

Les données sont **simulées** à partir des résultats réels des phases 1 à 4 du projet  
(seed fixe `np.random.seed(42)` pour la reproductibilité) :

| Métrique | Valeur réelle |
|----------|--------------|
| Commandes totales | 99 441 |
| Clients uniques | 93 358 |
| Taux de churn | **96.9%** |
| Taux repeat purchase | **3.1%** |
| Score satisfaction moyen | 4.16 / 5 |
| Taux livraisons en retard | 6.8% |
| Clients zone rouge (score ≥ 0.70) | **10 966** |
| AUC-ROC XGBoost | **0.977** |

---

## 🤖 Modèle XGBoost — Configuration Optimale

```python
=======
🗂️ Pages du Dashboard
Page	Contenu	Composants clés
📊 Vue Générale	KPIs globaux, CA mensuel, géographie, heures/jours, top catégories	Line chart, Donut, Bar charts
🔴 Analyse du Churn	Zones de risque, distribution des scores, satisfaction vs retard, RFM K-Means, tests statistiques	Histogram, Pie, Scatter, Subplots
🤖 Modèles ML	Comparaison des 3 modèles, courbe ROC, SHAP values, hyperparamètres XGBoost	Bar grouped, Scatter (ROC), Bar horizontal
💡 Recommandations	3 leviers actionnables, impact financier, ROI par levier	Cards HTML, Bar grouped, KPI cards
🎛️ Filtres Disponibles (Sidebar)
Filtre	Type	Valeur par défaut	Impact
Seuil de risque churn	Slider [0.0 – 1.0]	0.70	Ligne de seuil sur l’histogramme des scores + zones colorées
Segment client	Multiselect	Tous	Filtrage par cluster K-Means (Champions / One-shot)
📊 Données & Métriques Clés
Les données sont simulées à partir des résultats réels des phases 1 à 4 du projet (seed fixe np.random.seed(42) pour la reproductibilité) :

Métrique	Valeur réelle
Commandes totales	99 441
Clients uniques	93 358
Taux de churn	96.9%
Taux repeat purchase	3.1%
Score satisfaction moyen	4.16 / 5
Taux livraisons en retard	6.8%
Clients zone rouge (score ≥ 0.70)	10 966
AUC-ROC XGBoost	0.977
🤖 Modèle XGBoost — Configuration
>>>>>>> a972d35c668de2dabc8e291631dc536eddb849fd
XGBClassifier(
    learning_rate = 0.1,
    max_depth     = 6,
    n_estimators  = 200,
<<<<<<< HEAD
    # + SMOTE pour rééquilibrage des classes (66% churn / 34% non-churn)
    # + GridSearchCV 5-fold (40 combinaisons testées)
)
```

**SHAP Features les plus importantes :**

| Rang | Feature | SHAP moyen | Interprétation |
|------|---------|------------|----------------|
| #1 | `purchase_month` | 4.15 | Saisonnalité — pic Q4, creux Q1 |
| #2 | `Cluster_KMeans` | 1.08 | Segment RFM — Champions vs One-shot |
| #3 | `total_freight` | 0.62 | Coût de livraison élevé → churn |
| #4 | `delivery_days` | 0.38 | Délai de livraison |
| #5 | `delivery_delta` | 0.35 | Retard vs estimation |

---

## 💰 Recommandations & Impact Financier

| # | Levier | CA Additionnel | Coût Estimé | ROI | Délai |
|---|--------|---------------|-------------|-----|-------|
| 1 | 🔴 Campagne Réengagement (coupon R$ 25) | R$ 1 499 000 | R$ 280 000 | **×5.4** | 1–3 mois |
| 2 | 🟡 Optimisation Livraison (SLA 10j) | R$ 420 000 | R$ 150 000 | **×2.8** | 3–6 mois |
| 3 | 🟢 Programme Fidélité Olist+ | R$ 800 000 | R$ 200 000 | **×4.0** | 6–12 mois |

**Potentiel total : R$ 2 719 000 · CA récupérable si churn −10% : R$ 1 499 000**

---

## 📄 Livrables Associés

| Livrable | Fichier | Description |
|----------|---------|-------------|
| Dashboard | `app.py` | Application Streamlit — 7 vues interactives |
| Plan A/B Test | `rapport_ab_test.tex` / `.pdf` | Document 2 pages — protocole expérimental complet |
| Dépendances | `requirements.txt` | Packages Python requis |

---

## 🎨 Design System

| Élément | Couleur | Usage |
|---------|---------|-------|
| Primary | `#6366f1` (indigo) | Graphiques principaux, accents |
| Success | `#10b981` (vert) | KPIs positifs, zone verte |
| Danger | `#ef4444` (rouge) | Churn, alertes, zone rouge |
| Warning | `#f59e0b` (ambre) | Risque modéré, délais |
| Cyan | `#06b6d4` | Métriques secondaires |
| Background | `#0d0f1a` | Fond principal dark |
| Card | `#1a1d35` | Fond des cartes KPI |

---

## 📄 Licence

Projet académique — usage interne.  
Dataset source : [Kaggle — Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)
=======
    # + SMOTE pour rééquilibrage des classes
    # + GridSearchCV avec 5-fold CV
)
SHAP Features les plus importantes :

purchase_month — Saisonnalité (impact #1, SHAP moyen = 4.15)
Cluster_KMeans — Segment RFM (impact #2, SHAP moyen = 1.08)
total_freight — Coût de livraison (impact #3, SHAP moyen = 0.62)
delivery_days + delivery_delta — Délai et retard
💰 Recommandations & Impact Financier
#	Levier	CA Additionnel	Coût Estimé	ROI	Délai
1	Campagne Réengagement (coupon R$ 25)	R$ 1 499 000	R$ 280 000	×5.4	1-3 mois
2	Optimisation Livraison (SLA 10j)	R$ 420 000	R$ 150 000	×2.8	3-6 mois
3	Programme Fidélité Olist+	R$ 800 000	R$ 200 000	×4.0	6-12 mois
🎨 Design System
Élément	Couleur	Usage
Primary	#6366f1 (indigo)	Graphiques principaux, accents
Success	#10b981 (vert)	KPIs positifs, zone verte
Danger	#ef4444 (rouge)	Churn, alertes, zone rouge
Warning	#f59e0b (ambre)	Risque modéré, délais
Cyan	#06b6d4	Métriques secondaires
Background	#0d0f1a	Fond principal dark
Card	#1a1d35	Fond des cartes
📄 Licence
Projet académique — usage interne ENSIAS.
Dataset source : Kaggle — Brazilian E-Commerce Public Dataset by Olist
>>>>>>> a972d35c668de2dabc8e291631dc536eddb849fd
