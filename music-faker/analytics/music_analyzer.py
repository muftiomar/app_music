#!/usr/bin/env python3
"""
Script d'analyse des données musicales stockées dans HDFS
"""
import subprocess
import json
import pandas as pd
from collections import defaultdict, Counter
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

def list_hdfs_files(hdfs_path="/music_events"):
    """Liste tous les fichiers JSONL dans HDFS"""
    try:
        cmd = f"docker exec namenode hdfs dfs -ls -R {hdfs_path}"
        result = subprocess.run(cmd.split(), capture_output=True, text=True)
        if result.returncode == 0:
            files = []
            for line in result.stdout.split('\n'):
                if line.strip() and line.startswith('-') and '.jsonl' in line and 'test.json' not in line:
                    # Extraire le chemin du fichier (dernière colonne)
                    parts = line.split()
                    if len(parts) >= 8:
                        file_path = parts[-1]
                        files.append(file_path)
            return files
        else:
            print(f"Erreur lors de la liste des fichiers: {result.stderr}")
            return []
    except Exception as e:
        print(f"Erreur: {e}")
        return []

def read_hdfs_file(hdfs_file_path):
    """Lit un fichier JSONL depuis HDFS et retourne les événements"""
    try:
        cmd = f"docker exec namenode hdfs dfs -cat {hdfs_file_path}"
        result = subprocess.run(cmd.split(), capture_output=True, text=True)
        if result.returncode == 0:
            events = []
            for line in result.stdout.strip().split('\n'):
                if line.strip():
                    try:
                        event = json.loads(line)
                        events.append(event)
                    except json.JSONDecodeError:
                        continue
            return events
        else:
            print(f"Erreur lecture {hdfs_file_path}: {result.stderr}")
            return []
    except Exception as e:
        print(f"Erreur: {e}")
        return []

def load_all_events():
    """Charge tous les événements depuis HDFS"""
    files = list_hdfs_files()
    print(f"📁 Trouvé {len(files)} fichiers dans HDFS:")
    for f in files:
        print(f"  - {f}")
    
    all_events = []
    for file_path in files:
        print(f"📖 Lecture de {file_path}...")
        events = read_hdfs_file(file_path)
        all_events.extend(events)
        print(f"   ✅ {len(events)} événements chargés")
    
    print(f"\n📊 Total: {len(all_events)} événements musicaux")
    return all_events

def analyze_events(events):
    """Analyse les événements musicaux"""
    if not events:
        print("Aucun événement à analyser")
        return
    
    print("\n" + "="*60)
    print("📈 ANALYSE DES DONNÉES MUSICALES")
    print("="*60)
    
    # Conversion en DataFrame pour faciliter l'analyse
    df = pd.DataFrame(events)
    
    # Statistiques générales
    print(f"\n🎵 STATISTIQUES GÉNÉRALES:")
    print(f"   • Nombre total d'événements: {len(df)}")
    print(f"   • Nombre d'utilisateurs uniques: {df['user'].nunique()}")
    print(f"   • Nombre d'artistes uniques: {df['artist'].nunique()}")
    print(f"   • Nombre de pistes uniques: {df['track'].nunique()}")
    print(f"   • Période: {df['timestamp'].min()} à {df['timestamp'].max()}")
    
    # Top genres
    print(f"\n🎼 TOP 10 GENRES:")
    top_genres = df['genre'].value_counts().head(10)
    for genre, count in top_genres.items():
        print(f"   • {genre}: {count} écoutes")
    
    # Top plateformes
    print(f"\n📱 TOP 5 PLATEFORMES:")
    top_platforms = df['platform'].value_counts().head(5)
    for platform, count in top_platforms.items():
        print(f"   • {platform}: {count} écoutes")
    
    # Top actions
    print(f"\n🎬 TOP 5 ACTIONS:")
    top_actions = df['action'].value_counts().head(5)
    for action, count in top_actions.items():
        print(f"   • {action}: {count} fois")
    
    # Top devices
    print(f"\n📟 TOP 5 APPAREILS:")
    top_devices = df['device'].value_counts().head(5)
    for device, count in top_devices.items():
        print(f"   • {device}: {count} utilisations")
    
    # Durée moyenne
    print(f"\n⏱️  DURÉES:")
    print(f"   • Durée moyenne: {df['duration'].mean():.1f} secondes")
    print(f"   • Durée médiane: {df['duration'].median():.1f} secondes")
    print(f"   • Durée min/max: {df['duration'].min()}s / {df['duration'].max()}s")
    
    # Top pays
    print(f"\n🌍 TOP 10 PAYS:")
    top_countries = df['country'].value_counts().head(10)
    for country, count in top_countries.items():
        print(f"   • {country}: {count} écoutes")
    
    return df

