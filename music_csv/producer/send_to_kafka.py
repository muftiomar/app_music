# -*- coding: utf-8 -*-
from kafka import KafkaProducer
import json
import time

KAFKA_BROKER = "kafka:9092"      
TOPIC = "music-events"

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

with open("/tmp/events_from_csv.jsonl", "r") as f:
    for line in f:
        event = json.loads(line)
        producer.send(TOPIC, value=event)
        print("Envoyé :", event)  # Pour debug
        time.sleep(0.1)           # Simule du temps réel (10 events/sec)

producer.flush()
producer.close()
print("Tous les événements ont été envoyés !")
