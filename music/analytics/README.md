# 📊 Analytics & Frontend

## 🎯 Objectif
Calculer les métriques business et créer un dashboard interactif pour visualiser les données musicales.

## 📋 Tâches principales
- [ ] Jobs Spark pour calcul de métriques
- [ ] API REST pour servir les données
- [ ] Dashboard web avec graphiques
- [ ] KPIs en temps réel

## 🛠️ Technologies
- Spark SQL/PySpark
- Flask/FastAPI pour l'API
- React ou Flask+Jinja pour le frontend
- Chart.js/D3.js pour les visualisations

## 📁 Structure des fichiers
```
analytics/
├── spark_jobs/
│   ├── top_artists.py         # Top artistes par période
│   ├── genre_analysis.py      # Analyse par genre
│   └── user_engagement.py     # Métriques d'engagement
├── api_backend.py             # API REST pour le frontend
├── metrics_calculator.py      # Logique de calcul principal
└── requirements.txt           # Dépendances Python
```

## 🚀 Quick Start
```bash
cd analytics/
pip install -r requirements.txt
python api_backend.py          # Lancer l'API
```

## 📈 Métriques calculées
- **Top artistes** : Plus écoutés par jour/semaine/mois
- **Genres populaires** : Par tranche horaire et région
- **Engagement utilisateur** : Taux de skip, likes, partages
- **Pics d'écoute** : Heures de forte activité
- **Analyse géographique** : Écoutes par pays/ville
