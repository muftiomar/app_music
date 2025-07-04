import pandas as pd
import json
import time
import requests
import random
import os
from kafka import KafkaProducer

CSV_FILE = "Last.fm_data.csv"
ALBUM_CACHE_FILE = "album_cache.csv"

PLATFORMS = ['Spotify', 'Deezer', 'Apple Music']
DEVICES = ['Mobile', 'Desktop', 'Tablet']
COUNTRIES = ['FR', 'US', 'UK', 'DE', 'ES']

def get_album_info(album_name, artist_name, cache):
    key = (album_name, artist_name)
    # Si dans le cache, on récupère sans requête
    if key in cache:
        return cache[key]
    # Sinon, requête à l’API Deezer
    try:
        url = f"https://api.deezer.com/search/album?q=album:'{album_name}' artist:'{artist_name}'"
        resp = requests.get(url, timeout=5)
        data = resp.json()
        if data.get('data'):
            album = data['data'][0]
            album_id = album.get('id')
            cover = album.get('cover_medium', '')
            # Appel complémentaire pour plus d’infos
            album_url = f"https://api.deezer.com/album/{album_id}"
            album_resp = requests.get(album_url, timeout=5)
            album_data = album_resp.json()
            genre = ""
            release_date = ""
            if album_data.get('genres') and album_data['genres'].get('data'):
                genre = album_data['genres']['data'][0]['name']
            release_date = album_data.get('release_date', "")
            result = (cover, genre, release_date)
            cache[key] = result
            return result
    except Exception as e:
        print(f"Erreur Deezer: {e}")
    cache[key] = ("", "", "")
    return ("", "", "")

def save_album_cache(cache, cache_file):
    rows = []
    for (album, artist), (cover, genre, release_date) in cache.items():
        rows.append({
            "album_name": album,
            "artist_name": artist,
            "cover": cover,
            "genre": genre,
            "release_date": release_date
        })
    pd.DataFrame(rows).to_csv(cache_file, index=False)

def load_album_cache(cache_file):
    cache = {}
    if os.path.exists(cache_file):
        df = pd.read_csv(cache_file)
        for _, row in df.iterrows():
            key = (row["album_name"], row["artist_name"])
            cache[key] = (row["cover"], row["genre"], row["release_date"])
    return cache

def generate_event(row, cache):
    timestamp = f"{row['Date'].strip()}T{str(row['Time']).strip()}:00"
    album_image, album_genre, album_release_date = get_album_info(row['Album'], row['Artist'], cache)
    return {
        "user_id": row['Username'],
        "timestamp": timestamp,
        "event_type": "listen",
        "track_name": row['Track'],
        "artist_name": row['Artist'],
        "album_name": row['Album'],
        "album_image": album_image,
        "album_genre": album_genre,
        "album_release_date": album_release_date,
        "device": random.choice(DEVICES),
        "platform": random.choice(PLATFORMS),
        "country": random.choice(COUNTRIES)
    }

if __name__ == "__main__":
    df = pd.read_csv(CSV_FILE)
    album_cache = load_album_cache(ALBUM_CACHE_FILE)

    producer = KafkaProducer(
        bootstrap_servers='localhost:9092',
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    try:
        for _, row in df.iterrows():
            event = generate_event(row, album_cache)
            producer.send('music-events', value=event)
            print("Sent:", event)
            time.sleep(0.2)  # Ajuste la vitesse si besoin
    finally:
        # Sauvegarde le cache pour les prochains runs
        save_album_cache(album_cache, ALBUM_CACHE_FILE)
