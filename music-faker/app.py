#!/usr/bin/env python3
"""
Frontend Web pour visualiser les données musicales en temps réel
"""
from flask import Flask, render_template, jsonify, request
import subprocess
import json
import pandas as pd
from datetime import datetime, timedelta
import os
import threading
import time
import requests

app = Flask(__name__)

class MusicDataManager:
    def __init__(self):
        self.last_update = None
        self.cached_data = None
        self.cache_duration = 3  # Cache pendant 3 secondes seulement pour temps réel
        self._loading = False  # Flag pour éviter les requêtes simultanées
        # Données de fallback quand HDFS est lent
        self.fallback_data = {
            'total_events': 100,
            'unique_users': 25,
            'unique_artists': 40,
            'unique_tracks': 85,
            'genres': ['Pop', 'Rock', 'Jazz', 'Electronic', 'Hip-Hop', 'Classical', 'Blues', 'Reggae'],
            'platforms': ['Spotify', 'Apple Music', 'YouTube Music', 'Deezer', 'Amazon Music'],
            'actions': ['play', 'skip', 'like', 'pause', 'share'],
            'countries': ['USA', 'France', 'UK', 'Germany', 'Canada'],
            'artists': ['Taylor Swift', 'Ed Sheeran', 'Billie Eilish', 'The Weeknd', 'Adele'],
            'tracks': ['Anti-Hero', 'Shape of You', 'Bad Guy', 'Blinding Lights', 'Easy On Me']
        }
    
    def get_hdfs_files(self):
        """Découverte robuste des fichiers HDFS : API REST WebHDFS puis fallback Docker CLI si échec"""
        files = []
        base_url = "http://localhost:9871/webhdfs/v1"
        try:
            # --- Découverte via API REST WebHDFS ---
            response = requests.get(f"{base_url}/music_events/year=2025?op=LISTSTATUS", timeout=5)
            if response.status_code != 200:
                raise Exception("API REST HDFS (mois) KO")
            months_data = response.json()["FileStatuses"]["FileStatus"]
            months = [item["pathSuffix"] for item in months_data if item["type"] == "DIRECTORY" and "month=" in item["pathSuffix"]]
            if not months:
                raise Exception("Aucun mois trouvé dans HDFS")
            last_month = months[-1]
            response = requests.get(f"{base_url}/music_events/year=2025/{last_month}?op=LISTSTATUS", timeout=5)
            if response.status_code != 200:
                raise Exception("API REST HDFS (jours) KO")
            days_data = response.json()["FileStatuses"]["FileStatus"]
            days = [item["pathSuffix"] for item in days_data if item["type"] == "DIRECTORY" and "day=" in item["pathSuffix"]]
            if not days:
                raise Exception("Aucun jour trouvé dans HDFS")
            for day in reversed(days):
                response = requests.get(f"{base_url}/music_events/year=2025/{last_month}/{day}?op=LISTSTATUS", timeout=5)
                if response.status_code == 200:
                    files_data = response.json()["FileStatuses"]["FileStatus"]
                    for file_item in files_data:
                        if file_item["type"] == "FILE" and ".jsonl" in file_item["pathSuffix"] and "test.json" not in file_item["pathSuffix"]:
                            file_path = f"/music_events/year=2025/{last_month}/{day}/{file_item['pathSuffix']}"
                            files.append(file_path)
            print(f"📁 Fichiers HDFS découverts (API REST): {files}")
            return files
        except Exception as e:
            print(f"⚠️ Découverte API REST HDFS impossible : {e}")
            # --- Fallback découverte via Docker CLI ---
            try:
                import shlex
                import select
                print("🔄 Fallback découverte fichiers HDFS via Docker CLI (Popen)...")
                # --- Lister les mois ---
                cmd_months = "docker exec music-faker-namenode-1 hdfs dfs -ls /music_events/year=2025"
                months = []
                with subprocess.Popen(shlex.split(cmd_months), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) as proc:
                    start = time.time()
                    while True:
                        line = proc.stdout.readline()
                        if not line:
                            break
                        if 'month=' in line:
                            parts = line.split()
                            if len(parts) >= 8:
                                months.append(parts[-1].split('/')[-1])
                        if time.time() - start > 30:
                            proc.kill()
                            raise TimeoutError("Timeout mois Docker CLI")
                if not months:
                    print("❌ Aucun mois trouvé via Docker CLI (Popen)")
                    return []
                last_month = months[-1]
                # --- Lister les jours ---
                cmd_days = f"docker exec music-faker-namenode-1 hdfs dfs -ls /music_events/year=2025/{last_month}"
                days = []
                with subprocess.Popen(shlex.split(cmd_days), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) as proc:
                    start = time.time()
                    while True:
                        line = proc.stdout.readline()
                        if not line:
                            break
                        if 'day=' in line:
                            parts = line.split()
                            if len(parts) >= 8:
                                days.append(parts[-1].split('/')[-1])
                        if time.time() - start > 30:
                            proc.kill()
                            raise TimeoutError("Timeout jours Docker CLI")
                if not days:
                    print("❌ Aucun jour trouvé via Docker CLI (Popen)")
                    return []
                # --- Lister les fichiers ---
                for day in reversed(days):
                    cmd_files = f"docker exec music-faker-namenode-1 hdfs dfs -ls /music_events/year=2025/{last_month}/{day}"
                    with subprocess.Popen(shlex.split(cmd_files), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) as proc:
                        start = time.time()
                        while True:
                            line = proc.stdout.readline()
                            if not line:
                                break
                            if '.jsonl' in line and 'test.json' not in line:
                                parts = line.split()
                                if len(parts) >= 8:
                                    file_path = parts[-1]
                                    files.append(file_path)
                            if time.time() - start > 30:
                                proc.kill()
                                raise TimeoutError(f"Timeout fichiers Docker CLI pour {day}")
                print(f"📁 Fichiers HDFS découverts (Docker CLI): {files}")
                return files
            except Exception as e2:
                print(f"❌ Exception fallback Docker CLI (Popen): {e2}")
                return []
    
    def read_hdfs_file(self, hdfs_file_path, max_lines=100):
        """Lecture optimisée d'un fichier HDFS via Docker CLI seulement."""
        import time
        import shlex
        try:
            start = time.time()
            print(f"📖 Lecture HDFS: {hdfs_file_path}")
            
            cmd = f"docker exec music-faker-namenode-1 hdfs dfs -cat {shlex.quote(hdfs_file_path)}"
            proc = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            events = []
            lines_read = 0
            timeout = 10  # Timeout réduit à 10 secondes
            
            while lines_read < max_lines:
                if time.time() - start > timeout:
                    print(f"⏰ Timeout lecture {hdfs_file_path}")
                    proc.kill()
                    break
                    
                line = proc.stdout.readline()
                if not line:
                    break
                    
                if line.strip():
                    try:
                        event = json.loads(line.strip())
                        events.append(event)
                    except json.JSONDecodeError:
                        pass  # Ignorer silencieusement les erreurs JSON
                        
                lines_read += 1
            
            # Nettoyer le processus
            if proc.poll() is None:
                proc.terminate()
                try:
                    proc.wait(timeout=1)
                except subprocess.TimeoutExpired:
                    proc.kill()
            
            elapsed = time.time() - start
            print(f"✅ Lecture terminée en {elapsed:.2f}s: {len(events)} événements")
            return events
            
        except Exception as e:
            print(f"❌ Erreur lecture {hdfs_file_path}: {e}")
            return []
    
    def load_latest_data(self, limit_files=15):
        """Charge les données les plus récentes depuis HDFS (lecture de plusieurs fichiers pour temps réel)"""
        try:
            files = self.get_hdfs_files()
            
            if not files:
                return []
            
            # Prendre les 15 fichiers les plus récents (plus pour temps réel)
            files = sorted(files, reverse=True)[:limit_files]
            
            all_events = []
            
            for file_path in files:
                events = self.read_hdfs_file(file_path, max_lines=100)  # Plus de lignes par fichier
                if events:  # Si la lecture réussit
                    all_events.extend(events)
                    print(f"✅ Fichier lu: {file_path} ({len(events)} événements)")
                    # Ne pas break - continuer à lire les autres fichiers pour avoir plus de données
                else:
                    print(f"⚠️ Échec: {file_path}")
                
                # Arrêter si on a assez d'événements
                if len(all_events) >= 500:  # Plus d'événements pour un dashboard riche
                    print(f"🎯 Objectif atteint: {len(all_events)} événements collectés")
                    break
            
            return all_events
        except Exception as e:
            print(f"❌ Erreur load_latest_data: {e}")
            return []
    
    def get_data(self, force_refresh=False):
        """Récupère les données depuis HDFS, avec protection contre les requêtes simultanées"""
        now = datetime.now()
        
        # Retourner le cache si valide
        if (not force_refresh and 
            self.cached_data is not None and 
            self.last_update is not None and 
            (now - self.last_update).seconds < self.cache_duration):
            return self.cached_data
        
        # Éviter les requêtes simultanées
        if self._loading:
            print("⏳ Chargement en cours, retour du cache existant...")
            return self.cached_data if self.cached_data is not None else pd.DataFrame([])
        
        self._loading = True
        print("🔍 Tentative de chargement depuis HDFS...")
        try:
            events = self.load_latest_data()
            if events:
                self.cached_data = pd.DataFrame(events)
                self.last_update = now
                print(f"✅ Données HDFS chargées: {len(events)} événements")
                return self.cached_data
            else:
                print("❌ Aucune donnée HDFS disponible (aucun event lu)")
                self.cached_data = pd.DataFrame([])
                self.last_update = now
                return self.cached_data
        except Exception as e:
            print(f"❌ Erreur lors du chargement HDFS : {e}")
            self.cached_data = pd.DataFrame([])
            self.last_update = now
            return self.cached_data
        finally:
            self._loading = False
    
    # Fallback désactivé : cette méthode n'est plus utilisée

