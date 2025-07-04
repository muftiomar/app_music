#!/usr/bin/env python3
"""
Script de vérification de santé pour les services avant de lancer le dashboard
"""
import subprocess
import requests
import time
import sys

def check_docker_container(container_name):
    """Vérifier l'état d'un conteneur Docker"""
    try:
        result = subprocess.run(['docker', 'inspect', container_name, '--format={{.State.Health.Status}}'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            status = result.stdout.strip()
            print(f"📦 {container_name}: {status}")
            return status == "healthy"
        else:
            print(f"❌ {container_name}: non trouvé")
            return False
    except Exception as e:
        print(f"❌ Erreur vérification {container_name}: {e}")
        return False

def check_hdfs_api():
    """Vérifier l'API REST HDFS"""
    try:
        response = requests.get("http://localhost:9870/webhdfs/v1/?op=LISTSTATUS", timeout=5)
        if response.status_code == 200:
            print("✅ API REST HDFS: OK")
            return True
        else:
            print(f"❌ API REST HDFS: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ API REST HDFS: {e}")
        return False

def check_music_data():
    """Vérifier la présence de données musicales"""
    try:
        response = requests.get("http://localhost:9870/webhdfs/v1/music_events?op=LISTSTATUS", timeout=5)
        if response.status_code == 200:
            data = response.json()
            folders = len(data["FileStatuses"]["FileStatus"])
            print(f"📊 Données musicales: {folders} dossiers trouvés")
            return folders > 0
        else:
            print(f"❌ Données musicales: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Données musicales: {e}")
        return False

def main():
    print("🔍 Vérification de santé des services...")
    
    # Vérifier les conteneurs
    containers = ['namenode', 'datanode']
    container_ok = all(check_docker_container(container) for container in containers)
    
    if not container_ok:
        print("\n⚠️  Certains conteneurs ne sont pas sains. Tentative de redémarrage...")
        for container in containers:
            if not check_docker_container(container):
                print(f"🔄 Redémarrage de {container}...")
                subprocess.run(['docker', 'restart', container])
        
        print("⏳ Attente de 30 secondes pour la stabilisation...")
        time.sleep(30)
    
    # Vérifier l'API HDFS
    api_ok = check_hdfs_api()
    if not api_ok:
        print("❌ L'API HDFS n'est pas accessible")
        sys.exit(1)
    
    # Vérifier les données
    data_ok = check_music_data()
    if not data_ok:
        print("⚠️  Aucune donnée musicale trouvée")
    
    print("\n✅ Vérification terminée. Services prêts pour le dashboard!")

if __name__ == '__main__':
    main()
