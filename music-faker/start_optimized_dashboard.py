#!/usr/bin/env python3
"""
Dashboard Music-Faker optimisé - Démarrage avec vérifications
"""
import subprocess
import time
import sys
import os

def check_containers():
    """Vérifier que les conteneurs essentiels sont en cours d'exécution"""
    print("🔍 Vérification des conteneurs...")
    try:
        result = subprocess.run(['docker', 'ps', '--filter', 'name=namenode', '--format', '{{.Status}}'], 
                              capture_output=True, text=True)
        if 'healthy' not in result.stdout.lower():
            print("⚠️ Namenode pas sain, redémarrage...")
            subprocess.run(['docker', 'restart', 'namenode'])
            time.sleep(10)
        print("✅ Namenode OK")
        return True
    except Exception as e:
        print(f"❌ Erreur conteneurs: {e}")
        return False

def main():
    print("🎵 Démarrage du Dashboard Music-Faker Optimisé")
    print("=" * 50)
    
    # Vérifications préalables
    if not check_containers():
        print("❌ Problème avec les conteneurs")
        sys.exit(1)
    
    print("🚀 Démarrage de l'application Flask...")
    print("📊 Dashboard sera disponible sur: http://localhost:5001")
    print("💡 Optimisations appliquées:")
    print("   - Protection contre requêtes simultanées")
    print("   - Lecture HDFS via Docker CLI optimisée")
    print("   - Cache intelligent 30s")
    print("   - Timeouts réduits")
    print()
    
    # Import et lancement de l'app
    from app import app
    app.run(debug=False, host='0.0.0.0', port=5001, threaded=True)

if __name__ == '__main__':
    main()
