from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests

# Create DB
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///movie-collections.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
Bootstrap(app)
db = SQLAlchemy(app)


# Create table
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(500), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    ranking = db.Column(db.Integer, nullable=False)
    review = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)


db.create_all()


class RateMovieForm(FlaskForm):
    rating = StringField(label="Your Rating Out of 10 e.g. 7.5", validators=[DataRequired()])
    review = StringField(label="Your Review", validators=[DataRequired()])
    submit = SubmitField(label="Done")


@app.route("/")
def home():
    all_movies = Movie.query.all()
    return render_template("index.html", movies=all_movies)


@app.route("/add")
def add():
    # if request.method == "POST":
    #     new_movie = Movie(
    #         title=request.form["title"],
    #         year=request.form["year"],
    #         description=request.form["description"],
    #         rating=request.form["rating"],
    #         ranking=request.form["ranking"],
    #         review=request.form["review"],
    #         img_url=request.form["img_url"]
    #     )
    #     print(new_movie)
    #     db.session.add(new_movie)
    #     db.session.commit()
    #     return redirect(url_for("home"), movie=new_movie)
    return render_template("add.html")


@app.route("/edit", methods=["GET", "POST"])
def edit():
    form = RateMovieForm()
    movie = request.args.get("id")
    movie_to_update = Movie.query.get(movie)
    # if request.method == "POST":
    if form.validate_on_submit():
        movie_to_update.rating = float(form.rating.data)
        movie_to_update.review = form.review.data
        db.session.commit()
        return redirect(url_for("home"))

    return render_template("edit.html", form=form, movie=movie)


@app.route("/select")
def select():
    return render_template("select.html")


if __name__ == '__main__':
    app.run(debug=True)
