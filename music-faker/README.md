# 🎵 Music-Faker Dashboard - Pipeline Temps Réel

Dashboard en temps réel pour visualiser les données musicales avec pipeline Kafka → HDFS → Analytics.

## 🚀 Démarrage Rapide

### 1. Démarrer les services Docker
```bash
# Démarrer Kafka + HDFS
./start_services.sh
# ou
docker-compose up -d
```

### 2. Option A : Pipeline Automatique (Recommandé)
```bash
# Lance tout automatiquement : producteur + consommateur + dashboard
python start_realtime_pipeline.py
```

### 3. Option B : Contrôle Manuel

#### Démarrer le producteur Kafka
```bash
# Génère 3 événements/seconde en continu
python producer/music_producer.py -n 1000 -d 0.33
```

#### Démarrer le consommateur HDFS
```bash
# Lit Kafka et écrit dans HDFS par lots de 5
python consumer/kafka_hdfs_consumer.py -m batch -b 5
```

#### Démarrer le dashboard
```bash
python app.py
```

### 4. Test Rapide
```bash
# Test de 60 secondes avec données simulées
python quick_test.py
```

## 📊 Accès aux Interfaces

- **Dashboard Principal** : http://localhost:5001
- **HDFS WebUI** : http://localhost:9871
- **Health Check** : http://localhost:5001/health

## 🎯 Fonctionnalités Temps Réel

- ✅ Auto-refresh toutes les 5 secondes
- ✅ Indicateur LIVE avec animation
- ✅ Contrôles pause/play pour l'auto-refresh
- ✅ Métriques temps réel (événements/minute)
- ✅ Activité récente en streaming
- ✅ Cache intelligent (3 secondes)

## 📈 Métriques Disponibles

- Statistiques générales (événements, utilisateurs, artistes, pistes)
- Top genres, plateformes, actions
- Répartition par pays
- Histogramme des durées d'écoute
- Activité récente (20 derniers événements)
- Streaming temps réel (50 événements les plus récents)

## 🏗️ Architecture

```
[Producteur] → [Kafka] → [Consommateur] → [HDFS] → [Dashboard]
     ↓              ↓            ↓           ↓          ↓
  Fake Data    Topic:         Batch        Partitioned  Real-time
  3 evt/sec   music_events    Write         by Date      Visualization
```

### Composants

1. **🎵 Producer** : Génère des événements musicaux réalistes avec Faker
2. **📊 Kafka** : Message broker pour le streaming temps réel
3. **🔄 Consumer** : Consomme les événements et les stocke dans HDFS
4. **💾 HDFS** : Stockage distribué avec partitionnement par date
5. **📈 Analytics** : Analyse des données et génération de rapports

## 🚀 Démarrage Rapide

### Prérequis

- Docker et Docker Compose
- Python 3.8+
- Environnement configuré avec Kafka et HDFS

### Installation

```bash
# 1. Installer les dépendances Python
pip install -r requirements.txt

# 2. Vérifier que les services Docker sont actifs
docker ps | grep -E "(kafka|namenode)"

# 3. Tester le pipeline complet
python test_pipeline.py
```

## 📁 Structure du Projet

```
music-faker/
├── producer/
│   └── music_producer.py              # Producer Kafka principal
├── consumer/
│   └── kafka_hdfs_consumer.py         # Consumer HDFS principal
├── analytics/
│   └── music_analyzer.py              # Analyseur de données HDFS
├── docker-compose.yml                 # Services Kafka + HDFS
├── requirements.txt                   # Dépendances Python
└── test_pipeline.py                  # Tests complets
```

## 🎯 Utilisation

### 1. Producer Kafka

Génère des événements musicaux et les envoie à Kafka :

```bash
# Générer 100 événements avec délai de 0.5s
python producer/music_producer.py -n 100 -d 0.5

# Générer 1000 événements rapidement
python producer/music_producer.py -n 1000
```

### 2. Consumer HDFS

Consomme les événements Kafka et les stocke dans HDFS :

```bash
# Mode batch (recommandé) - lots de 50 événements
python consumer/kafka_hdfs_consumer.py -m batch -b 50

# Mode temps réel - traitement immédiat
python consumer/kafka_hdfs_consumer.py -m realtime
```

### 3. Pipeline Complet

Pour un test complet automatisé :

```bash
python test_pipeline.py
```

### 4. Analyse des Données

Analyse les données stockées dans HDFS :

```bash
python analytics/music_analyzer.py
```

## 📊 Format des Données

### Événement Musical

```json
{
  "user": "johndoe",
  "artist": "The Beatles",
  "track": "Hey Jude (Remastered)",
  "timestamp": "2025-07-03T14:30:00.123456",
  "genre": "Rock",
  "duration": 420,
  "platform": "Spotify",
  "device": "Mobile",
  "action": "play",
  "country": "US"
}
```

### Partitionnement HDFS

