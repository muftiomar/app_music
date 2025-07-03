# Producer - Générateur d'Événements Musicaux

## TODO pour cette partie

### Fichiers à créer :
1. `music_event_generator.py` - Simulateur d'événements
2. `kafka_producer.py` - Envoi vers Kafka
3. `config.py` - Configuration du producer

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
