#!/bin/bash
# Script pour démarrer le pipeline temps réel Music-Faker

echo "🎵 Démarrage du pipeline Music-Faker temps réel..."

# Vérifier que Docker est en cours
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker n'est pas démarré. Veuillez démarrer Docker Desktop."
    exit 1
fi

# Démarrer les services Docker
echo "🐳 Démarrage des services Docker (Kafka + HDFS)..."
docker-compose up -d

# Attendre que les services soient prêts
echo "⏳ Attente que les services soient prêts (30s)..."
sleep 30

# Vérifier la santé des services
echo "🔍 Vérification de la santé des services..."
if curl -s http://localhost:9871 > /dev/null; then
    echo "✅ HDFS NameNode OK"
else
    echo "⚠️ HDFS NameNode pas encore prêt"
fi

if nc -z localhost 9092 2>/dev/null; then
    echo "✅ Kafka OK"
else
    echo "⚠️ Kafka pas encore prêt"
fi

echo ""
echo "🚀 Services prêts ! Vous pouvez maintenant :"
echo "   1️⃣ Démarrer le producteur : python producer/music_producer.py -n 1000 -d 0.5"
echo "   2️⃣ Démarrer le consommateur : python consumer/kafka_hdfs_consumer.py -m batch -b 5"
echo "   3️⃣ Démarrer le dashboard : python app.py"
echo ""
echo "🎯 Ou utiliser le script automatique : python start_realtime_pipeline.py"
echo ""
echo "📊 Dashboard sera disponible sur : http://localhost:5001"
echo "🔧 HDFS WebUI disponible sur : http://localhost:9871"
