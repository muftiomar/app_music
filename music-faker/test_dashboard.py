#!/usr/bin/env python3
"""
Test simple du dashboard optimisé
"""
import sys
import os
sys.path.append('/Users/omar/Desktop/datalake/app_music/music-faker')

from app import MusicDataManager

def test_data_manager():
    print("🧪 Test du MusicDataManager optimisé...")
    
    manager = MusicDataManager()
    
    # Test 1: Charger les données
    print("\n1️⃣ Test chargement des données...")
    df = manager.get_data(force_refresh=True)
    print(f"Données chargées: {len(df)} lignes")
    
    if not df.empty:
        print(f"Colonnes: {list(df.columns)}")
        print(f"Premiers artistes: {df['artist'].head(3).tolist()}")
        
    # Test 2: Vérifier le cache
    print("\n2️⃣ Test cache...")
    df2 = manager.get_data()  # Ne devrait pas recharger
    print(f"Cache utilisé: {len(df2)} lignes")
    
    print("✅ Test terminé")

if __name__ == '__main__':
    test_data_manager()
