"""
Scripts d'ingestion de données pour tests
"""
import json
import logging
from datetime import datetime, date
from typing import Dict, Any, List
import pandas as pd
from pathlib import Path
import random

from hdfs_manager import HDFSManager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataIngestionTester:
    """Classe pour tester l'ingestion de données dans HDFS"""
    
    def __init__(self):
        """Initialise le testeur d'ingestion"""
        self.hdfs_manager = HDFSManager()
        
    def generate_sample_music_events(self, num_events: int = 1000) -> pd.DataFrame:
        """
        Génère des événements musicaux d'exemple
        
        Args:
            num_events: Nombre d'événements à générer
            
        Returns:
            DataFrame avec les événements
        """
        logger.info(f"Génération de {num_events} événements musicaux")
        
        # Données d'exemple
        artists = ["Drake", "Taylor Swift", "The Weeknd", "Billie Eilish", "Ed Sheeran",
                  "Ariana Grande", "Post Malone", "Dua Lipa", "Bad Bunny", "Olivia Rodrigo"]
        
        genres = ["Pop", "Hip-Hop", "R&B", "Electronic", "Rock", "Jazz", "Country", "Reggaeton"]
        
        platforms = ["Spotify", "Apple Music", "YouTube Music", "Amazon Music", "Deezer"]
        
        devices = ["iPhone", "Android Phone", "Desktop", "Laptop", "Smart Speaker"]
        
        event_types = ["play", "pause", "skip", "like", "share", "add_to_playlist"]
        
        countries = ["France", "United States", "United Kingdom", "Germany", "Spain", "Canada"]
        
        cities = {
            "France": ["Paris", "Lyon", "Marseille"],
            "United States": ["New York", "Los Angeles", "Chicago"],
            "United Kingdom": ["London", "Manchester", "Birmingham"],
            "Germany": ["Berlin", "Munich", "Hamburg"],
            "Spain": ["Madrid", "Barcelona", "Valencia"],
            "Canada": ["Toronto", "Vancouver", "Montreal"]
        }
        
        events = []
        for i in range(num_events):
            country = random.choice(countries)
            city = random.choice(cities[country])
            artist = random.choice(artists)
            
            event = {
                "event_id": f"evt_{i:08d}",
                "user_id": f"user_{random.randint(1, 10000):06d}",
                "track_id": f"track_{random.randint(1, 50000):08d}",
                "artist": artist,
                "title": f"{artist} - Song {random.randint(1, 100)}",
                "album": f"{artist} Album",
                "genre": random.choice(genres),
                "duration_ms": random.randint(120000, 300000),  # 2-5 minutes
                "platform": random.choice(platforms),
                "device": random.choice(devices),
                "event_type": random.choice(event_types),
                "timestamp": datetime.now(),
                "country": country,
                "city": city,
                "latitude": round(random.uniform(-90, 90), 6),
                "longitude": round(random.uniform(-180, 180), 6),
                "session_id": f"session_{random.randint(1000000, 9999999)}",
                "volume_level": random.randint(20, 100),
                "playback_position_ms": random.randint(0, 180000),
                "sent_at": datetime.now()
            }
            events.append(event)
        
        return pd.DataFrame(events)
    
    def generate_sample_user_interactions(self, num_interactions: int = 200) -> pd.DataFrame:
        """
        Génère des interactions utilisateur d'exemple
        
        Args:
            num_interactions: Nombre d'interactions à générer
            
        Returns:
            DataFrame avec les interactions
        """
        logger.info(f"Génération de {num_interactions} interactions utilisateur")
        
        interaction_types = ["like", "dislike", "share", "add_to_playlist", "follow_artist"]
        platforms = ["Spotify", "Apple Music", "YouTube Music", "Amazon Music", "Deezer"]
        devices = ["iPhone", "Android Phone", "Desktop", "Laptop", "Smart Speaker"]
        
        interactions = []
        for i in range(num_interactions):
            interaction = {
                "interaction_id": f"int_{i:08d}",
                "user_id": f"user_{random.randint(1, 10000):06d}",
                "track_id": f"track_{random.randint(1, 50000):08d}",
                "interaction_type": random.choice(interaction_types),
                "timestamp": datetime.now(),
                "platform": random.choice(platforms),
                "device": random.choice(devices),
                "metadata": json.dumps({
                    "source": "mobile_app",
                    "version": "1.2.3"
                }),
                "sent_at": datetime.now()
            }
            interactions.append(interaction)
        
        return pd.DataFrame(interactions)
    
    def generate_sample_system_metrics(self, num_metrics: int = 50) -> pd.DataFrame:
        """
        Génère des métriques système d'exemple
        
        Args:
            num_metrics: Nombre de métriques à générer
            
        Returns:
            DataFrame avec les métriques
        """
        logger.info(f"Génération de {num_metrics} métriques système")
        
        platforms = ["Spotify", "Apple Music", "YouTube Music", "Amazon Music", "Deezer"]
        metric_types = ["latency", "error_rate", "concurrent_users", "bandwidth_usage"]
        regions = ["eu-west", "us-east", "asia-pacific"]
        load_balancers = ["lb-01", "lb-02", "lb-03"]
        
        metrics = []
        for i in range(num_metrics):
            metric_type = random.choice(metric_types)
            
            # Valeurs réalistes selon le type de métrique
            if metric_type == "latency":
                value = random.uniform(10, 500)  # ms
            elif metric_type == "error_rate":
                value = random.uniform(0.1, 5.0)  # %
            elif metric_type == "concurrent_users":
                value = random.randint(1000, 100000)
            else:  # bandwidth_usage
                value = random.uniform(1.0, 1000.0)  # Mbps
            
            metric = {
                "metric_id": f"metric_{i:08d}",
                "platform": random.choice(platforms),
                "metric_type": metric_type,
                "value": round(value, 2),
                "timestamp": datetime.now(),
                "server_region": random.choice(regions),
                "load_balancer": random.choice(load_balancers),
                "sent_at": datetime.now()
            }
            metrics.append(metric)
        
        return pd.DataFrame(metrics)
    
    def test_full_ingestion_pipeline(self):
        """
        Test complet du pipeline d'ingestion
        """
        logger.info("🚀 Démarrage du test d'ingestion complet")
        
        try:
            # 1. Créer la structure de répertoires
            logger.info("📁 Création de la structure HDFS...")
            if not self.hdfs_manager.create_directory_structure():
                logger.error("❌ Échec création structure HDFS")
                return False
            
            # 2. Générer des données d'exemple
            logger.info("📊 Génération des données d'exemple...")
            music_events = self.generate_sample_music_events(1000)
            user_interactions = self.generate_sample_user_interactions(200)
            system_metrics = self.generate_sample_system_metrics(50)
            
            # 3. Ingérer les données
            logger.info("💾 Ingestion des données...")
            
            success_events = self.hdfs_manager.write_parquet_data(
                music_events, "music_events", date.today()
            )
            
            success_interactions = self.hdfs_manager.write_parquet_data(
                user_interactions, "user_interactions", date.today()
            )
            
            success_metrics = self.hdfs_manager.write_parquet_data(
                system_metrics, "system_metrics", date.today()
            )
            
            if success_events and success_interactions and success_metrics:
                logger.info("✅ Ingestion réussie pour toutes les tables")
            else:
                logger.warning("⚠️  Échec partiel de l'ingestion")
            
            # 4. Tester la lecture
            logger.info("📖 Test de lecture des données...")
            
            read_events = self.hdfs_manager.read_parquet_data("music_events")
            read_interactions = self.hdfs_manager.read_parquet_data("user_interactions")
            read_metrics = self.hdfs_manager.read_parquet_data("system_metrics")
            
            if read_events is not None and len(read_events) > 0:
                logger.info(f"✅ Lecture événements musicaux: {len(read_events)} lignes")
            else:
                logger.error("❌ Échec lecture événements musicaux")
            
            if read_interactions is not None and len(read_interactions) > 0:
                logger.info(f"✅ Lecture interactions: {len(read_interactions)} lignes")
            else:
                logger.error("❌ Échec lecture interactions")
            
            if read_metrics is not None and len(read_metrics) > 0:
                logger.info(f"✅ Lecture métriques: {len(read_metrics)} lignes")
            else:
                logger.error("❌ Échec lecture métriques")
            
            # 5. Afficher les informations des tables
            logger.info("📋 Informations des tables:")
            for table in self.hdfs_manager.list_tables():
                info = self.hdfs_manager.get_table_info(table)
                logger.info(f"  - {table}: {info}")
            
            logger.info("🎉 Test d'ingestion terminé avec succès !")
            return True
            
        except Exception as e:
            logger.error(f"❌ Erreur lors du test d'ingestion: {e}")
            return False
        
        finally:
            self.hdfs_manager.close()
    
    def test_with_sample_files(self):
        """
        Test avec création de fichiers d'exemple locaux
        """
        logger.info("📁 Création de fichiers d'exemple pour validation")
        
        try:
            # Créer le répertoire de sortie
            output_dir = Path("./sample_data")
            output_dir.mkdir(exist_ok=True)
            
            # Générer et sauvegarder les données
            music_events = self.generate_sample_music_events(500)
            user_interactions = self.generate_sample_user_interactions(100)
            system_metrics = self.generate_sample_system_metrics(25)
            
            # Sauvegarder en CSV pour inspection
            music_events.to_csv(output_dir / "sample_music_events.csv", index=False)
            user_interactions.to_csv(output_dir / "sample_user_interactions.csv", index=False)
            system_metrics.to_csv(output_dir / "sample_system_metrics.csv", index=False)
            
            # Sauvegarder en JSON pour les autres composants
            music_events.to_json(output_dir / "sample_music_events.json", 
                               orient="records", date_format="iso")
            
            logger.info(f"✅ Fichiers d'exemple créés dans {output_dir}")
            
            # Afficher quelques statistiques
            logger.info("📊 Statistiques des données générées:")
            logger.info(f"  - Événements musicaux: {len(music_events)} lignes")
            logger.info(f"  - Artistes uniques: {music_events['artist'].nunique()}")
            logger.info(f"  - Genres uniques: {music_events['genre'].nunique()}")
            logger.info(f"  - Interactions: {len(user_interactions)} lignes")
            logger.info(f"  - Métriques système: {len(system_metrics)} lignes")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Erreur création fichiers d'exemple: {e}")
            return False

def main():
    """Fonction principale de test"""
    print("🎵 TEST D'INGESTION HDFS - PLATEFORME MUSICALE")
    print("=" * 60)
    
    tester = DataIngestionTester()
    
    print("\nOptions disponibles:")
    print("1. Test complet d'ingestion HDFS")
    print("2. Génération de fichiers d'exemple seulement")
    print("3. Test de connexion HDFS")
    
    choice = input("\nVotre choix (1-3): ").strip()
    
    if choice == "1":
        tester.test_full_ingestion_pipeline()
    elif choice == "2":
        tester.test_with_sample_files()
    elif choice == "3":
        hdfs_manager = HDFSManager()
        print(f"HDFS disponible: {hdfs_manager.fs is not None}")
        print(f"Spark disponible: {hdfs_manager.spark is not None}")
        hdfs_manager.close()
    else:
        print("❌ Choix invalide")

if __name__ == "__main__":
    main()