# Instance globale
data_manager = MusicDataManager()

@app.route('/')
def dashboard():
    """Page principale du dashboard"""
    return render_template('dashboard.html')

@app.route('/api/stats')
def api_stats():
    """API pour les statistiques générales"""
    df = data_manager.get_data()
    
    if df.empty:
        return jsonify({
            'total_events': 0,
            'unique_users': 0,
            'unique_artists': 0,
            'unique_tracks': 0,
            'last_update': 'Aucune donnée'
        })
    
    stats = {
        'total_events': len(df),
        'unique_users': df['user'].nunique(),
        'unique_artists': df['artist'].nunique(),
        'unique_tracks': df['track'].nunique(),
        'last_update': datetime.now().strftime('%H:%M:%S')
    }
    
    return jsonify(stats)

@app.route('/api/top_genres')
def api_top_genres():
    """API pour les top genres"""
    df = data_manager.get_data()
    
    if df.empty:
        return jsonify([])
    
    top_genres = df['genre'].value_counts().head(10)
    result = [{'genre': genre, 'count': int(count)} for genre, count in top_genres.items()]
    
    return jsonify(result)

@app.route('/api/top_platforms')
def api_top_platforms():
    """API pour les top plateformes"""
    df = data_manager.get_data()
    
    if df.empty:
        return jsonify([])
    
    top_platforms = df['platform'].value_counts().head(8)
    result = [{'platform': platform, 'count': int(count)} for platform, count in top_platforms.items()]
    
    return jsonify(result)

