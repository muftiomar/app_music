# Configuration Partagée - Plateforme Musicale

## Schéma des Données d'Événements Musicaux

### Format JSON des Événements
```json
{
  "event_id": "uuid4",
  "timestamp": "2025-07-03T14:30:00Z",
  "event_type": "play|like|share|skip",
  "user": {
    "user_id": "string",
    "country": "FR|US|UK|DE|...",
    "age_group": "18-25|26-35|36-45|46-55|55+",
    "subscription_type": "free|premium"
  },
  "track": {
    "track_id": "string",
    "title": "string",
    "artist": "string",
    "album": "string",
    "genre": "pop|rock|hip-hop|electronic|jazz|classical|...",
    "duration_ms": "integer",
    "release_year": "integer"
  },
  "session": {
    "session_id": "string",
    "device_type": "mobile|desktop|tablet|smart_speaker",
    "platform": "spotify|apple_music|youtube_music|deezer",
    "listening_quality": "low|medium|high|lossless"
  },
  "playback": {
    "position_ms": "integer",
    "volume_level": "float (0-1)",
    "was_skipped": "boolean",
    "completion_rate": "float (0-1)"
  }
}
```

## Configuration Kafka

### Topics
- `music-events-raw` : Événements bruts du producer
- `music-events-cleaned` : Événements après nettoyage
- `music-metrics` : Métriques calculées

### Configuration Recommandée
```properties
# Kafka
bootstrap.servers=localhost:9092
num.partitions=3
replication.factor=1

# Producer
acks=1
retries=3
batch.size=16384

# Consumer
group.id=music-platform-consumers
auto.offset.reset=earliest
```

## Configuration HDFS

### Structure des Répertoires
```
/user/music-platform/
├── raw-events/          # Données brutes du streaming
├── cleaned-events/      # Données nettoyées
├── metrics/            # Métriques calculées
│   ├── artists/
│   ├── genres/
│   └── countries/
└── temp/               # Répertoire temporaire
```

## Configuration Spark

### Ressources Recommandées
```properties
spark.sql.adaptive.enabled=true
spark.sql.adaptive.coalescePartitions.enabled=true
spark.sql.adaptive.skewJoin.enabled=true
spark.serializer=org.apache.spark.serializer.KryoSerializer
```

## Variables d'Environnement (.env)

```bash
# Kafka
KAFKA_BOOTSTRAP_SERVERS=localhost:9092
KAFKA_TOPIC_RAW=music-events-raw

# HDFS
HDFS_NAMENODE=localhost:9000
HDFS_BASE_PATH=/user/music-platform

# Spark
SPARK_MASTER=local[*]
SPARK_APP_NAME=MusicPlatform

# Flask
FLASK_ENV=development
FLASK_PORT=5000

# Database (si nécessaire)
DATABASE_URL=sqlite:///music_metrics.db
```
