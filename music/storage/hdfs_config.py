"""
Configuration HDFS pour la plateforme musicale
"""
import os
from pathlib import Path

# Configuration HDFS
HDFS_HOST = "localhost"
HDFS_PORT = 9000
HDFS_URL = f"hdfs://{HDFS_HOST}:{HDFS_PORT}"

# Configuration Hive
HIVE_HOST = "localhost"
HIVE_PORT = 10000
HIVE_DATABASE = "music_platform"

# Structure des répertoires HDFS
HDFS_BASE_PATH = "/music"

HDFS_PATHS = {
    # Données brutes (streaming)
    "raw": {
        "base": f"{HDFS_BASE_PATH}/raw",
        "music_events": f"{HDFS_BASE_PATH}/raw/music_events",
        "user_interactions": f"{HDFS_BASE_PATH}/raw/user_interactions", 
        "system_metrics": f"{HDFS_BASE_PATH}/raw/system_metrics"
    },
    
    # Données traitées (batch processing)
    "processed": {
        "base": f"{HDFS_BASE_PATH}/processed",
        "daily_top_artists": f"{HDFS_BASE_PATH}/processed/daily_top_artists",
        "hourly_genre_stats": f"{HDFS_BASE_PATH}/processed/hourly_genre_stats",
        "country_platform_stats": f"{HDFS_BASE_PATH}/processed/country_platform_stats",
        "user_engagement": f"{HDFS_BASE_PATH}/processed/user_engagement"
    },
    
    # Analytics et agrégations
    "analytics": {
        "base": f"{HDFS_BASE_PATH}/analytics",
        "dashboard": f"{HDFS_BASE_PATH}/analytics/dashboard",
        "reports": f"{HDFS_BASE_PATH}/analytics/reports",
        "ml_features": f"{HDFS_BASE_PATH}/analytics/ml_features"
    },
    
    # Données temporaires
    "temp": {
        "base": f"{HDFS_BASE_PATH}/temp",
        "staging": f"{HDFS_BASE_PATH}/temp/staging",
        "checkpoints": f"{HDFS_BASE_PATH}/temp/checkpoints"
    }
}

# Stratégie de partitioning
PARTITION_STRATEGY = {
    "music_events": ["year", "month", "day"],
    "user_interactions": ["year", "month", "day"],
    "system_metrics": ["year", "month", "day"],
    "daily_top_artists": ["date_partition"],
    "hourly_genre_stats": ["date_partition"],
    "country_platform_stats": ["date_partition"],
    "user_engagement": ["date_partition"]
}

# Configuration Spark
SPARK_CONFIG = {
    "spark.app.name": "MusicPlatform",
    "spark.master": "local[*]",
    "spark.sql.warehouse.dir": f"{HDFS_URL}/user/hive/warehouse",
    "spark.sql.catalogImplementation": "hive",
    "spark.serializer": "org.apache.spark.serializer.KryoSerializer",
    "spark.sql.adaptive.enabled": "true",
    "spark.sql.adaptive.coalescePartitions.enabled": "true",
    "spark.sql.parquet.compression.codec": "snappy"
}

# Configuration des formats de fichiers
FILE_FORMATS = {
    "raw_data": "parquet",
    "processed_data": "parquet", 
    "analytics": "parquet",
    "compression": "snappy"
}

# Rétention des données (en jours)
DATA_RETENTION = {
    "raw_events": 90,        # 3 mois de données brutes
    "processed_daily": 365,  # 1 an de données traitées
    "analytics": 730,        # 2 ans d'analytics
    "temp_data": 7           # 1 semaine de données temporaires
}
