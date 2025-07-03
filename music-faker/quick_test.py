#!/usr/bin/env python3
"""
Script de test rapide pour le pipeline temps réel
"""
import subprocess
import time
import sys
import os
from threading import Thread

def run_producer(duration=60):
    """Lance le producteur pour une durée donnée"""
    print(f"🎵 Démarrage producteur pour {duration}s...")
    cmd = [
        sys.executable, "producer/music_producer.py",
        "-n", "200",  # 200 événements
        "-d", "0.3"   # Un événement toutes les 0.3s (≈3/sec)
    ]
    proc = subprocess.Popen(cmd, cwd=".")
    time.sleep(duration)
    proc.terminate()
    print("✅ Producteur arrêté")

def run_consumer(duration=60):
    """Lance le consommateur pour une durée donnée"""
    print(f"📥 Démarrage consommateur pour {duration}s...")
    cmd = [
        sys.executable, "consumer/kafka_hdfs_consumer.py",
        "-m", "batch",
        "-b", "5"
    ]
    proc = subprocess.Popen(cmd, cwd=".")
    time.sleep(duration)
    proc.terminate()
    print("✅ Consommateur arrêté")

def main():
    print("🧪 Test rapide du pipeline temps réel")
    print("=" * 50)
    
    # Démarrer le consommateur en arrière-plan
    consumer_thread = Thread(target=run_consumer, args=(70,), daemon=True)
    consumer_thread.start()
    
    # Attendre un peu puis démarrer le producteur
    time.sleep(5)
    producer_thread = Thread(target=run_producer, args=(60,), daemon=True)
    producer_thread.start()
    
    print("📊 Vous pouvez maintenant lancer le dashboard :")
    print("   python app.py")
    print()
    print("🔗 Dashboard : http://localhost:5000")
    print("🔗 HDFS WebUI : http://localhost:9870")
    print()
    print("⏰ Test en cours pendant 70 secondes...")
    
    # Attendre que tout se termine
    producer_thread.join()
    consumer_thread.join()
    
    print("✅ Test terminé ! Vérifiez les données dans HDFS.")

if __name__ == "__main__":
    main()
