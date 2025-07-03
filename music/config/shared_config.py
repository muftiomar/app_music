# Configuration partagée pour la plateforme musicale

## Endpoints et Ports
KAFKA_BOOTSTRAP_SERVERS = "localhost:9092"
HDFS_NAMENODE_URL = "http://localhost:9870"
SPARK_MASTER_URL = "local[*]"
API_HOST = "0.0.0.0"
API_PORT = 5000

## Topics Kafka
KAFKA_TOPICS = {
    "music_events": "music-events",
    "user_interactions": "user-interactions", 
    "system_metrics": "system-metrics"
}

## Schema des données musicales
MUSIC_EVENT_SCHEMA = {
    "event_id": "string",
    "user_id": "string",
    "track_id": "string",
    "artist": "string",
    "title": "string",
    "genre": "string",
    "duration_ms": "integer",
    "platform": "string",  # spotify, apple_music, youtube, etc.
    "device": "string",     # mobile, desktop, smart_speaker
    "event_type": "string", # play, pause, skip, like, share
    "timestamp": "timestamp",
    "location": {
        "country": "string",
        "city": "string"
    }
}

## Chemins HDFS
HDFS_PATHS = {
    "raw_data": "/music/raw/",
    "processed_data": "/music/processed/",
    "analytics": "/music/analytics/"
}

## Métriques à calculer
ANALYTICS_METRICS = [
    "top_artists_by_plays",
    "top_genres_by_hour", 
    "plays_by_country",
    "user_engagement_by_platform",
    "peak_listening_hours"
]
