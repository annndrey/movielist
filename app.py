import json
from imdb import Cinemagoer
from rapidfuzz import fuzz

from flask import Flask

from modules.actors.models import Actor
from modules.movies.models import Movie 
from modules.genres.models import Genre

from modules.movies import MovieAPI
from modules.actors import ActorAPI
from modules.genres import GenreAPI
from modules.db import session

app = Flask(__name__)

# Adding modules
app.register_blueprint(MovieAPI)
app.register_blueprint(ActorAPI)
app.register_blueprint(GenreAPI)


#@app.before_first_request
def fill_db():
    app.logger.info("Filling DB with some data from data/movies.json")
    # Parsing json
    # Validating data
    # Removing invalid entries
    # Put records to the DB

    ia = Cinemagoer()
    with open('./data/movies.json') as json_file:
        json_data = json.loads(json_file.read())
        non_names = ['a', 'an', 'the', 'some', 'many', 'I', 'you', 'he', 'she', 'some', 'to', 'at', 'after', 'on', 'but', 'and', 'but', 'when' ]
        for m in json_data:
            print(m)
            # {'title': 'The Lone Wolf', 'year': 1924, 'cast': ['Dorothy Dalton', 'Jack Holt'], 'genres': ['Mystery']}
            # Add genres
            # Add cast
            # Add  movie title & year
            # add actors and genres
            movie_cast = []
            db_actors = []
            db_genres = []

            # Processing actors
            for a in m['cast']:
                    if len(a.split(" ")) < 2:
                        if a.lower() not in non_names:
                            if a[0].isupper():
                                # Searching actors by name in IMDB
                                people = ia.search_person(a)
                                if len(people) > 0:
                                    found_name = people[0]['name']
                                    # If somethig's found, check for similarity with the source name
                                    sim_ratio = fuzz.ratio(a, found_name)
                                    # If initial name and the IMDB data are quite similar,
                                    # we can add it to the DB
                                    if sim_ratio > 75:
                                        movie_cast.append(found_name)
                    else:
                        # OK 
                        # print(a)
                        movie_cast.append(a)
            # Adding actors to the DB
            for a in movie_cast:
                actor = session.query(Actor).filter(Actor.name == a).first()
                if actor is None:
                    actor = Actor(name=a)
                    session.add(actor)
                    session.commit()
                db_actors.append(actor)
            # Processing genres
            for g in m['genres']:
                genre = session.query(Genre).filter(Genre.name == g).first()
                if genre is None:
                    genre = Genre(name=g)
                    session.add(genre)
                    session.commit()
                db_genres.append(genre)
            # Finally adding movies
            movie = Movie(title=m['title'], year=m['year'])
            movie.cast = db_actors
            movie.genres = db_genres
            session.add(movie)
            session.commit()
    

@app.route("/")
def hello():
    greetings = """🎥 Welcome to our movie database! 🎥
    Feel free to look around and find some movies to watch.
    
    A full list of movies is available at /movies
    Actors list can be reaced by hitting the /actors URL
    And all collected genres can be obtained from here 👉 /genres

    Since our collection is huge, we added some pagination to speed up the results to load.
    It can be turned on by providing additional argument ?page=NUM_PAGE to the URL, 
    especially for the movies list.

    If you decide to add a new entry to our collection, pick a list of authors & genres,
    provide a movie ttitle and release year and just send us a POST request to /movies with
    all your data in JSON format. The following fields  are required: year, title, 
    cast[list], genres[list]. If everything is OK, you'll see your new entry together with it's ID.
    
    To edit an already added entry, please sent the PATCH request to the /movies/[MOVIE_ID] endpoint

    If for some reason you've decided to delete a movie from the collection, send the DELETE 
    request to /movies/[MOVIE_ID
    
    ###

    Our service provide some basic stats for authors and movies. 

    To get a list of actors aggregated by the years of release
    of the films in which he starred, with the number of films released this year, 
    send a GET request to /actors_stats.
    
    Sample output:
    ...
    [ "Claire McDowell", 1913, 53   ],
    [ "Claire McDowell", 1922, 421 ],
    [ "Claire McDowell", 1923, 395 ],
    ...

    """
    return greetings
    
if __name__ == '__main__':
    app.run(debug=True, port=9005)
