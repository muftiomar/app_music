#!/usr/bin/env python3
"""
Script de test pour vérifier les données HDFS
"""
import subprocess
import json

def test_hdfs():
    print("🔍 Test de connectivité HDFS...")
    
    # Test de base
    try:
        cmd = "docker exec namenode hdfs dfs -ls /"
        result = subprocess.run(cmd.split(), capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ HDFS accessible")
            print("Contenu racine HDFS:")
            print(result.stdout)
        else:
            print("❌ Erreur HDFS:", result.stderr)
            return False
    except Exception as e:
        print(f"❌ Erreur connexion HDFS: {e}")
        return False
    
    # Test répertoire music_events
    try:
        cmd = "docker exec namenode hdfs dfs -ls -R /music_events/"
        result = subprocess.run(cmd.split(), capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("\n📁 Contenu /music_events/:")
            print(result.stdout)
            
            # Compter les fichiers .jsonl
            files = [line for line in result.stdout.split('\n') if '.jsonl' in line]
            print(f"\n📊 Nombre de fichiers JSONL trouvés: {len(files)}")
            
            if files:
                # Tester lecture d'un fichier
                first_file_line = files[0]
                parts = first_file_line.split()
                if len(parts) >= 8:
                    file_path = parts[-1]
                    print(f"\n🔍 Test lecture du fichier: {file_path}")
                    
                    cmd = f"docker exec namenode hdfs dfs -cat {file_path}"
                    result = subprocess.run(cmd.split(), capture_output=True, text=True, timeout=10)
                    if result.returncode == 0:
                        lines = result.stdout.strip().split('\n')
                        print(f"✅ Fichier lu avec succès: {len(lines)} lignes")
                        if lines and lines[0]:
                            try:
                                event = json.loads(lines[0])
                                print(f"📝 Premier événement: {event.get('artist', 'N/A')} - {event.get('track', 'N/A')}")
                                return True
                            except json.JSONDecodeError:
                                print("❌ Erreur parsing JSON")
                    else:
                        print(f"❌ Erreur lecture fichier: {result.stderr}")
        else:
            print("❌ Répertoire /music_events/ introuvable")
            return False
            
    except Exception as e:
        print(f"❌ Erreur test music_events: {e}")
        return False
    
    return False

if __name__ == "__main__":
    test_hdfs()
