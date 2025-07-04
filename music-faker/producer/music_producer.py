import random
import json
import time
from faker import Faker
from kafka import KafkaProducer

fake = Faker()
KAFKA_TOPIC = "music_events"
KAFKA_SERVER = "127.0.0.1:9092"

# ... (tu peux réutiliser tes fonctions de génération d'événements ici) ...
GENRES = [
    "Pop", "Rock", "Jazz", "Electro", "Hip-Hop", "Classique", "Indie", "Soul", "Folk", "Reggae", "Blues", "Country", "Metal", "R&B", "Funk",
    "Trap", "House", "Techno", "Disco", "Gospel", "K-Pop", "Chill", "Ambient", "Trance", "Dubstep", "Salsa", "Latino", "Afrobeat", "Punk", "Grunge", "Opera"
]
PLATFORMS = [
    "Spotify", "Apple Music", "Deezer", "YouTube Music", "Amazon Music", "Tidal", "SoundCloud", "Napster", "Qobuz", "Pandora", "Anghami", "Boomplay", "Audiomack"
]
DEVICES = [
    "Mobile", "Desktop", "Tablet", "Smart Speaker", "TV", "Car", "Console", "Smartwatch", "Home Cinema", "VR Headset", "Web", "Radio"
]
ACTIONS = [
    "play", "like", "share", "skip", "add_to_playlist", "repeat", "download", "comment", "rate", "dislike", "favorite", "shuffle"
]
COUNTRIES = list({fake.country_code() for _ in range(100)})

def generate_artist():
    suffixes = [
        " Band", " Project", " Crew", " Collective", " Squad", " & Friends", " Experience", " Orchestra", " Sound", " Ensemble", " Unit", " Syndicate", " Group", " Family", " Movement", " Company", " Syndicate", " All Stars", " System", " Machine"
    ]
    if random.random() < 0.4:
        return fake.name()
    elif random.random() < 0.7:
        return fake.first_name() + random.choice(["", " " + fake.last_name()]) + random.choice(suffixes)
    else:
        return fake.user_name().capitalize() + random.choice(suffixes)

def generate_track():
    formats = [
        lambda: fake.catch_phrase(),
        lambda: fake.sentence(nb_words=random.randint(2, 6)),
        lambda: fake.word().capitalize() + " " + fake.word().capitalize(),
        lambda: fake.bs().capitalize(),
        lambda: fake.color_name() + " Nights",
        lambda: fake.first_name() + "'s Dream",
        lambda: fake.last_name() + " Flow",
        lambda: fake.city() + " Vibes",
        lambda: fake.company() + " Anthem",
        lambda: fake.job() + " Song"
    ]
    base = random.choice(formats)()
    suffixes = ["", " (Remix)", " - Live", " feat. " + fake.first_name(), " (Acoustic)", " (Radio Edit)", " (Extended)", " (Club Mix)", " (Demo)", " (Cover)"]
    return base.strip().replace(".", "") + random.choice(suffixes)

def generate_fake_event():
    event = {
        "user": fake.user_name(),
        "artist": generate_artist(),
        "track": generate_track(),
        "timestamp": fake.date_time_between(start_date="-30d", end_date="now").isoformat(),
        "genre": random.choice(GENRES),
        "duration": random.randint(60, 360),
        "platform": random.choice(PLATFORMS),
        "device": random.choice(DEVICES),
        "action": random.choice(ACTIONS),
        "country": random.choice(COUNTRIES)
    }
    return event

def produce_to_kafka(n=100, delay=0):
    try:
        producer = KafkaProducer(
            bootstrap_servers=KAFKA_SERVER,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            request_timeout_ms=10000,
            retries=3
        )
        print(f"Connecté à Kafka sur {KAFKA_SERVER}")
    except Exception as e:
        print(f"Erreur de connexion à Kafka: {e}")
        return
    
    for i in range(n):
        event = generate_fake_event()
        try:
            future = producer.send(KAFKA_TOPIC, value=event)
            result = future.get(timeout=10)
            print(f"Envoyé à Kafka: {event['artist']} - {event['track']}")
        except Exception as e:
            print(f"Erreur envoi événement {i}: {e}")
        if delay > 0:
            time.sleep(delay)
    producer.flush()
    print(f"{n} événements envoyés dans le topic '{KAFKA_TOPIC}'!")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Producer Kafka pour événements musicaux")
    parser.add_argument("-n", type=int, default=100, help="Nombre d'événements à générer")
    parser.add_argument("-d", "--delay", type=float, default=0, help="Délai entre chaque événement (secondes)")
    args = parser.parse_args()
    produce_to_kafka(n=args.n, delay=args.delay)
