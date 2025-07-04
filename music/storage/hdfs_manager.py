"""
Gestionnaire HDFS pour la plateforme musicale
"""
import os
import logging
from datetime import datetime, date
from typing import List, Dict, Any, Optional
import pandas as pd
from pathlib import Path

try:
    from hdfs3 import HDFileSystem
    HDFS_AVAILABLE = True
except ImportError:
    HDFS_AVAILABLE = False
    logging.warning("hdfs3 non disponible - mode simulation activé")

try:
    from pyspark.sql import SparkSession
    from pyspark.sql.types import *
    SPARK_AVAILABLE = True
except ImportError:
    SPARK_AVAILABLE = False
    logging.warning("PySpark non disponible")

from hdfs_config import HDFS_URL, HDFS_PATHS, PARTITION_STRATEGY, SPARK_CONFIG

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HDFSManager:
    """Gestionnaire pour les opérations HDFS"""
    
    def __init__(self, hdfs_url: str = HDFS_URL):
        """
        Initialise le gestionnaire HDFS
        
        Args:
            hdfs_url: URL du cluster HDFS
        """
        self.hdfs_url = hdfs_url
        self.fs = None
        self.spark = None
        
        if HDFS_AVAILABLE:
            try:
                self.fs = HDFileSystem(host='localhost', port=9000)
                logger.info("Connexion HDFS établie")
            except Exception as e:
                logger.error(f"Erreur connexion HDFS: {e}")
                self.fs = None
        
        if SPARK_AVAILABLE:
            try:
                self.spark = SparkSession.builder \
                    .appName("MusicPlatformStorage") \
                    .config("spark.sql.catalogImplementation", "hive") \
                    .enableHiveSupport() \
                    .getOrCreate()
                logger.info("Session Spark créée")
            except Exception as e:
                logger.error(f"Erreur création Spark: {e}")
                self.spark = None
    
    def create_directory_structure(self) -> bool:
        """
        Crée la structure de répertoires HDFS
        
        Returns:
            bool: True si succès, False sinon
        """
        try:
            directories_to_create = []
            
            # Collecter tous les chemins à créer
            for category, paths in HDFS_PATHS.items():
                if isinstance(paths, dict):
                    for path_name, path_value in paths.items():
                        directories_to_create.append(path_value)
                else:
                    directories_to_create.append(paths)
            
            if self.fs:
                # Créer avec HDFS
                for directory in directories_to_create:
                    try:
                        if not self.fs.exists(directory):
                            self.fs.makedirs(directory)
                            logger.info(f"Répertoire créé: {directory}")
                        else:
                            logger.debug(f"Répertoire existant: {directory}")
                    except Exception as e:
                        logger.error(f"Erreur création {directory}: {e}")
                        return False
            else:
                # Mode simulation - créer localement
                local_base = Path("./hdfs_simulation")
                for directory in directories_to_create:
                    local_path = local_base / directory.lstrip('/')
                    local_path.mkdir(parents=True, exist_ok=True)
                    logger.info(f"Répertoire simulé créé: {local_path}")
            
            logger.info("Structure de répertoires créée avec succès")
            return True
            
        except Exception as e:
            logger.error(f"Erreur lors de la création des répertoires: {e}")
            return False
    
    def write_parquet_data(self, data: pd.DataFrame, table_name: str, 
                          partition_date: Optional[date] = None) -> bool:
        """
        Écrit des données au format Parquet avec partitioning
        
        Args:
            data: DataFrame à écrire
            table_name: Nom de la table
            partition_date: Date pour le partitioning
            
        Returns:
            bool: True si succès, False sinon
        """
        try:
            if partition_date is None:
                partition_date = date.today()
            
            # Ajouter les colonnes de partition
            if table_name in ["music_events", "user_interactions", "system_metrics"]:
                data['year'] = partition_date.year
                data['month'] = partition_date.month
                data['day'] = partition_date.day
                partition_path = f"year={partition_date.year}/month={partition_date.month}/day={partition_date.day}"
            else:
                data['date_partition'] = partition_date
                partition_path = f"date_partition={partition_date}"
            
            # Déterminer le chemin de destination
            if table_name == "music_events":
                base_path = HDFS_PATHS["raw"]["music_events"]
            elif table_name == "user_interactions":
                base_path = HDFS_PATHS["raw"]["user_interactions"]
            elif table_name == "system_metrics":
                base_path = HDFS_PATHS["raw"]["system_metrics"]
            elif table_name in HDFS_PATHS["processed"]:
                base_path = HDFS_PATHS["processed"][table_name]
            else:
                logger.error(f"Table inconnue: {table_name}")
                return False
            
            full_path = f"{base_path}/{partition_path}"
            
            if self.spark and SPARK_AVAILABLE:
                # Utiliser Spark pour l'écriture
                spark_df = self.spark.createDataFrame(data)
                spark_df.write \
                    .mode("overwrite") \
                    .option("compression", "snappy") \
                    .parquet(full_path)
                logger.info(f"Données écrites via Spark: {full_path}")
            else:
                # Mode simulation - écriture locale
                local_base = Path("./hdfs_simulation")
                local_path = local_base / full_path.lstrip('/')
                local_path.mkdir(parents=True, exist_ok=True)
                
                # Sauvegarder en Parquet
                parquet_file = local_path / "data.parquet"
                data.to_parquet(parquet_file, compression='snappy')
                logger.info(f"Données simulées écrites: {parquet_file}")
            
            return True
            
        except Exception as e:
            logger.error(f"Erreur écriture données {table_name}: {e}")
            return False
    
    def read_parquet_data(self, table_name: str, 
                         start_date: Optional[date] = None,
                         end_date: Optional[date] = None) -> Optional[pd.DataFrame]:
        """
        Lit des données Parquet avec filtrage par date
        
        Args:
            table_name: Nom de la table
            start_date: Date de début (optionnel)
            end_date: Date de fin (optionnel)
            
        Returns:
            DataFrame ou None si erreur
        """
        try:
            if table_name == "music_events":
                base_path = HDFS_PATHS["raw"]["music_events"]
            elif table_name == "user_interactions":
                base_path = HDFS_PATHS["raw"]["user_interactions"]
            elif table_name == "system_metrics":
                base_path = HDFS_PATHS["raw"]["system_metrics"]
            elif table_name in HDFS_PATHS["processed"]:
                base_path = HDFS_PATHS["processed"][table_name]
            else:
                logger.error(f"Table inconnue: {table_name}")
                return None
            
            if self.spark and SPARK_AVAILABLE:
                # Lire avec Spark
                df = self.spark.read.parquet(base_path)
                
                # Filtrer par date si spécifié
                if start_date:
                    df = df.filter(df.date_partition >= start_date)
                if end_date:
                    df = df.filter(df.date_partition <= end_date)
                
                return df.toPandas()
            else:
                # Mode simulation - lecture locale
                local_base = Path("./hdfs_simulation")
                local_path = local_base / base_path.lstrip('/')
                
                if local_path.exists():
                    # Lire tous les fichiers parquet dans le répertoire
                    parquet_files = list(local_path.rglob("*.parquet"))
                    if parquet_files:
                        dfs = [pd.read_parquet(f) for f in parquet_files]
                        combined_df = pd.concat(dfs, ignore_index=True)
                        logger.info(f"Données simulées lues: {len(combined_df)} lignes")
                        return combined_df
                
                logger.warning(f"Aucune donnée trouvée pour {table_name}")
                return pd.DataFrame()
                
        except Exception as e:
            logger.error(f"Erreur lecture données {table_name}: {e}")
            return None
    
    def get_table_info(self, table_name: str) -> Dict[str, Any]:
        """
        Récupère les informations sur une table
        
        Args:
            table_name: Nom de la table
            
        Returns:
            Dictionnaire avec les infos de la table
        """
        try:
            if table_name in HDFS_PATHS["raw"]:
                path = HDFS_PATHS["raw"][table_name]
                category = "raw"
            elif table_name in HDFS_PATHS["processed"]:
                path = HDFS_PATHS["processed"][table_name]
                category = "processed"
            else:
                return {"error": f"Table {table_name} non trouvée"}
            
            info = {
                "table_name": table_name,
                "category": category,
                "hdfs_path": path,
                "partition_strategy": PARTITION_STRATEGY.get(table_name, []),
                "format": "parquet",
                "compression": "snappy"
            }
            
            # Ajouter des stats si possible
            if self.fs and self.fs.exists(path):
                info["exists"] = True
                # TODO: Ajouter taille, nombre de fichiers, etc.
            else:
                info["exists"] = False
            
            return info
            
        except Exception as e:
            logger.error(f"Erreur récupération info table {table_name}: {e}")
            return {"error": str(e)}
    
    def list_tables(self) -> List[str]:
        """
        Liste toutes les tables disponibles
        
        Returns:
            Liste des noms de tables
        """
        tables = []
        tables.extend(HDFS_PATHS["raw"].keys())
        tables.extend(HDFS_PATHS["processed"].keys())
        return [t for t in tables if t != "base"]
    
    def cleanup_old_data(self, retention_days: int = 90) -> bool:
        """
        Nettoie les anciennes données selon la politique de rétention
        
        Args:
            retention_days: Nombre de jours à conserver
            
        Returns:
            bool: True si succès, False sinon
        """
        try:
            cutoff_date = datetime.now().date() - pd.Timedelta(days=retention_days)
            logger.info(f"Nettoyage des données antérieures à {cutoff_date}")
            
            # TODO: Implémenter le nettoyage réel
            # Pour l'instant, juste un log
            logger.info("Nettoyage simulé - fonctionnalité à implémenter")
            
            return True
            
        except Exception as e:
            logger.error(f"Erreur lors du nettoyage: {e}")
            return False
    
    def close(self):
        """Ferme les connexions"""
        if self.spark:
            self.spark.stop()
            logger.info("Session Spark fermée")
        
        # HDFS3 se ferme automatiquement
        logger.info("Connexions fermées")
