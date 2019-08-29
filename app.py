from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from models import Movie

app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

@app.route("/")
def index():
    return "Ruis API"

@app.route("/upcoming")
def get_upcoming_moovies():
    return "{}"

@app.route("/movies/<movie_id>")
def get_movie_details(movie_id):
    return "{'movie': 'Selected movie'}"

if __name__ == '__main__':
    app.run()