def create_visualizations(df):
    """Crée des visualisations des données"""
    if df.empty:
        return
    
    print(f"\n📊 Création des graphiques...")
    
    # Configuration du style
    plt.style.use('seaborn-v0_8')
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('🎵 Analyse des Données Musicales - HDFS', fontsize=16, fontweight='bold')
    
    # Graphique 1: Top genres
    top_genres = df['genre'].value_counts().head(8)
    axes[0,0].bar(range(len(top_genres)), top_genres.values, color='skyblue')
    axes[0,0].set_title('🎼 Top 8 Genres Musicaux')
    axes[0,0].set_xticks(range(len(top_genres)))
    axes[0,0].set_xticklabels(top_genres.index, rotation=45, ha='right')
    axes[0,0].set_ylabel('Nombre d\'écoutes')
    
    # Graphique 2: Plateformes
    top_platforms = df['platform'].value_counts().head(6)
    axes[0,1].pie(top_platforms.values, labels=top_platforms.index, autopct='%1.1f%%', startangle=90)
    axes[0,1].set_title('📱 Répartition par Plateforme')
    
    # Graphique 3: Actions
    top_actions = df['action'].value_counts().head(6)
    axes[1,0].barh(range(len(top_actions)), top_actions.values, color='lightcoral')
    axes[1,0].set_title('🎬 Actions les Plus Fréquentes')
    axes[1,0].set_yticks(range(len(top_actions)))
    axes[1,0].set_yticklabels(top_actions.index)
    axes[1,0].set_xlabel('Nombre d\'occurrences')
    
    # Graphique 4: Durées
    axes[1,1].hist(df['duration'], bins=20, color='lightgreen', alpha=0.7, edgecolor='black')
    axes[1,1].set_title('⏱️ Distribution des Durées')
    axes[1,1].set_xlabel('Durée (secondes)')
    axes[1,1].set_ylabel('Fréquence')
    axes[1,1].axvline(df['duration'].mean(), color='red', linestyle='--', 
                     label=f'Moyenne: {df["duration"].mean():.1f}s')
    axes[1,1].legend()
    
    plt.tight_layout()
    
    # Sauvegarder le graphique
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'music_analytics_{timestamp}.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"   ✅ Graphiques sauvegardés: {filename}")
    
    # Afficher
    plt.show()

def export_summary_to_csv(df):
    """Exporte un résumé en CSV"""
    if df.empty:
        return
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Résumé par genre
    genre_summary = df.groupby('genre').agg({
        'duration': ['count', 'mean', 'sum'],
        'user': 'nunique',
        'artist': 'nunique'
    }).round(2)
    genre_summary.columns = ['Total_Ecoutes', 'Duree_Moyenne', 'Duree_Totale', 'Utilisateurs_Uniques', 'Artistes_Uniques']
    genre_summary.to_csv(f'music_stats_{timestamp}_genres.csv')
    
    # Résumé par plateforme
    platform_summary = df.groupby('platform').agg({
        'duration': ['count', 'mean'],
        'user': 'nunique'
    }).round(2)
    platform_summary.columns = ['Total_Ecoutes', 'Duree_Moyenne', 'Utilisateurs_Uniques']
    platform_summary.to_csv(f'music_stats_{timestamp}_platforms.csv')
    
    # Résumé par pays
    country_summary = df.groupby('country').agg({
        'duration': ['count', 'sum'],
        'user': 'nunique'
    }).round(2)
    country_summary.columns = ['Total_Ecoutes', 'Duree_Totale', 'Utilisateurs_Uniques']
    country_summary.to_csv(f'music_stats_{timestamp}_countries.csv')
    
    # Résumé par action
    action_summary = df.groupby('action').size().reset_index(name='Count')
    action_summary.to_csv(f'music_stats_{timestamp}_events.csv', index=False)
    
    print(f"\n📁 Fichiers CSV exportés:")
    print(f"   • music_stats_{timestamp}_genres.csv")
    print(f"   • music_stats_{timestamp}_platforms.csv") 
    print(f"   • music_stats_{timestamp}_countries.csv")
    print(f"   • music_stats_{timestamp}_events.csv")

def main():
    print("🎵 ANALYSEUR DE DONNÉES MUSICALES HDFS")
    print("="*50)
    
    # Charger les données
    events = load_all_events()
    
    if not events:
        print("❌ Aucune donnée trouvée dans HDFS")
        return
    
    # Analyser
    df = analyze_events(events)
    
    # Exporter les résumés
    export_summary_to_csv(df)
    
    # Créer les visualisations
    try:
        create_visualizations(df)
    except Exception as e:
        print(f"⚠️  Erreur lors de la création des graphiques: {e}")
    
    print(f"\n✨ Analyse terminée!")

if __name__ == "__main__":
    main()
