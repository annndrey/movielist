from flask import Blueprint, jsonify, request
from marshmallow import fields, Schema
from .models import Movie
from .. import db
from .. import genres
from .. import actors

MovieAPI = Blueprint('MovieAPI', __name__)
Genre = genres.models.Genre
Actor = actors.models.Actor


class MovieSchema(Schema):
    id  = fields.Int(required=False)
    title = fields.Str(required=True)
    year = fields.Int(required=True)
    genres = fields.Function(lambda obj: [g.name for g in obj.genres])
    cast = fields.Function(lambda obj: [a.name for a in obj.cast])


class MovieInputSchema(Schema):
    id  = fields.Int(required=False)
    title = fields.Str(required=True)
    year = fields.Int(required=True)
    genres = fields.List(fields.String, required=True)
    cast = fields.List(fields.String,  required=True)
    

    
# 2.1.The user should be able to create/edit/delete a movie. Creation and editing should
# be executed by selection actors and genres from the existing ones in the database.
    
@MovieAPI.route('/movies', methods=['GET', ])
def movies():
    page = request.args.get('page', 0, type=int)
    per_page = 10
    offset = per_page * page
    print(page)
    movie_schema = MovieSchema()
    # Getting paginated results
    all_movies = [movie_schema.dump(m) for m in db.session.query(Movie).limit(per_page).offset(offset).all()]
    
    return jsonify(all_movies)

@MovieAPI.route('/movies', methods=['POST', ])
def movies_add():
    movie_schema = MovieSchema()
    movie_input_schema = MovieInputSchema()
    
    json_data = request.json
    # Input validation
    errors = movie_input_schema.validate(json_data)
    if errors:
        return jsonify(errors), 400
    

    title = json_data['title']
    year = json_data['year']
    
    genres = json_data['genres']
    db_genres = db.session.query(Genre).filter(Genre.name.in_(genres)).all()
    
    if len(db_genres) < len(genres):
        # Throwing an error if genre is not found in DB
        return "Only existing genres are allowed", 400
    
    actors = json_data['cast']
    db_actors = db.session.query(Actor).filter(Actor.name.in_(actors)).all()
    
    if len(db_actors) < len(actors):
        # Throwing an error if actore is not found in DB
        return "Only existing actoes are allowed", 400
    
    existing_movie = db.session.query(Movie).filter(Movie.title==title).filter(Movie.year==year).first()
    if existing_movie:
        # Returning an existing movie in case it's already here
        return jsonify(movie_schema.dump(existing_movie)), 409
    
    # Adding a new movie entry
    new_movie = Movie(title =title, year=year)
    new_movie.genres = db_genres
    new_movie.cast = db_actors
    db.session.add(new_movie)
    db.session.commit()
    
    return jsonify(movie_schema.dump(new_movie))


@MovieAPI.route('/movies/<int:movie_id>', methods=['PATCH', ])
def movies_edit(movie_id):
    # Edition of an existing movie
    movie_schema = MovieSchema()
    movie_input_schema = MovieInputSchema()
    
    movie = db.session.query(Movie).filter(Movie.id==movie_id).first()
    if not movie:
        # Throwing 404 in case there's no movie with provided ID 
        return 404
    
    json_data = request.json
    # Input validation
    errors = movie_input_schema.validate(json_data)
    if errors:
        return jsonify(errors), 400
    

    title = json_data['title']
    year = json_data['year']
    
    genres = json_data['genres']
    db_genres = db.session.query(Genre).filter(Genre.name.in_(genres)).all()
    if len(db_genres) < len(genres):
        return "Only existing genres are allowed", 400
    
    actors = json_data['cast']
    db_actors = db.session.query(Actor).filter(Actor.name.in_(actors)).all()
    if len(db_actors) < len(actors):
        return "Only existing actoes are allowed", 400
    # Updating movie record with the new data
    movie.title = title
    movie.year = year
    movie.genres = db_genres
    movie.cast = db_actors
    db.session.add(movie)
    db.session.commit()
    
    return jsonify(movie_schema.dump(movie)), 201


@MovieAPI.route('/movies/<int:movie_id>', methods=['DELETE', ])
def movies_delete(movie_id):
    
    movie = db.session.query(Movie).filter(Movie.id==movie_id).first()
    if not movie:
        return f"Item {movie_id} not found", 404
    # Deleting a movie
    db.session.delete(movie)
    db.session.commit()
    
    return "OK", 204