@app.route('/api/top_actions')
def api_top_actions():
    """API pour les top actions"""
    df = data_manager.get_data()
    
    if df.empty:
        return jsonify([])
    
    top_actions = df['action'].value_counts().head(8)
    result = [{'action': action, 'count': int(count)} for action, count in top_actions.items()]
    
    return jsonify(result)

@app.route('/api/duration_stats')
def api_duration_stats():
    """API pour les statistiques de durée"""
    df = data_manager.get_data()
    
    if df.empty:
        return jsonify({})
    
    stats = {
        'mean': float(df['duration'].mean()),
        'median': float(df['duration'].median()),
        'min': int(df['duration'].min()),
        'max': int(df['duration'].max()),
        'histogram': []
    }
    
    # Histogramme des durées
    hist, bins = pd.cut(df['duration'], bins=10, retbins=True)
    hist_counts = hist.value_counts().sort_index()
    
    for interval, count in hist_counts.items():
        stats['histogram'].append({
            'range': f"{int(interval.left)}-{int(interval.right)}s",
            'count': int(count)
        })
    
    return jsonify(stats)

@app.route('/api/recent_activity')
def api_recent_activity():
    """API pour l'activité récente"""
    df = data_manager.get_data()
    
    if df.empty:
        return jsonify([])
    
    # Trier par timestamp et prendre les 20 plus récents
    df_sorted = df.sort_values('timestamp', ascending=False).head(20)
    
    recent = []
    for _, event in df_sorted.iterrows():
        recent.append({
            'artist': event['artist'],
            'track': event['track'],
            'user': event['user'],
            'action': event['action'],
            'platform': event['platform'],
            'timestamp': event['timestamp']
        })
    
    return jsonify(recent)

