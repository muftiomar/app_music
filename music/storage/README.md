# 🗄️ Storage & HDFS

## 🎯 Objectif
Architecturer et gérer le stockage des données musicales dans un DataLake HDFS.

## 📋 Tâches principales
- [ ] Configuration HDFS et Hadoop
- [ ] Stratégie de partitioning des données
- [ ] Schémas Hive pour requêtes SQL
- [ ] Gestion des métadonnées

## 🛠️ Technologies
- HDFS/Hadoop
- Apache Hive
- Format Parquet/Delta Lake
- Spark SQL

## 📁 Structure des fichiers
```
storage/
├── hdfs_config/
│   ├── core-site.xml          # Configuration HDFS
│   └── hdfs-site.xml          # Paramètres HDFS
├── hive_schemas.sql           # Définition des tables Hive
├── partitioning_strategy.py   # Logique de partitioning
├── data_ingestion.py          # Scripts d'ingestion batch
└── metadata_manager.py        # Gestion des métadonnées
```

## 🚀 Quick Start
```bash
cd storage/
# Démarrer HDFS
./start-hdfs.sh
# Créer les tables Hive
hive -f hive_schemas.sql
```

## 📊 Structure des données
```
/music/
├── raw/                       # Données brutes from Kafka
│   ├── music_events/          # Événements d'écoute
│   ├── user_interactions/     # Likes, partages, playlists
│   └── system_metrics/        # Métriques de performance
├── processed/                 # Données nettoyées et agrégées
│   ├── daily_top_artists/     # Top artistes par jour
│   ├── hourly_genre_stats/    # Stats genres par heure
│   ├── country_platform_stats/ # Stats par pays/plateforme
│   └── user_engagement/       # Métriques d'engagement
└── analytics/                 # Analyses avancées
    ├── dashboard/             # Données pour dashboard
    ├── reports/               # Rapports générés
    └── ml_features/           # Features pour ML
```

## 🚀 Installation et utilisation

### Démarrage rapide
```bash
cd storage/
chmod +x start_storage.sh
./start_storage.sh
```

### Installation manuelle
```bash
cd storage/
pip install -r requirements.txt
```

## 📋 Fonctionnalités implémentées

### ✅ Infrastructure HDFS
- Configuration automatique des répertoires
- Intégration avec Docker Hadoop existant
- Gestion des métadonnées et partitioning
- Support Parquet avec compression Snappy

### ✅ Schémas de données
- **Tables brutes** : music_events, user_interactions, system_metrics
- **Tables agrégées** : daily_top_artists, hourly_genre_stats, country_platform_stats
- **Partitioning** : Par année/mois/jour pour optimiser les requêtes
- **Format** : Parquet pour performance optimale

### ✅ Gestionnaire HDFS
- Classe `HDFSManager` pour toutes les opérations
- Mode simulation si HDFS indisponible
- Lecture/écriture Parquet automatique
- Gestion des erreurs robuste

### ✅ Scripts d'ingestion
- Générateur de données d'exemple réalistes
- Tests complets du pipeline
- Validation de l'intégrité des données
- Support batch et streaming

## 🛠️ Utilisation détaillée

### 1. Démarrer l'infrastructure
```bash
./start_storage.sh
# Choisir option 1: Démarrer Hadoop
```

### 2. Créer la structure HDFS
```bash
./start_storage.sh
# Choisir option 2: Créer structure HDFS
```

### 3. Initialiser les tables Hive
```bash
./start_storage.sh
# Choisir option 3: Créer tables Hive
```

### 4. Tester l'ingestion
```bash
./start_storage.sh
# Choisir option 4: Test d'ingestion
```

### Utilisation programmatique
```python
from hdfs_manager import HDFSManager
import pandas as pd

# Initialiser le gestionnaire
hdfs = HDFSManager()

# Créer la structure
hdfs.create_directory_structure()

# Écrire des données
data = pd.DataFrame([...])
hdfs.write_parquet_data(data, "music_events")

# Lire des données
events = hdfs.read_parquet_data("music_events")

# Informations sur les tables
info = hdfs.get_table_info("music_events")
```

## 📊 Schémas de données

### Événements musicaux
```sql
CREATE TABLE music_events (
    event_id STRING,
    user_id STRING,
    track_id STRING,
    artist STRING,
    title STRING,
    genre STRING,
    event_type STRING,  -- play, pause, skip, like
    timestamp TIMESTAMP,
    country STRING,
    platform STRING     -- Spotify, Apple Music, etc.
)
PARTITIONED BY (year INT, month INT, day INT)
```

### Interactions utilisateur
```sql
CREATE TABLE user_interactions (
    interaction_id STRING,
    user_id STRING,
    track_id STRING,
    interaction_type STRING,  -- like, share, playlist
    timestamp TIMESTAMP,
    metadata MAP<STRING, STRING>
)
PARTITIONED BY (year INT, month INT, day INT)
```

## 🔧 Configuration

### Variables d'environnement
```bash
HDFS_HOST=localhost
HDFS_PORT=9000
HIVE_HOST=localhost
HIVE_PORT=10000
```

### Chemins HDFS configurés
- **Données brutes** : `/music/raw/`
- **Données traitées** : `/music/processed/`
- **Analytics** : `/music/analytics/`
- **Temporaire** : `/music/temp/`

## 🐛 Dépannage

### HDFS non disponible
Le système fonctionne en mode simulation :
```bash
./start_storage.sh
# Option 5: Générer données d'exemple
```

### Problèmes Docker
```bash
# Vérifier le statut
docker ps | grep hadoop

# Redémarrer si nécessaire
docker-compose restart namenode datanode
```

### Erreurs de dépendances
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Vérifier la connectivité HDFS
```bash
# Interface web Namenode
curl http://localhost:9870

# Via le script
./start_storage.sh  # Option 6
```

## 📈 Performance et optimisation

### Partitioning
- **Par date** : Optimise les requêtes temporelles
- **Format Parquet** : Compression et lecture rapide
- **Compression Snappy** : Équilibre taille/vitesse

### Rétention des données
- **Données brutes** : 90 jours
- **Données traitées** : 1 an
- **Analytics** : 2 ans

## 🔗 Intégration avec les autres composants

### Avec le Producer (Personne 1)
```python
# Le producer utilise ces schémas pour Kafka
from storage.hdfs_config import HDFS_PATHS
```

### Avec le Consumer (Personne 2)
```python
# Le consumer écrit directement en HDFS
hdfs.write_parquet_data(kafka_data, "music_events")
```

### Avec Analytics (Personne 4)
```python
# Analytics lit depuis HDFS
events = hdfs.read_parquet_data("music_events", start_date, end_date)
```
