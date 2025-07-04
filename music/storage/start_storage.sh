#!/bin/bash

# Script de démarrage pour le composant Storage/HDFS
echo "🗄️  Démarrage du composant Storage HDFS"
echo "======================================"

# Vérifier si Python est installé
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 n'est pas installé"
    exit 1
fi

# Aller dans le répertoire storage
cd "$(dirname "$0")"
echo "📁 Répertoire: $(pwd)"

# Vérifier si Docker est en cours d'exécution
if ! docker info &> /dev/null; then
    echo "⚠️  Docker n'est pas en cours d'exécution"
    echo "   Veuillez démarrer Docker avant de continuer"
    exit 1
fi

# Vérifier le statut de Hadoop
echo "🔍 Vérification du statut Hadoop..."
if docker ps | grep -q namenode; then
    echo "✅ Hadoop Namenode est en cours d'exécution"
    HADOOP_RUNNING=true
else
    echo "⚠️  Hadoop Namenode n'est pas en cours d'exécution"
    HADOOP_RUNNING=false
fi

echo ""
echo "Options disponibles:"
echo "1. 🐳 Démarrer l'infrastructure Hadoop (Docker)"
echo "2. 🗄️  Créer la structure HDFS"
echo "3. 📊 Créer les tables Hive"
echo "4. 🧪 Test d'ingestion de données"
echo "5. 📁 Générer des données d'exemple"
echo "6. 🔍 Vérifier le statut HDFS"
echo "7. 🛑 Arrêter Hadoop"

read -p "Votre choix (1-7): " choice

case $choice in
    1)
        echo "🐳 Démarrage de l'infrastructure Hadoop..."
        cd ../../
        docker-compose up -d namenode datanode
        echo "⏳ Attente du démarrage complet (30s)..."
        sleep 30
        echo "✅ Infrastructure Hadoop démarrée"
        echo "🌐 Interface web disponible: http://localhost:9870"
        ;;
    2)
        echo "🗄️  Création de la structure HDFS..."
        python3 -c "
from hdfs_manager import HDFSManager
hdfs = HDFSManager()
success = hdfs.create_directory_structure()
print('✅ Structure créée avec succès' if success else '❌ Échec création structure')
hdfs.close()
"
        ;;
    3)
        echo "📊 Création des tables Hive..."
        if [ "$HADOOP_RUNNING" = true ]; then
            docker exec -i namenode hive -f /myhadoop/music/storage/hive_schemas.sql
        else
            echo "❌ Hadoop n'est pas démarré. Utilisez l'option 1 d'abord."
        fi
        ;;
    4)
        echo "🧪 Test d'ingestion de données..."
        python3 data_ingestion.py
        ;;
    5)
        echo "📁 Génération de données d'exemple..."
        python3 -c "
from data_ingestion import DataIngestionTester
tester = DataIngestionTester()
tester.test_with_sample_files()
"
        ;;
    6)
        echo "🔍 Vérification du statut HDFS..."
        python3 -c "
from hdfs_manager import HDFSManager
hdfs = HDFSManager()
print(f'HDFS connecté: {hdfs.fs is not None}')
print(f'Spark disponible: {hdfs.spark is not None}')
tables = hdfs.list_tables()
print(f'Tables configurées: {len(tables)}')
for table in tables:
    info = hdfs.get_table_info(table)
    print(f'  - {table}: {info.get(\"exists\", \"unknown\")}')
hdfs.close()
"
        ;;
    7)
        echo "🛑 Arrêt de Hadoop..."
        cd ../../
        docker-compose stop namenode datanode
        echo "✅ Hadoop arrêté"
        ;;
    *)
        echo "❌ Choix invalide"
        exit 1
        ;;
esac

echo ""
echo "✅ Opération terminée"
echo "📋 Pour plus d'infos, consultez: music/storage/README.md"
