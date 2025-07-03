# TODO - Répartition des Tâches

## Répartition Suggérée par Composant

### 👤 Personne 1 - Producer & Kafka
**Dossier** : `producer/`
**Responsabilités** :
- Créer le simulateur d'événements musicaux
- Configurer Kafka
- Générer des données réalistes (écoutes, likes, partages)
- Format des événements JSON

### 👤 Personne 2 - Consumer & Streaming
**Dossier** : `consumer/`
**Responsabilités** :
- Développer le consumer Spark Streaming
- Ingestion depuis Kafka vers HDFS
- Nettoyage et enrichissement des données
- Gestion des erreurs et monitoring

### 👤 Personne 3 - Traitement Batch
**Dossier** : `batch_processing/`
**Responsabilités** :
- Scripts Spark SQL / Hive
- Calcul des métriques analytiques
- Optimisation des requêtes
- Sauvegarde des résultats

### 👤 Personne 4 - Frontend & API
**Dossier** : `frontend/`
**Responsabilités** :
- Interface web (Flask ou React)
- API pour servir les métriques
- Graphiques et visualisations
- Design et UX

### 👤 Personne 5 - Architecture & Documentation
**Dossier** : `docs/`
**Responsabilités** :
- Justification choix d'architecture (Partie 1)
- Schémas et diagrammes (Partie 2)
- Documentation technique
- Coordination générale

## Fichiers à Créer par Équipe

### Producer (Personne 1)
- [ ] `producer/music_event_generator.py`
- [ ] `producer/kafka_producer.py`
- [ ] `producer/config.py`

### Consumer (Personne 2)
- [ ] `consumer/spark_streaming_consumer.py`
- [ ] `consumer/data_cleaner.py`
- [ ] `consumer/hdfs_writer.py`

### Batch Processing (Personne 3)
- [ ] `batch_processing/metrics_calculator.py`
- [ ] `batch_processing/spark_jobs.py`
- [ ] `batch_processing/hive_queries.sql`

### Frontend (Personne 4)
- [ ] `frontend/app.py` (Flask) ou setup React
- [ ] `frontend/api.py`
- [ ] `frontend/templates/` ou `frontend/src/`

### Documentation (Personne 5)
- [ ] `docs/architecture_choice.md`
- [ ] `docs/pipeline_schema.md`
- [ ] `docs/setup_instructions.md`

## Coordination

### Points de Synchronisation
1. **Format des données** : Le Producer doit définir le schéma JSON
2. **API des métriques** : Batch Processing et Frontend doivent s'accorder
3. **Configuration** : Partager les configs Kafka, HDFS, etc.

### Réunions Suggérées
- [ ] Kick-off : Définir les formats de données
- [ ] Mi-parcours : Vérifier l'intégration
- [ ] Finale : Tests end-to-end
