# 🎵 Data Producer & Simulation

## 🎯 Objectif
Générer des événements musicaux réalistes et les envoyer vers Kafka en temps réel.

## 📋 Tâches principales
- [ ] Simulateur d'événements musicaux (plays, likes, skips)
- [ ] API de collecte de données en temps réel
- [ ] Validation et formatage des données
- [ ] Tests de charge

## 🛠️ Technologies
- Python (Flask/FastAPI)
- Kafka Producer
- Faker pour données fictives
- Pandas pour manipulation de données

## 📁 Structure des fichiers
```
producer/
├── music_simulator.py      # Générateur principal d'événements
├── api_collector.py        # API REST pour collecte
├── data_schemas.py         # Définition des schémas de données
├── kafka_producer.py       # Client Kafka
├── tests/                  # Tests unitaires
│   ├── test_simulator.py
│   └── test_api.py
└── requirements.txt        # Dépendances Python
```

## 🚀 Quick Start
```bash
cd producer/
pip install -r requirements.txt
python music_simulator.py
```

## 📊 Format des données générées
Voir `../config/shared_config.py` pour le schéma complet des événements musicaux.

### Responsabilités :
- Générer des événements musicaux réalistes
- Respecter le format JSON défini dans `../config/shared_config.md`
- Envoyer les données vers Kafka
- Gérer la fréquence d'envoi (temps réel simulé)

### Exemples d'événements à générer :
- Écoutes de musique (event_type: "play")
- Likes (event_type: "like") 
- Partages (event_type: "share")
- Skips (event_type: "skip")

### Technologies suggérées :
- `faker` pour générer des données réalistes
- `kafka-python` pour l'envoi vers Kafka
- `uuid` pour les identifiants uniques
- `datetime` pour les timestamps
