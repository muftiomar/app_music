#!/usr/bin/env python3
"""
Test script pour vérifier le pipeline temps réel complet
"""
import subprocess
import time
import json
import requests

def reset_kafka_offsets():
    """Reset des offsets Kafka pour le consommateur"""
    print("🔄 Reset des offsets Kafka...")
    cmd = "docker exec music-faker-kafka-1 kafka-consumer-groups --bootstrap-server localhost:9092 --group music_hdfs_batch_consumer --reset-offsets --to-latest --topic music_events --execute"
    subprocess.run(cmd.split(), capture_output=True)

def generate_test_events():
    """Génère des événements de test"""
    print("🎵 Génération d'événements test...")
    subprocess.run([
        "python", "music-faker/producer/music_producer.py", 
        "-n", "20", "-d", "0.2"
    ])

def start_consumer():
    """Démarre le consommateur en arrière-plan"""
    print("🔄 Démarrage du consommateur...")
    return subprocess.Popen([
        "python", "music-faker/consumer/kafka_hdfs_consumer.py", 
        "-m", "batch", "-b", "3"
    ])

def check_dashboard():
    """Vérifie les stats du dashboard"""
    print("📊 Vérification du dashboard...")
    try:
        response = requests.get("http://localhost:5001/api/stats", timeout=5)
        data = response.json()
        print(f"✅ Dashboard: {data['total_events']} événements")
        return data['total_events']
    except Exception as e:
        print(f"❌ Erreur dashboard: {e}")
        return 0

def main():
    print("🚀 Test pipeline temps réel complet")
    
    # 1. Reset offsets
    reset_kafka_offsets()
    
    # 2. Démarrage consommateur
    consumer_proc = start_consumer()
    time.sleep(2)
    
    # 3. Génération d'événements
    generate_test_events()
    
    # 4. Attendre traitement
    print("⏱️ Attente traitement (10s)...")
    time.sleep(10)
    
    # 5. Vérifier dashboard
    events_count = check_dashboard()
    
    # 6. Nettoyer
    consumer_proc.terminate()
    
    if events_count > 0:
        print(f"🎉 Succès! Pipeline fonctionnel avec {events_count} événements")
    else:
        print("❌ Échec: aucun événement détecté")

if __name__ == "__main__":
    main()