Les données sont stockées avec un partitionnement par date :

```
/music_events/
├── year=2025/
│   ├── month=07/
│   │   ├── day=03/
│   │   │   ├── batch_20250703_143015.jsonl
│   │   │   └── batch_20250703_143020.jsonl
│   │   └── day=04/
│   └── month=08/
```

## 📈 Analytics

L'analyseur génère automatiquement :

### Rapports Texte
- Statistiques générales (utilisateurs, artistes, pistes)
- Top genres, plateformes, actions, pays
- Métriques de durée

### Fichiers CSV
- `music_stats_YYYYMMDD_HHMMSS_genres.csv`
- `music_stats_YYYYMMDD_HHMMSS_platforms.csv`
- `music_stats_YYYYMMDD_HHMMSS_countries.csv`
- `music_stats_YYYYMMDD_HHMMSS_events.csv`

### Visualisations
- Graphiques des top genres
- Répartition par plateforme
- Actions les plus fréquentes
- Distribution des durées

## 🔧 Configuration

### Variables Kafka

```python
KAFKA_TOPIC = "music_events"
KAFKA_SERVER = "127.0.0.1:9092"
```

### Variables HDFS

```python
HDFS_BASE_PATH = "/music_events"
```

## 🧪 Tests

### Test Unitaire

```bash
# Test de connectivité Kafka
python -c "from producer.music_producer import *; produce_to_kafka(5)"

# Test HDFS
docker exec namenode hdfs dfs -ls /music_events/
```

### Test Complet

```bash
python test_pipeline.py
```

Le test vérifie :
- ✅ Connectivité Kafka
- ✅ Connectivité HDFS  
- ✅ Pipeline Producer → Consumer
- ✅ Stockage des données
- ✅ Analyseur de données

## 📦 Dépendances

```
kafka-python>=2.0.2
faker>=19.0.0
pandas>=2.0.0
numpy>=1.24.0
matplotlib>=3.7.0
seaborn>=0.12.0
```

## 🔍 Monitoring

### Vérifier Kafka

```bash
# Topics Kafka
docker exec music-faker-kafka-1 kafka-topics --list --bootstrap-server localhost:9092

# Messages dans le topic
docker exec music-faker-kafka-1 kafka-console-consumer --topic music_events --from-beginning --bootstrap-server localhost:9092
```

### Vérifier HDFS

```bash
# Espace disponible
docker exec namenode hdfs dfsadmin -report

# Contenu des répertoires
docker exec namenode hdfs dfs -ls -R /music_events/

# Contenu d'un fichier
docker exec namenode hdfs dfs -cat /music_events/year=2025/month=07/day=03/batch_*.jsonl
```

## 🚨 Dépannage

### Kafka n'est pas accessible
```bash
docker ps | grep kafka  # Vérifier que le conteneur est actif
docker logs music-faker-kafka-1  # Logs Kafka
```

### HDFS non accessible
```bash
docker ps | grep namenode  # Vérifier namenode
docker exec namenode hdfs dfsadmin -safemode get  # Mode safe
```

### Consumer ne reçoit pas de messages
```bash
# Vérifier le consumer group
docker exec music-faker-kafka-1 kafka-consumer-groups --bootstrap-server localhost:9092 --list
```

## 🎯 Cas d'Usage

### 1. Simulation de Streaming Musical
Génère des données réalistes pour tester des algorithmes de recommandation

### 2. Test de Pipeline Big Data
Valide l'architecture Kafka → HDFS pour des systèmes de production

### 3. Formation Data Engineering
Apprentissage des technologies de streaming et stockage distribué

### 4. Analytics en Temps Réel
Analyse de tendances musicales et comportements utilisateurs

## 🔮 Extensions Possibles

- **Spark Streaming** : Traitement en temps réel
- **Elasticsearch** : Indexation pour recherche
- **Grafana** : Dashboards temps réel
- **Apache Airflow** : Orchestration des pipelines
- **Schema Registry** : Gestion des schémas de données

## 📝 Licence

Ce projet est open source et disponible sous licence MIT.

## ✨ Structure Finale Simplifiée

Le projet a été nettoyé et simplifié avec seulement les fichiers essentiels :

### 📂 Fichiers Principaux
- **`producer/music_producer.py`** : Producer Kafka avec événements musicaux réalistes
- **`consumer/kafka_hdfs_consumer.py`** : Consumer HDFS avec partitionnement automatique
- **`analytics/music_analyzer.py`** : Analyseur complet avec visualisations
- **`test_pipeline.py`** : Tests automatisés du pipeline complet

### 🎯 Utilisation Simplifiée
```bash
# 1. Test complet automatique
python test_pipeline.py

# 2. Utilisation manuelle
python producer/music_producer.py -n 100 &
python consumer/kafka_hdfs_consumer.py -m batch &
python analytics/music_analyzer.py
```

---

**🎵 Profitez de votre pipeline musical ! 🎵**
