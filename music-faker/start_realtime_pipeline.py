#!/usr/bin/env python3
"""
Script pour démarrer le pipeline temps réel complet
"""
import subprocess
import time
import sys
import os
import signal
from threading import Thread

class RealTimePipeline:
    def __init__(self):
        self.processes = []
        self.running = True
        
    def log(self, message):
        print(f"[{time.strftime('%H:%M:%S')}] {message}")
        
    def start_docker_services(self):
        """Démarre les services Docker (Kafka, HDFS)"""
        self.log("🐳 Démarrage des services Docker...")
        try:
            # Vérifier si les services sont déjà en cours
            result = subprocess.run(["docker-compose", "ps", "--services", "--filter", "status=running"], 
                                  capture_output=True, text=True, cwd=".")
            running_services = set(result.stdout.strip().split('\n')) if result.stdout.strip() else set()
            
            required_services = {"zookeeper", "kafka", "namenode", "datanode"}
            missing_services = required_services - running_services
            
            if missing_services:
                self.log(f"Services manquants: {missing_services}")
                self.log("Démarrage de docker-compose...")
                subprocess.run(["docker-compose", "up", "-d"], check=True, cwd=".")
                
                # Attendre que les services soient prêts
                self.log("⏳ Attente que les services soient prêts...")
                time.sleep(30)
            else:
                self.log("✅ Services Docker déjà en cours d'exécution")
                
        except Exception as e:
            self.log(f"❌ Erreur démarrage Docker: {e}")
            return False
        return True
    
    def start_producer(self, events_per_second=2):
        """Démarre le producteur Kafka en mode continu"""
        self.log(f"🎵 Démarrage du producteur Kafka ({events_per_second} événements/sec)...")
        delay = 1.0 / events_per_second
        
        def run_producer():
            while self.running:
                try:
                    # Produire par petits lots pour éviter la surcharge
                    cmd = [
                        sys.executable, "producer/music_producer.py", 
                        "-n", "10", 
                        "-d", str(delay)
                    ]
                    proc = subprocess.Popen(cmd, cwd=".")
                    self.processes.append(proc)
                    proc.wait()
                    
                    if not self.running:
                        break
                        
                    time.sleep(1)  # Petite pause entre les lots
                    
                except Exception as e:
                    if self.running:
                        self.log(f"⚠️ Erreur producteur: {e}")
                        time.sleep(5)
        
        producer_thread = Thread(target=run_producer, daemon=True)
        producer_thread.start()
        return producer_thread
    
    def start_consumer(self, batch_size=5):
        """Démarre le consommateur Kafka vers HDFS"""
        self.log(f"📥 Démarrage du consommateur Kafka->HDFS (batch={batch_size})...")
        
        def run_consumer():
            while self.running:
                try:
                    cmd = [
                        sys.executable, "consumer/kafka_hdfs_consumer.py",
                        "-m", "batch",
                        "-b", str(batch_size)
                    ]
                    proc = subprocess.Popen(cmd, cwd=".")
                    self.processes.append(proc)
                    proc.wait()
                    
                    if not self.running:
                        break
                        
                    self.log("🔄 Redémarrage du consommateur...")
                    time.sleep(2)
                    
                except Exception as e:
                    if self.running:
                        self.log(f"⚠️ Erreur consommateur: {e}")
                        time.sleep(5)
        
        consumer_thread = Thread(target=run_consumer, daemon=True)
        consumer_thread.start()
        return consumer_thread
    
    def start_dashboard(self):
        """Démarre le dashboard Flask"""
        self.log("🌐 Démarrage du dashboard Flask...")
        
        def run_dashboard():
            try:
                # Utiliser le port 5001 pour éviter les conflits
                env = os.environ.copy()
                env['FLASK_ENV'] = 'development'
                
                cmd = [sys.executable, "app.py"]
                proc = subprocess.Popen(cmd, cwd=".", env=env)
                self.processes.append(proc)
                proc.wait()
                
            except Exception as e:
                self.log(f"❌ Erreur dashboard: {e}")
        
        dashboard_thread = Thread(target=run_dashboard, daemon=True)
        dashboard_thread.start()
        return dashboard_thread
    
    def cleanup(self):
        """Nettoie tous les processus"""
        self.log("🧹 Nettoyage des processus...")
        self.running = False
        
        for proc in self.processes:
            try:
                if proc.poll() is None:
                    proc.terminate()
                    proc.wait(timeout=5)
            except:
                try:
                    proc.kill()
                except:
                    pass
    
    def run(self):
        """Lance le pipeline complet"""
        try:
            # 1. Démarrer Docker
            if not self.start_docker_services():
                return
            
            # 2. Démarrer le producteur
            producer_thread = self.start_producer(events_per_second=3)
            
            # 3. Démarrer le consommateur  
            consumer_thread = self.start_consumer(batch_size=5)
            
            # 4. Démarrer le dashboard
            dashboard_thread = self.start_dashboard()
            
            self.log("🚀 Pipeline temps réel démarré avec succès!")
            self.log("📊 Dashboard disponible sur: http://localhost:5001")
            self.log("🔥 Génération de 3 événements/seconde")
            self.log("📁 Stockage par lots de 5 dans HDFS")
            self.log("❌ Ctrl+C pour arrêter")
            
            # Attendre l'interruption
            while True:
                time.sleep(1)
                
        except KeyboardInterrupt:
            self.log("🛑 Arrêt demandé par l'utilisateur")
        except Exception as e:
            self.log(f"❌ Erreur fatale: {e}")
        finally:
            self.cleanup()

def signal_handler(signum, frame):
    """Gestionnaire de signal pour arrêt propre"""
    print("\n🛑 Signal d'arrêt reçu...")
    sys.exit(0)

if __name__ == "__main__":
    # Gérer les signaux d'arrêt
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    pipeline = RealTimePipeline()
    pipeline.run()
