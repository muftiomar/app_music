import os
import json
import pandas as pd
from glob import glob


def main(storage_dir):
    df = load_events(storage_dir)
    print("Colonnes détectées :", df.columns)
    print(df.head())

def load_events(storage_dir):
    files = glob(os.path.join(storage_dir, "events_from_csv.jsonl"))
    all_events = []
    for file in files:
        with open(file, "r") as f:
            for line in f:
                try:
                    all_events.append(json.loads(line))
                except Exception:
                    continue
    return pd.DataFrame(all_events)

def top_artists(df, n=10):
    return df[df['action'] == 'play'].groupby('artist').size().sort_values(ascending=False).head(n)

def genres_by_hour(df):
    df['hour'] = pd.to_datetime(df['timestamp']).dt.hour
    return df[df['action'] == 'play'].groupby(['hour', 'genre']).size().unstack(fill_value=0)

def listens_by_country_platform(df):
    return df[df['action'] == 'play'].groupby(['country', 'platform']).size().unstack(fill_value=0)

def main(storage_dir):
    df = load_events(storage_dir)
    print("\nTop artistes les plus écoutés :")
    top_art = top_artists(df)
    print(top_art)
    top_art.to_csv(os.path.join(storage_dir, "top_artists_csv.csv"))

    print("\nGenres préférés par tranche horaire :")
    genres_hour = genres_by_hour(df)
    print(genres_hour)
    genres_hour.to_csv(os.path.join(storage_dir, "genres_by_hour_csv.csv"))

    print("\nNombre d'écoutes par pays / plateforme :")
    country_plat = listens_by_country_platform(df)
    print(country_plat)
    country_plat.to_csv(os.path.join(storage_dir, "listens_by_country_platform_csv.csv"))

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Analytics batch sur les événements musicaux")
    parser.add_argument("-s", "--storage", type=str, required=True, help="Dossier de stockage des événements nettoyés")
    args = parser.parse_args()
    main(args.storage)
