# 🌊 Streaming & Kafka

## 🎯 Objectif
Gérer le flux de données en temps réel entre les producers et le stockage via Kafka et Spark Streaming.

## 📋 Tâches principales
- [ ] Configuration et déploiement de Kafka
- [ ] Consumer Spark Streaming pour ingestion
- [ ] Gestion des erreurs et retry logic
- [ ] Monitoring du pipeline streaming

## 🛠️ Technologies
- Apache Kafka
- Spark Streaming (PySpark)
- Docker Compose pour Kafka
- Kafka Manager pour monitoring

## 📁 Structure des fichiers
```
streaming/
├── kafka_config/
│   ├── docker-compose.yml     # Cluster Kafka
│   └── server.properties      # Configuration Kafka
├── spark_consumer.py          # Consumer Spark Streaming
├── monitoring.py              # Métriques et alertes
├── error_handler.py           # Gestion des erreurs
└── requirements.txt           # Dépendances Python
```

## 🚀 Quick Start
```bash
cd streaming/
docker-compose up -d           # Démarrer Kafka
python spark_consumer.py       # Lancer le consumer
```

## 📊 Topics Kafka
- `music-events`: Événements d'écoute principaux
- `user-interactions`: Likes, partages, playlists
- `system-metrics`: Métriques de performance
