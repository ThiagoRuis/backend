import os, requests, json
from flask import Flask, request

app = Flask(__name__)
app.config['TMDB_API_KEY'] = '1f54bd990f1cdfb230adb312546d765d'


@app.route("/")
def index():
    return "Ruis API"


@app.route("/upcoming/<page>")
def get_upcoming_movies(page):
    genreDict = get_genre_list()

    url = "https://api.themoviedb.org/3/movie/upcoming"

    payload = {
        'api_key': app.config['TMDB_API_KEY'],
        'page': page
    }
    response = requests.request("GET", url, data=payload)
    imdbAPIResponse = json.loads(response.text)
    moviesList = imdbAPIResponse['results']
    movies = []

    for item in moviesList:
        genre_list = []
        for genre_id in item['genre_ids']:
            genre_list.append(genreDict[genre_id])

        movie = {
            'id' : item['id'],
            'title' : item['title'],
            'poster_img' : item['poster_path'],
            'genre_ids' : item['genre_ids'],
            'genre_list': genre_list,
            'overview' : item['overview'],
            'release_date' : item['release_date'],
        }
        movies.append(movie)

    return json.dumps(movies)


@app.route("/movies/<movie_id>")
def get_movie_details(movie_id):
    url = "https://api.themoviedb.org/3/movie/" + movie_id
    payload = {
        'api_key': app.config['TMDB_API_KEY'],
    }
    response = requests.request("GET", url, data=payload)
    response_json = json.loads(response.text)

    movie = {
        'id': response_json['id'],
        'title': response_json['title'],
        'poster_img': response_json['poster_path'],
        'genres': response_json['genres'],
        'overview': response_json['overview'],
        'release_date': response_json['release_date'],
    }
    return json.dumps(movie)


@app.route("/search/<search_string>")
def search_movie(search_string):
    genreDict = get_genre_list()
    url = "https://api.themoviedb.org/3/search/movie"
    payload = {
        'api_key': app.config['TMDB_API_KEY'],
        'query': search_string
    }
    response = requests.request("GET", url, data=payload)
    response_json = json.loads(response.text)

    movies = []
    for item in response_json['results']:
        genre_list = []
        for genre_id in item['genre_ids']:
            genre_list.append(genreDict[genre_id])

        movie = {
            'id': item['id'],
            'title': item['title'],
            'poster_img': item['poster_path'],
            'genre_ids': item['genre_ids'],
            'genre_list': genre_list,
            'overview': item['overview'],
            'release_date': item['release_date'],
        }
        movies.append(movie)

    search_results = {
        'movies': movies,
        'total_results': response_json['total_results'],
        'total_pages': response_json['total_pages'],
        'page': response_json['page'],
        'search_string': search_string
    }

    return json.dumps(search_results)


def get_genre_list():
    url = "https://api.themoviedb.org/3/genre/movie/list"

    payload = {
        'api_key': app.config['TMDB_API_KEY'],
    }
    response = requests.request("GET", url, data=payload)

    genreDict = {}
    for genre in json.loads(response.text)['genres']:
        genreDict[genre['id']] = genre['name']

    return genreDict

if __name__ == '__main__':
    app.run()