@app.route('/api/countries')
def api_countries():
    """API pour la répartition par pays"""
    df = data_manager.get_data()
    
    if df.empty:
        return jsonify([])
    
    top_countries = df['country'].value_counts().head(15)
    result = [{'country': country, 'count': int(count)} for country, count in top_countries.items()]
    
    return jsonify(result)

@app.route('/api/refresh')
def api_refresh():
    """API pour forcer le rafraîchissement des données"""
    df = data_manager.get_data(force_refresh=True)
    return jsonify({'status': 'refreshed', 'events': len(df)})

@app.route('/api/stream')
def api_stream():
    """API pour streaming temps réel - retourne les derniers événements"""
    df = data_manager.get_data()
    
    if df.empty:
        return jsonify({'events': [], 'count': 0})
    
    # Retourner les 50 événements les plus récents
    df_recent = df.sort_values('timestamp', ascending=False).head(50)
    
    events = []
    for _, event in df_recent.iterrows():
        events.append({
            'artist': event['artist'],
            'track': event['track'],
            'user': event['user'],
            'action': event['action'],
            'platform': event['platform'],
            'genre': event['genre'],
            'country': event['country'],
            'timestamp': event['timestamp'],
            'duration': event['duration']
        })
    
    return jsonify({
        'events': events,
        'count': len(events),
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/live_stats')
def api_live_stats():
    """API pour statistiques temps réel avec plus de détails"""
    df = data_manager.get_data()
    
    if df.empty:
        return jsonify({
            'total_events': 0,
            'events_per_minute': 0,
            'top_artist': 'Aucun',
            'top_platform': 'Aucun',
            'active_countries': 0,
            'last_update': 'Jamais'
        })
    
    # Calculer les événements des 5 dernières minutes
    now = datetime.now()
    df['ts'] = pd.to_datetime(df['timestamp'])
    recent_events = df[df['ts'] > (now - pd.Timedelta(minutes=5))]
    
    stats = {
        'total_events': len(df),
        'events_per_minute': len(recent_events),
        'top_artist': df['artist'].value_counts().index[0] if not df.empty else 'Aucun',
        'top_platform': df['platform'].value_counts().index[0] if not df.empty else 'Aucun',
        'active_countries': df['country'].nunique(),
        'last_update': datetime.now().strftime('%H:%M:%S')
    }
    
    return jsonify(stats)

@app.route('/api/realtime_metrics')
def api_realtime_metrics():
    """API pour les métriques temps réel (utilisé par le JS pour l'auto-refresh)"""
    df = data_manager.get_data()
    
    if df.empty:
        return jsonify({
            'status': 'no_data',
            'message': 'Aucune donnée disponible',
            'timestamp': datetime.now().isoformat(),
            'cache_age': 0
        })
    
    # Calculer l'âge du cache
    cache_age = 0
    if data_manager.last_update:
        cache_age = (datetime.now() - data_manager.last_update).total_seconds()
    
    return jsonify({
        'status': 'ok',
        'total_events': len(df),
        'cache_age_seconds': cache_age,
        'timestamp': datetime.now().isoformat(),
        'data_freshness': 'fresh' if cache_age < 10 else 'stale'
    })

@app.route('/health')
def health_check():
    """Endpoint de santé pour vérifier le statut du service"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })

if __name__ == '__main__':
    print("🚀 Démarrage du dashboard Music-Faker...")
    print("📊 Dashboard disponible sur: http://localhost:5001")
    print("🔥 Mode temps réel activé avec auto-refresh")
    app.run(host='0.0.0.0', port=5001, debug=True, threaded=True)
