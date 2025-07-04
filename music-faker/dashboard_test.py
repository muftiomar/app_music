#!/usr/bin/env python3
"""
Dashboard simple avec données de test
"""
from flask import Flask, render_template, jsonify
import random
from datetime import datetime

app = Flask(__name__)

# Données de test
test_data = {
    'total_events': 100,
    'unique_users': 25,
    'unique_artists': 40,
    'unique_tracks': 85,
    'genres': [
        {'genre': 'Pop', 'count': 25},
        {'genre': 'Rock', 'count': 20},
        {'genre': 'Jazz', 'count': 15},
        {'genre': 'Electronic', 'count': 12},
        {'genre': 'Hip-Hop', 'count': 10},
        {'genre': 'Classical', 'count': 8},
        {'genre': 'Blues', 'count': 6},
        {'genre': 'Reggae', 'count': 4}
    ],
    'platforms': [
        {'platform': 'Spotify', 'count': 35},
        {'platform': 'Apple Music', 'count': 25},
        {'platform': 'YouTube Music', 'count': 20},
        {'platform': 'Deezer', 'count': 12},
        {'platform': 'Amazon Music', 'count': 8}
    ],
    'actions': [
        {'action': 'play', 'count': 45},
        {'action': 'skip', 'count': 25},
        {'action': 'like', 'count': 15},
        {'action': 'pause', 'count': 10},
        {'action': 'share', 'count': 5}
    ]
}

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/stats')
def api_stats():
    return jsonify({
        'total_events': test_data['total_events'],
        'unique_users': test_data['unique_users'],
        'unique_artists': test_data['unique_artists'],
        'unique_tracks': test_data['unique_tracks'],
        'last_update': datetime.now().strftime('%H:%M:%S')
    })

@app.route('/api/top_genres')
def api_top_genres():
    return jsonify(test_data['genres'])

@app.route('/api/top_platforms')
def api_top_platforms():
    return jsonify(test_data['platforms'])

@app.route('/api/top_actions')
def api_top_actions():
    return jsonify(test_data['actions'])

@app.route('/api/duration_stats')
def api_duration_stats():
    return jsonify({
        'mean': 215.5,
        'median': 210.0,
        'min': 120,
        'max': 350,
        'histogram': [
            {'range': '120-150s', 'count': 8},
            {'range': '150-180s', 'count': 12},
            {'range': '180-210s', 'count': 25},
            {'range': '210-240s', 'count': 30},
            {'range': '240-270s', 'count': 15},
            {'range': '270-300s', 'count': 7},
            {'range': '300-330s', 'count': 3}
        ]
    })

@app.route('/api/recent_activity')
def api_recent_activity():
    artists = ['Taylor Swift', 'Ed Sheeran', 'Billie Eilish', 'The Weeknd', 'Adele']
    tracks = ['Anti-Hero', 'Shape of You', 'Bad Guy', 'Blinding Lights', 'Easy On Me']
    users = ['user1', 'user2', 'user3', 'user4', 'user5']
    actions = ['play', 'skip', 'like', 'pause']
    platforms = ['Spotify', 'Apple Music', 'YouTube Music']
    
    recent = []
    for i in range(20):
        recent.append({
            'artist': random.choice(artists),
            'track': random.choice(tracks),
            'user': random.choice(users),
            'action': random.choice(actions),
            'platform': random.choice(platforms),
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
    
    return jsonify(recent)

@app.route('/api/countries')
def api_countries():
    return jsonify([
        {'country': 'USA', 'count': 30},
        {'country': 'France', 'count': 20},
        {'country': 'UK', 'count': 15},
        {'country': 'Germany', 'count': 12},
        {'country': 'Canada', 'count': 10},
        {'country': 'Australia', 'count': 8},
        {'country': 'Japan', 'count': 5}
    ])

@app.route('/api/refresh')
def api_refresh():
    return jsonify({'status': 'refreshed', 'events': test_data['total_events']})

if __name__ == '__main__':
    print("🎵 Démarrage du dashboard de test...")
    print("📊 Dashboard disponible sur: http://localhost:5001")
    app.run(host='0.0.0.0', port=5001, debug=False)
