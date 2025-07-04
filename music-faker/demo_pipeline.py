#!/usr/bin/env python3
"""
Démonstration du pipeline temps réel fonctionnel
"""
import subprocess
import time
import requests
import json

def monitor_pipeline():
    print("🚀 DÉMONSTRATION PIPELINE TEMPS RÉEL")
    print("=" * 50)
    
    # Démarrage monitoring
    for i in range(8):  # Monitorer pendant 8 cycles
        print(f"\n📊 Cycle {i+1}/8 - {time.strftime('%H:%M:%S')}")
        
        try:
            # Stats dashboard
            response = requests.get("http://localhost:5001/api/stats", timeout=10)
            stats = response.json()
            
            # Métriques temps réel
            response2 = requests.get("http://localhost:5001/api/realtime_metrics", timeout=5)
            metrics = response2.json()
            
            print(f"   🎵 Événements: {stats['total_events']}")
            print(f"   🎤 Artistes: {stats['unique_artists']}")
            print(f"   🎧 Tracks: {stats['unique_tracks']}")
            print(f"   👥 Utilisateurs: {stats['unique_users']}")
            print(f"   ⏰ Dernière MAJ: {stats['last_update']}")
            print(f"   📈 Statut: {metrics['status']}")
            
            # Vérification HDFS
            result = subprocess.run([
                "docker", "exec", "music-faker-namenode-1",
                "hdfs", "dfs", "-ls", "/music_events/year=2025/month=07/day=03/"
            ], capture_output=True, text=True)
            
            files_count = len([line for line in result.stdout.split('\n') if 'batch_' in line])
            print(f"   📁 Fichiers HDFS: {files_count}")
            
            # Indicateur de progression
            if i == 0:
                baseline_events = stats['total_events']
                print(f"   📋 Baseline: {baseline_events} événements")
            else:
                new_events = stats['total_events'] - baseline_events
                print(f"   📈 Nouveaux: +{new_events} événements")
                
                if new_events > 0:
                    print("   ✅ Pipeline ACTIF")
                else:
                    print("   ⏳ En attente...")
        
        except Exception as e:
            print(f"   ❌ Erreur: {e}")
        
        time.sleep(5)
    
    print("\n🎉 Démonstration terminée!")
    print("🌐 Dashboard web disponible sur: http://localhost:5001")
    print("📊 API Stats: http://localhost:5001/api/stats")
    print("⚡ API Temps réel: http://localhost:5001/api/realtime_metrics")

if __name__ == "__main__":
    monitor_pipeline()
