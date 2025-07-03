# 🎵 Pipeline Temps Réel de Données Musicales - OPÉRATIONNEL ✅

## 🎯 État du Projet : FONCTIONNEL

✅ **Pipeline complet opérationnel** : Production → Kafka → HDFS → Dashboard  
✅ **Dashboard web temps réel** : http://localhost:5001  
✅ **Visualisation interactive** avec auto-refresh  
✅ **API REST complète** pour intégrations  

## 🚀 Démarrage Rapide

### 1. Démarrer l'infrastructure
```bash
cd music-faker
./start_services.sh
```

### 2. Tester le pipeline complet
```bash
# Démonstration complète (recommandé)
python demo_pipeline.py

# OU test rapide
python test_realtime.py
```

### 3. Générer des événements temps réel
```bash
# Flux continu (recommandé pour démo)
python producer_realtime.py -n 20 -d 1

# Lot unique
python producer/music_producer.py -n 50 -d 0.5
```

### 4. Consommation vers HDFS
```bash
# Mode batch (optimisé)
python consumer/kafka_hdfs_consumer.py -m batch -b 5

# Mode temps réel
python consumer/kafka_hdfs_consumer.py -m realtime
```

## 🌐 Accès Dashboard

- **Interface Web** : http://localhost:5001
- **API Stats** : http://localhost:5001/api/stats
- **API Temps Réel** : http://localhost:5001/api/realtime_metrics
- **Santé** : http://localhost:5001/health

## 📊 APIs Disponibles

### GET /api/stats
```json
{
  "total_events": 12,
  "unique_artists": 11,
  "unique_tracks": 11,
  "unique_users": 11,
  "last_update": "20:11:16"
}
```

### GET /api/realtime_metrics
```json
{
  "status": "ok",
  "total_events": 12,
  "data_freshness": "fresh",
  "timestamp": "2025-07-03T20:11:16"
}
```

## 🔧 Architecture Technique

```
Producer (Python) 
    ↓ 
Kafka (Docker)
    ↓
Consumer (Python)
    ↓
HDFS (Docker)
    ↓
Dashboard Flask
    ↓
Interface Web (HTML/JS)
```

## 📁 Structure des Données HDFS

```
/music_events/
├── year=2025/
│   └── month=07/
│       └── day=03/
│           ├── batch_20250703_200803.jsonl
│           ├── batch_20250703_200747.jsonl
│           └── ...
```

### Format JSON des Événements
```json
{
  "user": "eric04",
  "artist": "Carol Moore", 
  "track": "MediumAquaMarine Nights - Live",
  "timestamp": "2025-07-03T20:07:50.691643",
  "genre": "Jazz",
  "duration": 146,
  "platform": "Spotify",
  "device": "Desktop", 
  "action": "like",
  "country": "FR"
}
```

## 🎮 Scripts Disponibles

| Script | Description | Usage |
|--------|-------------|-------|
| `start_services.sh` | Démarre Docker Compose | `./start_services.sh` |
| `producer_realtime.py` | Producteur temps réel | `python producer_realtime.py -n 10` |
| `demo_pipeline.py` | Démo complète | `python demo_pipeline.py` |
| `test_realtime.py` | Test pipeline | `python test_realtime.py` |
| `app.py` | Dashboard Flask | Démarré automatiquement |

## 🔍 Monitoring

### Vérifier les services Docker
```bash
docker-compose ps
```

### Voir les fichiers HDFS
```bash
docker exec music-faker-namenode-1 hdfs dfs -ls -R /music_events
```

### Consulter les messages Kafka
```bash
docker exec music-faker-kafka-1 kafka-console-consumer --bootstrap-server localhost:9092 --topic music_events --from-beginning --max-messages 5
```

### Logs en temps réel
```bash
# Dashboard
curl -s http://localhost:5001/api/stats | jq .

# HDFS Web UI
open http://localhost:9871

# Kafka
docker logs music-faker-kafka-1 --tail 20
```

## 📈 Métriques Temps Réel

Le dashboard se met à jour automatiquement toutes les 5 secondes et affiche :

- 📊 **Nombre total d'événements**
- 🎤 **Artistes uniques**  
- 🎧 **Tracks uniques**
- 👥 **Utilisateurs uniques**
- 🌍 **Distribution géographique**
- 📱 **Plateformes populaires**
- 🎵 **Genres musicaux**
- ⚡ **Indicateurs temps réel**

## 🛠️ Dépannage

### Dashboard ne répond pas
```bash
# Redémarrer le dashboard
docker-compose restart flask-app
```

### Aucun événement dans HDFS
```bash
# Vérifier le consommateur
python consumer/kafka_hdfs_consumer.py -m batch -b 3

# Regénérer des événements
python producer_realtime.py -n 10 -d 1
```

### HDFS inaccessible
```bash
# Redémarrer HDFS
docker-compose restart namenode datanode
```

## 🎉 Validation Réussie

✅ **Production d'événements** : Kafka reçoit les messages  
✅ **Consommation HDFS** : Fichiers créés et stockés  
✅ **Lecture dashboard** : Données affichées en temps réel  
✅ **Interface web** : Visualisation interactive  
✅ **APIs fonctionnelles** : Endpoints répondent correctement  

**Le pipeline temps réel est entièrement opérationnel ! 🚀**
