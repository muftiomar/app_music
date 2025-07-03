#!/usr/bin/env python3
"""
Test final du pipeline temps réel
"""
import subprocess
import time
import json
import requests
from datetime import datetime

def test_complete_pipeline():
    print("🚀 Test pipeline complet - Démarrage")
    
    # 1. Nettoyer et démarrer un consommateur dédié
    print("🧹 Nettoyage des processus existants...")
    subprocess.run("pkill -f kafka_hdfs_consumer", shell=True)
    time.sleep(2)
    
    # 2. Démarrer consommateur avec nouveau group_id
    group_id = f"test_consumer_{int(time.time())}"
    print(f"🔄 Démarrage consommateur avec groupe: {group_id}")
    
    consumer_cmd = [
        "python", "music-faker/consumer/kafka_hdfs_consumer.py",
        "-m", "batch", "-b", "2"
    ]
    
    # Modifier temporairement le consommateur
    with open("music-faker/consumer/kafka_hdfs_consumer.py", "r") as f:
        content = f.read()
    
    # Remplacer le group_id et auto_offset_reset
    modified_content = content.replace(
        "group_id=f'music_hdfs_batch_consumer_{datetime.now().strftime(\"%H%M%S\")}'",
        f"group_id='{group_id}'"
    ).replace(
        "auto_offset_reset='latest'",
        "auto_offset_reset='latest'"
    )
    
    with open("music-faker/consumer/kafka_hdfs_consumer.py", "w") as f:
        f.write(modified_content)
    
    # Démarrer le consommateur
    consumer_proc = subprocess.Popen(consumer_cmd)
    time.sleep(3)
    
    try:
        # 3. Générer des événements de test
        print("🎵 Génération d'événements test...")
        subprocess.run([
            "python", "music-faker/producer/music_producer.py",
            "-n", "8", "-d", "0.3"
        ])
        
        # 4. Attendre le traitement
        print("⏱️ Attente traitement (15s)...")
        time.sleep(15)
        
        # 5. Vérifier HDFS
        result = subprocess.run([
            "docker", "exec", "music-faker-namenode-1", 
            "hdfs", "dfs", "-ls", "-t", "/music_events/year=2025/month=07/day=03/"
        ], capture_output=True, text=True)
        
        files = result.stdout.strip().split('\n')
        new_files = [f for f in files if '2025-07-03 18:' in f]
        
        print(f"📁 Nouveaux fichiers HDFS détectés: {len(new_files)}")
        
        # 6. Vérifier dashboard
        print("📊 Test dashboard...")
        response = requests.get("http://localhost:5001/api/stats?refresh=true", timeout=20)
        data = response.json()
        
        print(f"✅ Résultats dashboard:")
        print(f"   - Événements: {data['total_events']}")
        print(f"   - Artistes: {data['unique_artists']}")
        print(f"   - Dernière MAJ: {data['last_update']}")
        
        if data['total_events'] > 2:
            print("🎉 SUCCÈS! Pipeline temps réel fonctionnel!")
            return True
        else:
            print("⚠️ Pipeline partiellement fonctionnel")
            return False
            
    finally:
        # Nettoyer
        consumer_proc.terminate()
        
        # Restaurer le fichier original
        with open("music-faker/consumer/kafka_hdfs_consumer.py", "w") as f:
            f.write(content)

if __name__ == "__main__":
    test_complete_pipeline()
