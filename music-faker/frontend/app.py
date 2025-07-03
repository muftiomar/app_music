from flask import Flask, jsonify, render_template
import pandas as pd
import os

app = Flask(__name__)
STORAGE_DIR = os.path.dirname(__file__) + '/../storage/'

@app.route("/api/top_artists")
def api_top_artists():
    df = pd.read_csv(STORAGE_DIR + 'top_artists.csv', index_col=0, header=0, names=["artist", "plays"])
    data = df.sort_values("plays", ascending=False).head(10).reset_index().to_dict(orient="records")
    return jsonify(data)

@app.route("/api/genres_by_hour")
def api_genres_by_hour():
    df = pd.read_csv(STORAGE_DIR + 'genres_by_hour.csv', index_col=0)
    data = df.reset_index().to_dict(orient="records")
    return jsonify(data)

@app.route("/api/country_platform")
def api_country_platform():
    df = pd.read_csv(STORAGE_DIR + 'listens_by_country_platform.csv', index_col=0)
    data = df.reset_index().to_dict(orient="records")
    return jsonify(data)

@app.route("/")
def dashboard():
    return render_template("dashboard.html")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
