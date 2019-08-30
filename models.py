import json
from app import db

#
# class Movie(db.Model):
#     __tablename__ = 'movies'
#
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String())
#     poster_img = db.Column(db.String())
#     genre = db.Column(db.String())
#     overview = db.Column(db.String())
#     release_date = db.Column(db.String())
#
#     def __init__(self, name):
#         self.name = name
#
#     def __repr__(self):
#         return '<id {}>'.format(self.id)
#
#     def serialize(self):
#         return {
#             'id': self.id,
#             'name': self.name,
#             'poster_img': self.poster_img,
#             'genre': self.genre,
#             'overview': self.overview,
#             'release_date': self.release_date,
#         }
#

class ResponseMovie(object):
    def __init__(self, data):
        self.__dict__ = json.loads(data)