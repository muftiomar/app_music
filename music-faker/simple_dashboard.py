#!/usr/bin/env python3
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Dashboard Test</title>
    </head>
    <body>
        <h1>🎵 Music Dashboard - Test Simple</h1>
        <div id="stats"></div>
        <script>
            fetch('/api/stats')
                .then(r => r.json())
                .then(data => {
                    document.getElementById('stats').innerHTML = 
                        '<h2>Statistiques</h2>' +
                        '<p>Total événements: ' + data.total_events + '</p>' +
                        '<p>Utilisateurs uniques: ' + data.unique_users + '</p>' +
                        '<p>Artistes uniques: ' + data.unique_artists + '</p>';
                })
                .catch(err => {
                    document.getElementById('stats').innerHTML = '<p>Erreur: ' + err + '</p>';
                });
        </script>
    </body>
    </html>
    """

@app.route('/api/stats')
def stats():
    return jsonify({
        'total_events': 100,
        'unique_users': 25,
        'unique_artists': 40,
        'unique_tracks': 85
    })

if __name__ == '__main__':
    print("Dashboard simple démarré sur http://localhost:5001")
    app.run(host='0.0.0.0', port=5001, debug=False)
