#!/usr/bin/env python3
"""
Script pour démarrer le dashboard sans debug mode
"""
from app import app

if __name__ == '__main__':
    print("🎵 Démarrage du frontend Music-Faker...")
    print("📊 Dashboard disponible sur: http://localhost:5001")
    print("🔄 Les données se rafraîchissent automatiquement toutes les 30 secondes")
    
    app.run(host='0.0.0.0', port=5001, debug=False)
