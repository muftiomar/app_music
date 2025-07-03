#!/usr/bin/env python3
"""
Producteur de test pour générer des événements avec timestamp actuel
"""
import random
import json
import time
from datetime import datetime
from faker import Faker
from kafka import KafkaProducer

fake = Faker()
KAFKA_TOPIC = "music_events"
KAFKA_SERVER = "127.0.0.1:9092"

GENRES = ["Pop", "Rock", "Jazz", "Hip-Hop", "Electronic"]
PLATFORMS = ["Spotify", "Apple Music", "YouTube Music", "Deezer"]
DEVICES = ["Mobile", "Desktop", "Tablet", "Smart Speaker"]
ACTIONS = ["play", "like", "share", "skip", "favorite"]
COUNTRIES = ["US", "FR", "UK", "DE", "CA"]

def generate_artist():
    suffixes = [" Band", " Project", " Sound", " Orchestra", " Group"]
    return fake.first_name() + " " + fake.last_name() + random.choice([""] + suffixes)

def generate_track():
    formats = [
        lambda: fake.catch_phrase(),
        lambda: fake.color_name() + " Nights",
        lambda: fake.first_name() + "'s Dream",
        lambda: fake.city() + " Vibes"
    ]
    base = random.choice(formats)()
    suffixes = ["", " (Remix)", " - Live", " (Radio Edit)"]
    return base.strip() + random.choice(suffixes)

def generate_realtime_event():
    """Génère un événement avec timestamp actuel"""
    event = {
        "user": fake.user_name(),
        "artist": generate_artist(),
        "track": generate_track(),
        "timestamp": datetime.now().isoformat(),  # Timestamp actuel
        "genre": random.choice(GENRES),
        "duration": random.randint(120, 300),
        "platform": random.choice(PLATFORMS),
        "device": random.choice(DEVICES),
        "action": random.choice(ACTIONS),
        "country": random.choice(COUNTRIES)
    }
    return event

def produce_realtime_events(n=10, delay=1.0):
    """Produit des événements en temps réel"""
    try:
        producer = KafkaProducer(
            bootstrap_servers=KAFKA_SERVER,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            request_timeout_ms=10000,
            retries=3
        )
        print(f"🎵 Producteur temps réel connecté à Kafka sur {KAFKA_SERVER}")
    except Exception as e:
        print(f"❌ Erreur de connexion Kafka: {e}")
        return
    
    for i in range(n):
        event = generate_realtime_event()
        try:
            future = producer.send(KAFKA_TOPIC, value=event)
            result = future.get(timeout=10)
            print(f"✅ [{i+1}/{n}] {event['artist']} - {event['track']}")
        except Exception as e:
            print(f"❌ Erreur envoi événement {i}: {e}")
        
        if delay > 0:
            time.sleep(delay)
    
    producer.flush()
    print(f"🎉 {n} événements temps réel envoyés!")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Producteur d'événements musicaux temps réel")
    parser.add_argument("-n", type=int, default=10, help="Nombre d'événements")
    parser.add_argument("-d", "--delay", type=float, default=1.0, help="Délai entre événements")
    
    args = parser.parse_args()
    produce_realtime_events(args.n, args.delay)
