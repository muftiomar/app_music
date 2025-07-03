# Documentation et Architecture

## TODO pour cette partie

### Partie 1 - Choix d'Architecture
Fichiers à créer :
1. `architecture_choice.md` - Justification écrite
2. `architecture_slide.pptx` - Diapositive pour présentation

**Question centrale** : DataLake, DataWarehouse ou Lakehouse ?

**Points à traiter** :
- Types de données collectées (structurées/semi-structurées)
- Besoins temps réel vs batch
- Outils et formats associés
- Pertinence pour le domaine musical

### Partie 2 - Schéma de Traitement
Fichiers à créer :
1. `pipeline_schema.png` - Schéma illustré (draw.io, Lucidchart)
2. `pipeline_description.md` - Description des flux

**Composants à inclure** :
- Producer (simulateur Python)
- Kafka (moteur de streaming)
- Spark Streaming (consumer)
- HDFS (stockage DataLake)
- Spark SQL/Hive (traitement analytique)
- Flask/React (frontend)

### Livrables Finaux
1. **Document PDF structuré** avec :
   - Justification architecture
   - Schéma global
   - Description pipeline
   - Captures frontend
   - Répartition des rôles
   - Difficultés/limites

2. **Slides de soutenance** :
   - 1 slide par personne
   - 5-10 min de présentation

### Outils suggérés :
- **Diagrammes** : draw.io, Lucidchart, Canva
- **Documentation** : Markdown, LaTeX
- **Présentation** : PowerPoint, Google Slides
