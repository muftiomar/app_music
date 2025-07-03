import json
import os
from collections import defaultdict

def clean_event(event):
    """
    Nettoyage simple :
    - Vérifie la présence des champs obligatoires
    - Peut enrichir ou corriger certains champs si besoin
    """
    required_fields = ["user", "artist", "track", "timestamp", "genre", "duration", "platform", "device", "action", "country"]
    for field in required_fields:
        if field not in event:
            return None  # Événement incomplet
    return event


def consume_events(input_file, output_dir):
    """
    Lit les événements depuis un fichier JSON lines,
    effectue un nettoyage simple,
    et écrit les événements nettoyés dans un dossier de stockage (un fichier par jour).
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    seen = set()  # Pour suppression des doublons (user+track+timestamp)
    stats = defaultdict(int)
    with open(input_file, "r") as f:
        for line in f:
            try:
                event = json.loads(line)
            except Exception:
                continue
            event = clean_event(event)
            if not event:
                continue
            key = (event["user"], event["track"], event["timestamp"])
            if key in seen:
                continue  # Doublon
            seen.add(key)
            # Partitionnement par jour
            day = event["timestamp"].split("T")[0]
            out_path = os.path.join(output_dir, f"music_events_{day}.jsonl")
            with open(out_path, "a") as out_f:
                out_f.write(json.dumps(event, ensure_ascii=False) + "\n")
            stats[day] += 1
    print(f"Ingestion terminée. Statistiques :")
    for day, count in stats.items():
        print(f"  {day} : {count} événements ingérés.")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Consumer d'événements musicaux fake (nettoyage + stockage)")
    parser.add_argument("-i", "--input", type=str, required=True, help="Fichier d'entrée (JSON lines)")
    parser.add_argument("-o", "--output", type=str, required=True, help="Dossier de sortie (simule HDFS)")
    args = parser.parse_args()
    consume_events(args.input, args.output)
