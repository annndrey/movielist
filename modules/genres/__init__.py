from flask import Blueprint, jsonify
from marshmallow import fields, Schema
from .models import Genre
from .. import db


GenreAPI = Blueprint('GenreAPI', __name__)


class GenreSchema(Schema):
    id  = fields.Int(required=False)
    name = fields.Str(required=True)

    
@GenreAPI.route('/genres')
def genres():
    genre_schema = GenreSchema()
    all_genres = db.session.query(Genre).all()
    res = [genre_schema.dump(g) for g in all_genres]
    return jsonify(res)
