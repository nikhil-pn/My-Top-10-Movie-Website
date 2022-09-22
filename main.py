from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///moviescollections.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
Bootstrap(app)


class MovieForm(FlaskForm):
    rating = IntegerField('Rating', validators=[DataRequired()])
    review = StringField("Review", validators=[DataRequired()])
    submit = SubmitField('Submit', )


class AddMovieForm(FlaskForm):
    movie_title = StringField("Movie Title", validators=[DataRequired()])
    submit = SubmitField('Submit', )


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=False, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    ranking = db.Column(db.Integer, nullable=False)
    review = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)

    # Optional: this will allow each book object to be identified by its title when printed.
    def __repr__(self):
        return f'<Movies {self.title}>'


db.create_all()
all_movies = Movie.query.all()

print(all_movies)

length = len(all_movies)


@app.route("/")
def home():
    all_movies = Movie.query.all()
    length = len(all_movies)
    order_desc = db.session.query(Movie).order_by(desc(Movie.rating)).all()
    db.session.commit()
    print(order_desc)
    print(len(order_desc))
    print(order_desc[0])
    return render_template("index.html", all_movies=order_desc, length=length)


@app.route("/edit", methods=["GET", "POST"])
def edit():
    form = MovieForm()
    movie_id = request.args.get("id")
    if form.validate_on_submit():
        print("True")
        # x = request.args['nu']
        # print(x)
        rating = form.rating.data
        review = form.review.data
        print(rating)
        print(review)

        change_rating = db.session.query(Movie).get(movie_id)
        change_rating.rating = rating
        change_rating.review = review

        db.session.commit()
        return redirect(url_for("home"))

    return render_template("edit.html", form=form)


@app.route("/delete", methods=["GET", "POST"])
def delete():
    x = request.args['nu']
    print(x)
    n = int(x)
    db.session.query(Movie).filter(Movie.id == n).delete()
    db.session.commit()

    return redirect(url_for("home"))


@app.route("/add", methods=["GET", "POST"])
def add():
    form = AddMovieForm()
    if form.validate_on_submit():
        print("True")
        movie_title = form.movie_title.data
        # print(movie_title)
        responses = requests.get(
            url=f"https://api.themoviedb.org/3/search/movie?api_key=3b43749597c33e33c3134c94e8400382&language=en-US&query={movie_title}&page=1")
        # print(responses.json()["results"][0]["title"])
        results = len(responses.json()["results"])
        result_int = int(results)
        return render_template("select.html", responses=responses, result_int=result_int)
    return render_template("add.html", form=form)


@app.route("/new_home", methods=["GET", "POST"])
def new_home():
    title = request.args["title"]
    release_date = request.args["release_date"]
    poster_path = request.args["poster_path"]
    vote_average = request.args["vote_average"]
    overview = request.args["overview"]
    id_str = request.args["id"]

    id_int = int(id_str)

    print(title)
    print(release_date)
    print(poster_path)
    print(vote_average)
    print(overview)
    print(id)

    new_movie = Movie(
        id=id_int,
        title=title,
        year=release_date,
        description=overview,
        rating=vote_average,
        ranking=10,
        review="My favourite character was the caller.",
        img_url=f"https://image.tmdb.org/t/p/w500{poster_path}"

    )
    db.session.add(new_movie)
    db.session.commit()

    db.session.query(Movie).order_by(Movie.rating).all()
    all_movies = Movie.query.all()
    length = len(all_movies)
    order = db.session.query(Movie).order_by(desc(Movie.rating)).all()
    db.session.commit()
    print(order)
    print(all_movies)
    order_desc = db.session.query(Movie).order_by(desc(Movie.rating)).all()
    db.session.commit()
    return redirect(url_for("edit", id=id_int))


@app.route("/newedit", methods=["GET", "POST"])
def newedit():
    form = MovieForm()
    if form.validate_on_submit():
        print("True")
        x = request.args['nu']
        print(x)
        rating = form.rating.data
        review = form.review.data
        print(rating)
        print(review)

        change_rating = db.session.query(Movie).get(x)
        change_rating.rating = rating
        change_rating.review = review

        db.session.commit()
        return redirect(url_for("home"))

    return render_template("edit.html", form=form)


if __name__ == '__main__':
    app.run(debug=True)
