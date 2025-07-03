# Consumer - Spark Streaming

## TODO pour cette partie

### Fichiers à créer :
1. `spark_streaming_consumer.py` - Consumer principal
2. `data_cleaner.py` - Nettoyage des données
3. `hdfs_writer.py` - Écriture vers HDFS

### Responsabilités :
- Consommer les événements depuis Kafka
- Nettoyer et valider les données
- Enrichir avec des métadonnées si nécessaire
- Sauvegarder vers HDFS en format optimisé (Parquet)

### Pipeline de traitement :
1. Lecture depuis Kafka topic `music-events-raw`
2. Validation du format JSON
3. Nettoyage des données incohérentes
4. Enrichissement (géolocalisation, etc.)
5. Sauvegarde vers HDFS

### Technologies suggérées :
- `pyspark` pour le streaming
- `pyspark.sql` pour les transformations
- `hdfs3` pour l'écriture HDFS
