import random
from faker import Faker
from datetime import datetime, timedelta
import json
import time

fake = Faker()


# Génération dynamique et réaliste
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
# Génère 100 codes pays uniques
COUNTRIES = list({fake.country_code() for _ in range(100)})

def generate_artist():
    # Génère un nom d'artiste réaliste et varié
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
    # Génère un titre de musique réaliste et varié
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
        "duration": random.randint(60, 360),  # en secondes
        "platform": random.choice(PLATFORMS),
        "device": random.choice(DEVICES),
        "action": random.choice(ACTIONS),
        "country": random.choice(COUNTRIES)
    }
    return event


def produce_events(n=100, output_file=None, delay=0):
    """
    Génère n événements musicaux fake.
    Si output_file est précisé, écrit les événements en JSON lines dans ce fichier.
    Sinon, les affiche dans la console.
    Si delay > 0, attend 'delay' secondes entre chaque événement (pour simuler du temps réel).
    """
    events = []
    for i in range(n):
        event = generate_fake_event()
        if output_file:
            with open(output_file, "a") as f:
                f.write(json.dumps(event) + "\n")
        else:
            print(json.dumps(event, ensure_ascii=False))
        if delay > 0:
            time.sleep(delay)
        events.append(event)
    return events


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Générateur d'événements musicaux fake")
    parser.add_argument("-n", type=int, default=100, help="Nombre d'événements à générer")
    parser.add_argument("-o", "--output", type=str, help="Fichier de sortie (JSON lines)")
    parser.add_argument("-d", "--delay", type=float, default=0, help="Délai entre chaque événement (secondes)")
    args = parser.parse_args()
    produce_events(n=args.n, output_file=args.output, delay=args.delay)
