from flask import Flask, request

app = Flask(__name__)

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