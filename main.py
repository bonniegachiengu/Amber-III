from flask import Flask, abort, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
# from flask_gravatar import Gravatar
# from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user
# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
# from sqlalchemy import Integer, String, Text
# from functools import wraps
# from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
from data import movies, watchlists, genres
import tools
import os

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
ckeditor = CKEditor(app)
Bootstrap5(app)


@app.route("/")
def home():
    return render_template("index.html", movies=movies, watchlists=watchlists)


@app.route("/library")
def library():
    # rank movie directors based on the ranks of their movies
    directors = tools.rank_directors(movies)
    num_of_movies = len(movies)
    num_of_directors = len(directors)
    num_of_watchlists = len(watchlists)
    return render_template("library.html",
        movies=movies,
        watchlists=watchlists,
        directors=directors,
        directors_dict=dict(directors),
        num_of_movies=num_of_movies,
        num_of_watchlists=num_of_watchlists,
        num_of_directors=num_of_directors,
        genres=genres,
    )


@app.route("/movie/<int:movie_id>")
def movie(movie_id):
    # find the movie with the given id
    movie = next((movie for movie in movies if movie["id"] == movie_id), None)
    if movie is None:
        abort(404)
    return render_template("film.html", movie=movie)


@app.route("/player")
def player():
    return render_template("player.html")


@app.route("/people")
def people():
    return render_template("people.html")


if __name__ == "__main__":
    app.run(debug=True)
