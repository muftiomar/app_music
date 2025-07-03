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
│   └── year=2025/month=07/day=03/
├── processed/                 # Données nettoyées
│   └── year=2025/month=07/day=03/
└── analytics/                 # Métriques calculées
    └── year=2025/month=07/day=03/
```
