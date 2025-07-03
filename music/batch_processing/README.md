# Traitement Batch - Métriques et Analytics

## TODO pour cette partie

### Fichiers à créer :
1. `metrics_calculator.py` - Script principal de calcul
2. `spark_jobs.py` - Jobs Spark pour l'analyse
3. `hive_queries.sql` - Requêtes Hive complexes

### Métriques à calculer :
1. **Artistes les plus écoutés**
   - Par jour, semaine, mois
   - Par pays, tranche d'âge
   
2. **Genres préférés par tranche horaire**
   - Analyse des patterns d'écoute
   - Heatmap temporelle
   
3. **Écoutes par pays/plateforme**
   - Répartition géographique
   - Comparaison des plateformes

### Format de sortie :
- Tables Hive partitionnées par date
- Fichiers JSON pour l'API frontend
- Format Parquet optimisé

### Technologies suggérées :
- `pyspark.sql` pour les agrégations
- `hive` pour les requêtes complexes
- Partitioning par date pour les performances
