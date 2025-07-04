# 🎵 Pipeline Temps Réel - Guide d'Utilisation Équipe

Salut l'équipe ! 👋

Notre pipeline de données musicales temps réel est **100% opérationnel** ! Voici comment l'utiliser facilement.

## 🚀 Démarrage Ultra-Simple (3 étapes)

### 1️⃣ Aller dans le bon dossier
```bash
cd /Users/omar/Desktop/datalake/app_music/music-faker
```

### 2️⃣ Démarrer tout en une commande
```bash
./start_services.sh
```
*(Attend 30 secondes que tout démarre)*

### 3️⃣ Lancer le pipeline automatique
```bash
python start_realtime_pipeline.py
```

**C'est tout ! 🎉 Le dashboard sera disponible sur http://localhost:5001**

---

## 🎯 Ce que ça fait

Notre pipeline récupère des **événements musicaux en temps réel** :
- 🎤 Artistes qui jouent
- 🎧 Utilisateurs qui écoutent  
- 📱 Plateformes utilisées (Spotify, Apple Music...)
- 🌍 Pays d'écoute
- ⚡ Actions (play, like, skip...)

**Et affiche tout ça sur un dashboard web qui se met à jour automatiquement !**

---

## 📊 Démonstration Rapide

Si vous voulez juste voir le pipeline en action :

```bash
# Démarrer les services
./start_services.sh

# Démo complète automatique
python demo_pipeline.py
```

Ça va vous montrer les stats en temps réel pendant 2 minutes !

---

## 🛠️ Architecture (pour les curieux)

```
Producteur Python → Kafka → Consommateur → HDFS → Dashboard Web
     🎵              📨        💾           🗃️        📊
```

1. **Producteur** : Génère des événements musicaux
2. **Kafka** : Transport des messages 
3. **Consommateur** : Stockage dans HDFS
4. **Dashboard** : Visualisation web temps réel

---

## 🔧 Commandes Utiles

### Générer plus d'événements
```bash
python producer_realtime.py -n 20 -d 1
# Génère 20 événements, 1 par seconde
```

### Voir les stats
```bash
curl http://localhost:5001/api/stats | jq .
```

### Arrêter tout
```bash
docker-compose down
```

---

## 🌐 URLs Importantes

- **📊 Dashboard Principal** : http://localhost:5001
- **📈 API Stats** : http://localhost:5001/api/stats  
- **⚡ API Temps Réel** : http://localhost:5001/api/realtime_metrics
- **🔧 HDFS Web UI** : http://localhost:9871
- **❤️ Santé** : http://localhost:5001/health

---

## 🆘 Si ça marche pas

### Problème Docker ?
```bash
docker-compose down
docker-compose up -d
```

### Dashboard pas accessible ?
```bash
python app.py
# Puis aller sur http://localhost:5001
```

### Pas d'événements ?
```bash
python producer_realtime.py -n 10 -d 0.5
```

---

## 🎉 Résultats Actuels

✅ **39 événements** traités  
✅ **38 artistes uniques**  
✅ **Pipeline 100% fonctionnel**  
✅ **Dashboard temps réel opérationnel**  

---

## 💡 Pour Impressionner

Lancez ça devant quelqu'un :

1. `./start_services.sh` *(attendre 30s)*
2. `python demo_pipeline.py` *(regarder les stats évoluer)*
3. Ouvrir http://localhost:5001 dans le navigateur
4. `python producer_realtime.py -n 50 -d 0.5` *(générer plein d'événements)*
5. Regarder le dashboard se mettre à jour en temps réel ! 🚀

**C'est du Big Data temps réel avec Kafka + HDFS + Dashboard web !** 

---

Des questions ? Ping-moi ! 😄

Omar
