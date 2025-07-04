-- Schémas Hive pour la plateforme musicale
-- Base de données principale
CREATE DATABASE IF NOT EXISTS music_platform;
USE music_platform;

-- Table des événements musicaux (données brutes)
CREATE TABLE IF NOT EXISTS music_events (
    event_id STRING,
    user_id STRING,
    track_id STRING,
    artist STRING,
    title STRING,
    album STRING,
    genre STRING,
    duration_ms BIGINT,
    platform STRING,
    device STRING,
    event_type STRING,
    timestamp TIMESTAMP,
    country STRING,
    city STRING,
    latitude DOUBLE,
    longitude DOUBLE,
    session_id STRING,
    volume_level INT,
    playback_position_ms BIGINT,
    sent_at TIMESTAMP
)
PARTITIONED BY (
    year INT,
    month INT,
    day INT
)
STORED AS PARQUET
LOCATION '/music/raw/music_events/'
TBLPROPERTIES (
    'parquet.compression'='SNAPPY',
    'transactional'='false'
);

-- Table des interactions utilisateur
CREATE TABLE IF NOT EXISTS user_interactions (
    interaction_id STRING,
    user_id STRING,
    track_id STRING,
    interaction_type STRING,
    timestamp TIMESTAMP,
    platform STRING,
    device STRING,
    metadata MAP<STRING, STRING>,
    sent_at TIMESTAMP
)
PARTITIONED BY (
    year INT,
    month INT,
    day INT
)
STORED AS PARQUET
LOCATION '/music/raw/user_interactions/'
TBLPROPERTIES (
    'parquet.compression'='SNAPPY',
    'transactional'='false'
);

-- Table des métriques système
CREATE TABLE IF NOT EXISTS system_metrics (
    metric_id STRING,
    platform STRING,
    metric_type STRING,
    value DOUBLE,
    timestamp TIMESTAMP,
    server_region STRING,
    load_balancer STRING,
    sent_at TIMESTAMP
)
PARTITIONED BY (
    year INT,
    month INT,
    day INT
)
STORED AS PARQUET
LOCATION '/music/raw/system_metrics/'
TBLPROPERTIES (
    'parquet.compression'='SNAPPY',
    'transactional'='false'
);

-- Tables agrégées pour les analytics (données traitées)

-- Top artistes par jour
CREATE TABLE IF NOT EXISTS daily_top_artists (
    artist STRING,
    play_count BIGINT,
    unique_users BIGINT,
    total_duration_hours DOUBLE,
    avg_skip_rate DOUBLE,
    date_partition DATE
)
PARTITIONED BY (date_partition)
STORED AS PARQUET
LOCATION '/music/processed/daily_top_artists/'
TBLPROPERTIES (
    'parquet.compression'='SNAPPY',
    'transactional'='false'
);

-- Genres par tranche horaire
CREATE TABLE IF NOT EXISTS hourly_genre_stats (
    genre STRING,
    hour_of_day INT,
    play_count BIGINT,
    unique_users BIGINT,
    avg_duration_ms BIGINT,
    date_partition DATE
)
PARTITIONED BY (date_partition)
STORED AS PARQUET
LOCATION '/music/processed/hourly_genre_stats/'
TBLPROPERTIES (
    'parquet.compression'='SNAPPY',
    'transactional'='false'
);

-- Écoutes par pays et plateforme
CREATE TABLE IF NOT EXISTS country_platform_stats (
    country STRING,
    platform STRING,
    play_count BIGINT,
    unique_users BIGINT,
    unique_tracks BIGINT,
    total_duration_hours DOUBLE,
    date_partition DATE
)
PARTITIONED BY (date_partition)
STORED AS PARQUET
LOCATION '/music/processed/country_platform_stats/'
TBLPROPERTIES (
    'parquet.compression'='SNAPPY',
    'transactional'='false'
);

-- Engagement utilisateur
CREATE TABLE IF NOT EXISTS user_engagement_metrics (
    user_id STRING,
    total_plays BIGINT,
    total_listening_time_hours DOUBLE,
    skip_rate DOUBLE,
    like_rate DOUBLE,
    unique_artists INT,
    unique_genres INT,
    favorite_genre STRING,
    favorite_platform STRING,
    date_partition DATE
)
PARTITIONED BY (date_partition)
STORED AS PARQUET
LOCATION '/music/processed/user_engagement/'
TBLPROPERTIES (
    'parquet.compression'='SNAPPY',
    'transactional'='false'
);

-- Vue pour les analytics temps réel
CREATE VIEW IF NOT EXISTS real_time_dashboard AS
SELECT 
    DATE(timestamp) as date,
    HOUR(timestamp) as hour,
    COUNT(*) as total_events,
    COUNT(DISTINCT user_id) as active_users,
    COUNT(DISTINCT artist) as unique_artists,
    genre,
    platform,
    event_type
FROM music_events 
WHERE year = YEAR(CURRENT_DATE())
  AND month = MONTH(CURRENT_DATE())
  AND day = DAY(CURRENT_DATE())
GROUP BY DATE(timestamp), HOUR(timestamp), genre, platform, event_type;
