import os, requests, json
from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/")
def index():
    return "Ruis API"


@app.route("/upcoming/")
def get_upcoming_movies():
    genreDict = get_genre_list()
    img_base_url = get_config()
    movies = []
    url = os.environ.get('BASE_URL') + 'movie/upcoming'

    for index in range(1, 2):
        payload = {
            'api_key': os.environ.get('TMDB_API_KEY'),
            'page': str(index)
        }
        response = requests.request("GET", url, data=payload)
        moviesList = response.json()['results']

        for item in moviesList:
            genre_list = []
            for genre_id in item['genre_ids']:
                genre_list.append(genreDict[genre_id])

            movie = {
                'id' : item.get('id'),
                'title' : item.get('title'),
                'poster_img' : '' if item.get('poster_path') is None else img_base_url + item.get('poster_path'),
                'genre_ids' : item.get('genre_ids'),
                'genre_list': genre_list,
                'overview' : item.get('overview'),
                'release_date' : item.get('release_date'),
            }
            movies.append(movie)

    return json.dumps(movies)


@app.route("/movies/<movie_id>")
def get_movie_details(movie_id):
    img_base_url = get_config()
    url = os.environ.get('BASE_URL') + "movie/" + movie_id
    payload = {
        'api_key': os.environ.get('TMDB_API_KEY'),
    }
    response = requests.request("GET", url, data=payload)
    response_json = json.loads(response.text)



    movie = {
        'id': response_json['id'],
        'title': response_json['title'],
        'poster_img': '' if response_json.get('poster_path') is None else img_base_url + response_json.get('poster_path'),
        'genre_ids': [ genre['id'] for genre in response_json['genres'] ],
        'genre_list': [ genre['name'] for genre in response_json['genres'] ],
        'overview': response_json['overview'],
        'release_date': response_json['release_date'],
    }
    return json.dumps(movie)


@app.route("/search/<search_string>")
def search_movie(search_string):
    genreDict = get_genre_list()
    img_base_url = get_config()

    url = os.environ.get('BASE_URL') + "search/movie"
    payload = {
        'api_key': os.environ.get('TMDB_API_KEY'),
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
            'poster_img': '' if item.get('poster_path') is None else img_base_url + item.get('poster_path'),
            'genre_ids': item['genre_ids'],
            'genre_list': genre_list,
            'overview': item['overview'],
            'release_date': item.get('release_date', ''),
        }
        movies.append(movie)

    return json.dumps(movies)


def get_genre_list():
    url = os.environ.get('BASE_URL') + "genre/movie/list"

    payload = {
        'api_key': os.environ.get('TMDB_API_KEY'),
    }
    response = requests.request("GET", url, data=payload)

    genreDict = {}
    for genre in json.loads(response.text)['genres']:
        genreDict[genre['id']] = genre['name']

    return genreDict


def get_config():
    url = os.environ.get('BASE_URL') + "configuration"

    payload = {
        'api_key': os.environ.get('TMDB_API_KEY'),
    }
    response = requests.request("GET", url, data=payload)

    return response.json()['images']['secure_base_url'] + '/' + os.environ.get('IMAGE_SIZE')


if __name__ == '__main__':
    app.run()