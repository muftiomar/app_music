#!/usr/bin/env python3
"""
Test complet du pipeline music-faker: Producer Kafka -> Consumer HDFS -> Analyse
"""
import subprocess
import time
import sys
import os

def run_command(cmd, description, background=False):
    """Exécute une commande avec gestion d'erreur"""
    print(f"🔄 {description}...")
    try:
        if background:
            process = subprocess.Popen(cmd, shell=True)
            return process
        else:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ {description} - Succès")
                return result
            else:
                print(f"❌ {description} - Erreur: {result.stderr}")
                return None
    except Exception as e:
        print(f"❌ {description} - Exception: {e}")
        return None

def test_kafka_connectivity():
    """Test la connectivité Kafka"""
    print("\n📡 TEST DE CONNECTIVITÉ KAFKA")
    print("-" * 40)
    
    # Vérifier les conteneurs Kafka
    result = run_command("docker ps | grep kafka", "Vérification conteneur Kafka")
    if not result or not result.stdout.strip():
        print("❌ Kafka n'est pas en cours d'exécution")
        return False
    
    print("✅ Kafka est actif")
    return True

def test_hdfs_connectivity():
    """Test la connectivité HDFS"""
    print("\n� TEST DE CONNECTIVITÉ HDFS")
    print("-" * 40)
    
    # Vérifier le namenode
    result = run_command("docker ps | grep namenode", "Vérification namenode HDFS")
    if not result or not result.stdout.strip():
        print("❌ HDFS namenode n'est pas en cours d'exécution")
        return False
    
    print("✅ HDFS est opérationnel")
    return True

def run_pipeline_test(num_events=20):
    """Exécute un test complet du pipeline"""
    print(f"\n🎵 TEST COMPLET DU PIPELINE - {num_events} ÉVÉNEMENTS")
    print("=" * 60)
    
    # Étape 1: Lancer le consumer en arrière-plan
    print("\n🔽 Démarrage du consumer HDFS...")
    consumer_process = subprocess.Popen([
        "python", "consumer/kafka_hdfs_consumer.py", "-m", "batch", "-b", "5"
    ], cwd="/Users/omar/Desktop/datalake/app_music/music-faker")
    
    # Attendre un peu que le consumer démarre
    time.sleep(3)
    
    # Étape 2: Générer des événements avec le producer
    print(f"\n🔼 Génération de {num_events} événements musicaux...")
    producer_cmd = f"python producer/music_producer.py -n {num_events} -d 0.1"
    producer_result = run_command(
        f"cd /Users/omar/Desktop/datalake/app_music/music-faker && {producer_cmd}",
        f"Production de {num_events} événements"
    )
    
    if not producer_result:
        consumer_process.terminate()
        return False
    
    # Étape 3: Attendre que le consumer traite tous les événements
    print("\n⏳ Attente du traitement par le consumer (15 secondes)...")
    time.sleep(15)
    
    # Étape 4: Arrêter le consumer
    print("\n🛑 Arrêt du consumer...")
    consumer_process.terminate()
    consumer_process.wait()
    
    # Étape 5: Vérifier les données dans HDFS
    print("\n🔍 Vérification des données dans HDFS...")
    hdfs_check_cmd = "docker exec namenode hdfs dfs -ls -R /music_events/ | grep batch"
    result = run_command(hdfs_check_cmd, "Listage des fichiers HDFS")
    
    if result and result.stdout.strip():
        files = result.stdout.strip().split('\n')
        print(f"✅ {len(files)} fichiers trouvés dans HDFS")
        return True
    else:
        print("❌ Aucun fichier trouvé dans HDFS")
        return False

def run_analytics_test():
    """Test l'analyseur de données"""
    print("\n📈 TEST DE L'ANALYSEUR DE DONNÉES")
    print("-" * 40)
    
    analytics_cmd = "python analytics/music_analyzer.py"
    result = run_command(
        f"cd /Users/omar/Desktop/datalake/app_music/music-faker && {analytics_cmd}",
        "Exécution de l'analyseur"
    )
    
    return result is not None

def main():
    """Test principal"""
    print("🚀 TEST COMPLET DU PIPELINE MUSIC-FAKER")
    print("=" * 50)
    
    # Tests de connectivité
    kafka_ok = test_kafka_connectivity()
    hdfs_ok = test_hdfs_connectivity()
    
    if not (kafka_ok and hdfs_ok):
        print("\n❌ Les prérequis ne sont pas satisfaits")
        sys.exit(1)
    
    # Test du pipeline complet
    pipeline_ok = run_pipeline_test(num_events=25)
    
    # Test de l'analyseur
    analytics_ok = run_analytics_test()
    
    # Résumé final
    print("\n" + "=" * 60)
    print("📋 RÉSUMÉ DES TESTS")
    print("=" * 60)
    print(f"   🔗 Connectivité Kafka: {'✅' if kafka_ok else '❌'}")
    print(f"   💾 Connectivité HDFS: {'✅' if hdfs_ok else '❌'}")
    print(f"   🔄 Pipeline complet: {'✅' if pipeline_ok else '❌'}")
    print(f"   📊 Analyseur: {'✅' if analytics_ok else '❌'}")
    
    if kafka_ok and hdfs_ok and pipeline_ok and analytics_ok:
        print("\n🎉 TOUS LES TESTS SONT PASSÉS AVEC SUCCÈS!")
        print("\n✨ Le pipeline music-faker est entièrement opérationnel:")
        print("   • Producer Kafka ✅")
        print("   • Consumer HDFS ✅") 
        print("   • Stockage partitionné ✅")
        print("   • Analyseur de données ✅")
    else:
        print("\n⚠️  Certains tests ont échoué")

if __name__ == "__main__":
    main()
