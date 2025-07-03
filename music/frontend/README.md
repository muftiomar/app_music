# Frontend - Interface Web et API

## TODO pour cette partie

### Option 1 : Flask + Charts
Fichiers à créer :
1. `app.py` - Application Flask principale
2. `api.py` - API pour servir les métriques
3. `templates/dashboard.html` - Interface web
4. `static/js/charts.js` - Graphiques interactifs

### Option 2 : React + Chart.js
Fichiers à créer :
1. `package.json` - Configuration npm
2. `src/App.js` - Composant principal
3. `src/components/Dashboard.js` - Tableau de bord
4. `src/services/api.js` - Appels API

### Graphiques requis (minimum 2) :
1. **Écoutes par genre/artiste**
   - Graphique en barres ou camembert
   - Filtres par période
   
2. **Heures de pics d'écoute**
   - Graphique linéaire
   - Heatmap par pays

### API Endpoints nécessaires :
- `GET /api/top-artists` - Top artistes
- `GET /api/genres-by-hour` - Genres par heure  
- `GET /api/listens-by-country` - Écoutes par pays
- `GET /api/platform-stats` - Stats par plateforme

### Technologies suggérées :
- **Flask** : Simple et rapide à mettre en place
- **React** : Plus moderne, meilleure UX
- **Chart.js/Plotly** : Bibliothèques de graphiques
