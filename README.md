# 🛒 Olist Churn & LTV Dashboard

**Projet Data-Driven Decision Making · Phase 5 & 6**  
Membre 3 — Data Storyteller & Décision Analyst

---

## 🚀 Lancement

```bash
# 1. Installer les dépendances
pip install -r requirements.txt

# 2. Lancer le dashboard
streamlit run app.py
```

Le dashboard s'ouvre automatiquement sur `http://localhost:8501`

---

## 📊 Contenu du Dashboard (5 vues)

| Page | Contenu |
|------|---------|
| 📊 Vue Générale | KPIs globaux, CA mensuel, géographie, comportement temporel |
| 🔴 Analyse du Churn | Scores churn, zones de risque, satisfaction vs retard, clusters RFM |
| 🤖 Modèles ML | Comparaison des 3 modèles, courbes ROC, SHAP values, hyperparamètres |
| 💡 Recommandations | 3 recommandations actionnables avec impact financier estimé |
| 🧪 Plan A/B Test | Design expérimental, calcul taille d'échantillon, règle de décision |

---

## 🎯 Question Décisionnelle

> *Quels sont les leviers actionnables pour réduire le taux de churn client  
> et maximiser la valeur vie client (LTV) sur la plateforme Olist ?*

---

## 📁 Fichiers

```
dashboard/
├── app.py              ← Dashboard principal Streamlit
├── requirements.txt    ← Dépendances Python
└── README.md           ← Ce fichier
```

---

## 🔑 Résultats Clés

- **Taux de churn** : 96.9% (97% des clients n'achètent qu'une fois)
- **Meilleur modèle** : XGBoost — AUC-ROC = 0.977, F1 = 0.938
- **Levier #1** : Mois d'achat (saisonnalité) — impact SHAP le plus élevé
- **ROI potentiel** : R$ 1 499 000 de CA additionnel si churn réduit de 10%

---

*Dataset : Olist Brazilian E-commerce (Kaggle) · 96 478 commandes · 93 358 clients*
