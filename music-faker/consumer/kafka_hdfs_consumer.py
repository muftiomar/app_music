import json
import subprocess
import tempfile
import os
from kafka import KafkaConsumer
from datetime import datetime

KAFKA_TOPIC = "music_events"
KAFKA_SERVER = "127.0.0.1:9092"
HDFS_BASE_PATH = "/music_events"

def ensure_hdfs_directory(hdfs_path):
    """Crée un répertoire HDFS s'il n'existe pas"""
    try:
        cmd = f"docker exec music-faker-namenode-1 hdfs dfs -test -d {hdfs_path}"
        result = subprocess.run(cmd.split(), capture_output=True)
        if result.returncode != 0:
            # Le répertoire n'existe pas, on le crée
            cmd = f"docker exec music-faker-namenode-1 hdfs dfs -mkdir -p {hdfs_path}"
            subprocess.run(cmd.split(), check=True)
            print(f"Répertoire HDFS créé: {hdfs_path}")
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de la création du répertoire HDFS {hdfs_path}: {e}")

def write_event_to_hdfs(event):
    """Écrit un événement directement dans HDFS avec partitionnement par date"""
    # Partitionnement par date (YYYY-MM-DD)
    ts = event.get("timestamp", "")
    date_str = ts[:10] if ts else datetime.now().strftime("%Y-%m-%d")
    
    # Chemin HDFS avec partitionnement
    hdfs_dir = f"{HDFS_BASE_PATH}/year={date_str[:4]}/month={date_str[5:7]}/day={date_str[8:10]}"
    hdfs_file = f"{hdfs_dir}/events_{datetime.now().strftime('%H%M%S')}.jsonl"
    
    # Assurer que le répertoire existe
    ensure_hdfs_directory(hdfs_dir)
    
    # Créer un fichier temporaire local
    with tempfile.NamedTemporaryFile(mode='w', suffix='.jsonl', delete=False) as temp_file:
        temp_file.write(json.dumps(event) + "\n")
        temp_file_path = temp_file.name
    
    try:
        # Copier vers HDFS en ajoutant au fichier existant
        cmd = f"docker exec -i music-faker-namenode-1 hdfs dfs -appendToFile {temp_file_path} {hdfs_file}"
        # Si le fichier n'existe pas, -appendToFile échouera, on utilise -put
        result = subprocess.run(cmd.split(), capture_output=True)
        
        if result.returncode != 0:
            # Le fichier n'existe pas encore, on le crée
            cmd = f"docker exec -i music-faker-namenode-1 hdfs dfs -put {temp_file_path} {hdfs_file}"
            subprocess.run(cmd.split(), check=True)
            print(f"Nouveau fichier HDFS créé: {hdfs_file}")
        else:
            print(f"Événement ajouté à HDFS: {hdfs_file}")
            
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'écriture dans HDFS: {e}")
    finally:
        # Nettoyer le fichier temporaire
        os.unlink(temp_file_path)

