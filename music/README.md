# Plateforme Musicale Connectée

## Description du Projet
Plateforme qui collecte des données d'écoute musicales en temps réel (titre, utilisateur, timestamp, genre, durée, plateforme, device, etc.).

## Architecture du Projet

### Structure des Dossiers
```
music/
├── producer/          # Générateur d'événements musicaux (écoutes, likes, partages)
├── consumer/          # Consumer Spark Streaming pour ingestion en temps réel
├── batch_processing/  # Traitement batch avec Spark/Hive pour métriques
├── frontend/          # Interface web (React ou Flask) avec graphiques
├── config/           # Fichiers de configuration
└── docs/             # Documentation et schémas d'architecture
```

## Composants du Pipeline

### 1. Producer (Partie 3)
- Simulateur d'événements musicaux
- Génération de données : écoutes, likes, partages
- Envoi vers Kafka

### 2. Consumer Streaming (Partie 3)
- Spark Streaming ou équivalent
- Ingestion dans DataLake (HDFS)
- Nettoyage et enrichissement initial

### 3. Traitement Batch (Partie 3)
- Spark SQL / Hive
- Calcul des métriques :
  - Artistes les plus écoutés
  - Genres préférés par tranche horaire
  - Écoutes par pays/plateforme

### 4. Frontend (Partie 4)
- Tableau de bord avec graphiques
- React + Chart.js ou Flask + Charts
- Backend pour lecture des métriques

## Questions Centrales à Traiter

### Partie 1 - Choix d'Architecture
- **Question** : DataLake, DataWarehouse ou Lakehouse ?
- **Livrables** :
  - Diapositive avec justification et schéma
  - Explication écrite (1 page max)

### Partie 2 - Schéma de Traitement
- **Livrables** :
  - Schéma illustré complet
  - Liens entre composants
  - Description des flux

## Technologies Utilisées
- **Streaming** : Kafka + Spark Streaming
- **Stockage** : HDFS (DataLake)
- **Traitement** : Spark SQL, Hive
- **Frontend** : React/Flask + Charts
- **Containerisation** : Docker

## Installation et Utilisation
TODO : Instructions d'installation et de démarrage

## Équipe et Répartition
TODO : Définir les rôles de chaque membre
