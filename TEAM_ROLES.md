# Répartition des rôles - Plateforme Musicale

## 👥 Équipe de 4 personnes

### 🎵 **Personne 1 - Data Producer & Simulation**
**Responsabilités :**
- Simulateur d'événements musicaux (Python)
- Schema des données (JSON/Avro)
- API de collecte en temps réel
- Tests de charge et performance

**Livrables :**
- Script Python de simulation
- Documentation du format de données
- API REST pour injection de données
- Tests unitaires

**Technologies :**
- Python (Flask/FastAPI)
- Faker pour données fictives
- Requests pour envoi vers Kafka

---

### 🌊 **Personne 2 - Streaming & Kafka**
**Responsabilités :**
- Configuration cluster Kafka
- Topics et partitioning strategy
- Consumer Spark Streaming
- Gestion des erreurs et monitoring

**Livrables :**
- Configuration Kafka (docker-compose)
- Consumer Spark Streaming
- Scripts de monitoring
- Documentation d'architecture streaming

**Technologies :**
- Apache Kafka
- Spark Streaming
- Python/Scala
- Kafka Connect (optionnel)

---

### 🗄️ **Personne 3 - Stockage & HDFS**
**Responsabilités :**
- Architecture DataLake HDFS
- Partitioning des données (par date/genre)
- Intégration Hive/Spark SQL
- Gestion des métadonnées

**Livrables :**
- Configuration HDFS
- Schema Hive tables
- Scripts d'ingestion batch
- Documentation architecture stockage

**Technologies :**
- HDFS/Hadoop
- Apache Hive
- Parquet/Delta Lake
- Spark SQL

---

### 📊 **Personne 4 - Analytics & Frontend**
**Responsabilités :**
- Traitement batch (métriques business)
- APIs pour servir les données
- Dashboard frontend
- Visualisations interactives

**Livrables :**
- Jobs Spark/Hive pour analytics
- API REST (Flask/FastAPI)
- Frontend (React/Flask+Jinja)
- Graphiques et KPIs

**Technologies :**
- Spark SQL/Python
- Flask/FastAPI/React
- Chart.js/D3.js
- Bootstrap/Material-UI

---

## 🔄 Interface entre les rôles

### Contrats de données :
1. **Producer → Kafka** : Schema JSON défini
2. **Kafka → HDFS** : Format Parquet partitionné
3. **HDFS → Analytics** : Tables Hive structurées
4. **Analytics → Frontend** : API REST standardisée

### Meetings de synchronisation :
- **Daily standup** (15 min) : avancement et blocages
- **Weekly review** : démos et ajustements
- **Integration sessions** : tests bout-en-bout

---

## 🎯 Planning suggéré

### Semaine 1 : Setup & Architecture
- Tous : Setup environnement (Docker, repo Git)
- Définition des contrats de données
- POC minimal bout-en-bout

### Semaine 2 : Développement parallèle
- Chacun développe sa partie
- Tests unitaires
- Documentation

### Semaine 3 : Intégration & Tests
- Assemblage des composants
- Tests de performance
- Debug et optimisation

### Semaine 4 : Frontend & Finalisation
- Dashboard final
- Documentation globale
- Préparation soutenance

---

## 📋 Checklist commune

### Pour tous :
- [ ] Code versionné sur Git
- [ ] Documentation technique
- [ ] Tests (unitaires minimum)
- [ ] Containerisation Docker
- [ ] Monitoring/logs basiques

### Intégration :
- [ ] Pipeline bout-en-bout fonctionnel
- [ ] Données test cohérentes
- [ ] Performance acceptable
- [ ] Interface utilisateur intuitive

---

## 📁 Organisation des dossiers

### Structure de travail recommandée :
```
music/                          # ← Dossier principal du projet
├── producer/                   # 👤 Personne 1 - Data Producer
│   ├── music_simulator.py
│   ├── api_collector.py
│   ├── data_schemas.py
│   └── tests/
├── streaming/                  # 👤 Personne 2 - Kafka & Streaming  
│   ├── kafka_config/
│   ├── spark_consumer.py
│   ├── monitoring.py
│   └── docker-compose.kafka.yml
├── storage/                    # 👤 Personne 3 - HDFS & Storage
│   ├── hdfs_config/
│   ├── hive_schemas.sql
│   ├── ingestion_scripts/
│   └── data_partitioning.py
├── analytics/                  # 👤 Personne 4 - Analytics
│   ├── spark_jobs/
│   ├── metrics_calculator.py
│   └── api_backend.py
├── frontend/                   # 👤 Personne 4 - Frontend
│   ├── dashboard.py           # ou React app
│   ├── static/
│   └── templates/
├── config/                     # Configuration partagée
│   ├── shared_config.py
│   └── environment.yml
└── docs/                       # Documentation commune
    ├── architecture.md
    └── api_documentation.md
```

### Pourquoi cette organisation ?

✅ **Séparation claire** : Chaque personne a son dossier principal
✅ **Dossier existant** : Réutilise la structure `music/` déjà créée  
✅ **Configuration partagée** : `config/` pour les éléments communs
✅ **Documentation centralisée** : `docs/` pour les schémas et spécifications

---
