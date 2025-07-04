import pandas as pd
import json
import random
from datetime import datetime, timedelta

csv_path = "/Users/admin/Documents/app_music/app_music/music_csv/producer/spotify_data.csv"     # <-- adapte avec ton vrai chemin CSV (ex: ../musics.csv)
jsonl_path = "/Users/admin/Documents/app_music/app_music/music_csv/producer/events_from_csv.jsonl"

PLATFORMS = [
    "Spotify", "Apple Music", "Deezer", "YouTube Music", "Amazon Music", "Tidal",
    "SoundCloud", "Napster", "Qobuz", "Pandora", "Anghami", "Boomplay", "Audiomack"
]
DEVICES = [
    "Mobile", "Desktop", "Tablet", "Smart Speaker", "TV", "Car", "Console",
    "Smartwatch", "Home Cinema", "VR Headset", "Web", "Radio"
]
ACTIONS = [
    "play", "like", "share", "skip", "add_to_playlist", "repeat", "download", "comment",
    "rate", "dislike", "favorite", "shuffle"
]
COUNTRIES = ['FR', 'US', 'UK', 'DE', 'IT', 'ES', 'JP', 'CA', 'RU', 'BR', 'MA']

df = pd.read_csv(csv_path)

# Générer des timestamps récents
start_time = datetime.now() - timedelta(days=30)
df['timestamp'] = [ (start_time + timedelta(seconds=random.randint(0, 2592000))).isoformat() for _ in range(len(df)) ]

# Ajoute/simule les colonnes manquantes
df['user'] = [f'user_{i%50}' for i in range(len(df))]
df['platform'] = [random.choice(PLATFORMS) for _ in range(len(df))]
df['device'] = [random.choice(DEVICES) for _ in range(len(df))]
df['action'] = [random.choice(['play', 'like', 'play', 'play']) for _ in range(len(df))]
df['country'] = [random.choice(COUNTRIES) for _ in range(len(df))]
df['duration'] = (df['duration_ms'] // 1000).astype(int)

with open(jsonl_path, "w") as f:
    for _, row in df.iterrows():
        event = {
            "user": row["user"],
            "artist": row["artist_name"],
            "track": row["track_name"],
            "timestamp": row["timestamp"],
            "genre": row["genre"],
            "duration": row["duration"],
            "platform": row["platform"],
            "device": row["device"],
            "action": row["action"],
            "country": row["country"]
        }
        f.write(json.dumps(event, ensure_ascii=False) + "\n")

print(f"Fichier {jsonl_path} généré !")