def write_batch_to_hdfs(events, batch_size=100):
    """Écrit un lot d'événements dans HDFS pour de meilleures performances"""
    if not events:
        return
        
    # Grouper par date pour le partitionnement
    events_by_date = {}
    for event in events:
        ts = event.get("timestamp", "")
        date_str = ts[:10] if ts else datetime.now().strftime("%Y-%m-%d")
        if date_str not in events_by_date:
            events_by_date[date_str] = []
        events_by_date[date_str].append(event)
    
    # Écrire chaque groupe de date
    for date_str, date_events in events_by_date.items():
        hdfs_dir = f"{HDFS_BASE_PATH}/year={date_str[:4]}/month={date_str[5:7]}/day={date_str[8:10]}"
        hdfs_file = f"{hdfs_dir}/batch_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jsonl"
        
        ensure_hdfs_directory(hdfs_dir)
        
        # Créer fichier temporaire avec tous les événements de la date
        with tempfile.NamedTemporaryFile(mode='w', suffix='.jsonl', delete=False) as temp_file:
            for event in date_events:
                temp_file.write(json.dumps(event, ensure_ascii=False) + "\n")
            temp_file_path = temp_file.name
        
        try:
            # Générer un nom de fichier unique dans le conteneur
            container_temp_path = f"/tmp/music_batch_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jsonl"
            
            # Copier le fichier vers le conteneur
            cmd = ["docker", "cp", temp_file_path, f"music-faker-namenode-1:{container_temp_path}"]
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                print(f"Erreur copie vers conteneur: {result.stderr}")
                continue
            
            # Copier vers HDFS
            cmd = f"docker exec music-faker-namenode-1 hdfs dfs -put {container_temp_path} {hdfs_file}"
            result = subprocess.run(cmd.split(), capture_output=True, text=True)
            if result.returncode != 0:
                print(f"Erreur HDFS put: {result.stderr}")
            else:
                print(f"✅ Batch de {len(date_events)} événements écrit dans HDFS: {hdfs_file}")
            
            # Nettoyer le fichier du conteneur
            cmd = f"docker exec music-faker-namenode-1 rm -f {container_temp_path}"
            subprocess.run(cmd.split(), capture_output=True)
            
        except Exception as e:
            print(f"Erreur lors de l'écriture du batch dans HDFS: {e}")
        finally:
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)

def consume_from_kafka_batch(batch_size=10):
    """Consumer Kafka avec écriture par lot dans HDFS"""
    consumer = KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_SERVER,
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        auto_offset_reset='latest',  # Lire depuis la fin pour les nouveaux messages
        enable_auto_commit=True,
        group_id=f'music_hdfs_batch_consumer_{datetime.now().strftime("%H%M%S")}'  # Nouveau groupe
        # Retirer le timeout pour un processing continu
    )
    
    print(f"Consumer batch connecté à Kafka sur {KAFKA_SERVER}, topic '{KAFKA_TOPIC}'")
    print(f"Écriture dans HDFS par lots de {batch_size} événements")
    print("En attente de messages...")
    
    events_batch = []
    message_count = 0
    
    try:
        for msg in consumer:
            event = msg.value
            events_batch.append(event)
            message_count += 1
            print(f"Message {message_count} reçu: {event.get('artist', 'Unknown')} - {event.get('track', 'Unknown')}")
            
            if len(events_batch) >= batch_size:
                print(f"Traitement d'un lot de {len(events_batch)} événements...")
                write_batch_to_hdfs(events_batch)
                events_batch = []
        
        # Traiter le dernier lot même s'il n'est pas complet
        if events_batch:
            write_batch_to_hdfs(events_batch)
                
    except KeyboardInterrupt:
        print("\nArrêt du consumer...")
        if events_batch:
            print(f"Écriture du dernier lot de {len(events_batch)} événements...")
            write_batch_to_hdfs(events_batch)
    finally:
        consumer.close()

def consume_from_kafka_realtime():
    """Consumer Kafka avec écriture temps réel dans HDFS"""
    consumer = KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_SERVER,
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='music_hdfs_realtime_consumer'
    )
    
    print(f"Consumer temps réel connecté à Kafka sur {KAFKA_SERVER}, topic '{KAFKA_TOPIC}'")
    print("Écriture immédiate dans HDFS pour chaque événement")
    
    try:
        for msg in consumer:
            event = msg.value
            write_event_to_hdfs(event)
            print(f"Événement traité: {event['artist']} - {event['track']}")
    except KeyboardInterrupt:
        print("\nArrêt du consumer...")
    finally:
        consumer.close()

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Consumer Kafka vers HDFS pour événements musicaux")
    parser.add_argument("-m", "--mode", choices=["batch", "realtime"], default="batch", 
                       help="Mode de consommation: batch ou realtime")
    parser.add_argument("-b", "--batch-size", type=int, default=10,
                       help="Taille du lot pour le mode batch")
    
    args = parser.parse_args()
    
    if args.mode == "batch":
        consume_from_kafka_batch(args.batch_size)
    else:
        consume_from_kafka_realtime()
