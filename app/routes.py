from flask import Blueprint, render_template, request
import pandas as pd
from .recommender import get_recommendations

main = Blueprint("main", __name__)
ratings = pd.read_csv("data/ml-latest-small/ratings.csv")
movies = pd.read_csv("data/ml-latest-small/movies.csv")
data = pd.merge(ratings, movies, on="movieId")
movie_titles = sorted(data['title'].unique())

@main.route("/", methods=["GET"])
def home():
    return render_template("index.html", movies=movie_titles)

@main.route("/recommend", methods=["POST"])
def recommend():
    movie = request.form["movie"]
    recommendations = get_recommendations(movie, data)
    if not recommendations:
        message = f"No strong recommendations found for '{movie}'. Try selecting another movie!"
        return render_template("index.html", movies=movie_titles, message=message)
    return render_template("index.html", movies=movie_titles, recommendations=recommendations)
