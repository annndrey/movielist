from flask import Blueprint, jsonify, request
from sqlalchemy import func
from marshmallow import fields, Schema
from .models import Actor, actor_association_table
from .. import db
from .. import movies

ActorAPI = Blueprint('ActorAPI', __name__)
Movie = movies.models.Movie


class ActorSchema(Schema):
    id  = fields.Int(required=False)
    name = fields.Str(required=True)


@ActorAPI.route('/actors')
def actors():
    page = request.args.get('page', 0, type=int)
    per_page = 10
    offset = per_page * page
    
    actor_schema = ActorSchema()
    all_actors = [actor_schema.dump(a) for a in db.session.query(Actor).limit(per_page).offset(offset).all()]
    
    return jsonify(all_actors)


@ActorAPI.route('/actors_stats')
def actors_stats():
    # 2.2.The user should be able to get a list of actors aggregated by the years of release
    # of the films in which he starred, with the number of films released this year.
    # Example:
    # Ashton Kutcher, 2006, 2
    # Ashton Kutcher, 2007, 1
    # Gary Sinise, 2005, 3
    # Gary Sinise, 2006, 4
    actors_query = db.session.query(Actor.name, Movie.year).filter(actor_association_table.c.actor_id == Actor.id).filter(actor_association_table.c.movie_id==Movie.id)
    asq = actors_query.subquery()
    years_count_query = db.session.query(Movie.year, func.count(Movie.year)).group_by(Movie.year)
    ysq = years_count_query.subquery()
    result = db.session.query(asq.c.name, asq.c.year, ysq.c.count).filter(asq.c.year==ysq.c.year).order_by(asq.c.name).all()
        
        
    return jsonify([[r[0], r[1], r[2]] for r in result])
