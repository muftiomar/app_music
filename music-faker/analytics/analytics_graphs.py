import os
import pandas as pd
import matplotlib.pyplot as plt

STORAGE_DIR = os.path.dirname(__file__) + '/../storage/'

# Top artistes
artistes = pd.read_csv(STORAGE_DIR + 'top_artists.csv', index_col=0, header=0, names=["artist", "plays"])
artistes = artistes.sort_values("plays", ascending=False).head(10)
plt.figure(figsize=(10,5))
artistes["plays"].plot(kind="bar", color="skyblue")
plt.title("Top 10 artistes les plus écoutés")
plt.ylabel("Nombre d'écoutes")
plt.xlabel("Artiste")
plt.tight_layout()
plt.savefig(STORAGE_DIR + 'top_artists.png')
plt.close()

# Genres par heure
genres_hour = pd.read_csv(STORAGE_DIR + 'genres_by_hour.csv', index_col=0)
plt.figure(figsize=(12,7))
genres_hour.sum(axis=1).plot()
plt.title("Nombre total d'écoutes par heure (tous genres confondus)")
plt.ylabel("Nombre d'écoutes")
plt.xlabel("Heure")
plt.tight_layout()
plt.savefig(STORAGE_DIR + 'listens_by_hour.png')
plt.close()

# Heatmap genres x heure
import seaborn as sns
plt.figure(figsize=(16,8))
sns.heatmap(genres_hour, cmap="YlGnBu")
plt.title("Heatmap : Genres préférés par heure")
plt.ylabel("Heure")
plt.xlabel("Genre musical")
plt.tight_layout()
plt.savefig(STORAGE_DIR + 'genres_by_hour_heatmap.png')
plt.close()

# Plateforme x pays (top 10 pays)
country_plat = pd.read_csv(STORAGE_DIR + 'listens_by_country_platform.csv', index_col=0)
top_countries = country_plat.sum(axis=1).sort_values(ascending=False).head(10).index
plt.figure(figsize=(14,7))
country_plat.loc[top_countries].plot(kind="bar", stacked=True)
plt.title("Écoutes par plateforme dans les 10 pays les plus actifs")
plt.ylabel("Nombre d'écoutes")
plt.xlabel("Pays")
plt.tight_layout()
plt.savefig(STORAGE_DIR + 'country_platform.png')
plt.close()

print("Graphiques générés dans le dossier storage !")
