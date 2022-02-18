# MovieList API Demo

## Available endpoints

- /  -> basic info about available features
- GET /actors -> list of all actors
- GET /actors_stats -> Some basic actors/movies stats (a list of actors aggregated by the years of release of the films in which he starred, with the number of films released this year.)
- GET /genres -> list of all genres
- GET /movies -> list of all movies
- POST /movies -> add a new movie
- PATCH /movies/<id> -> edit an exising movie
- DELETE /movies/<id> -> delete a movie

### Live demo

Live demo could be accesed here:
[https://demo-api.testapi.me](https://demo-api.testapi.me/actors_stats)

### External packages
- [cinemagoer](https://github.com/cinemagoer/cinemagoer) for actor names validation
- [rapidfuzz](https://github.com/maxbachmann/RapidFuzz) for string similarity estimation

### Run the app

```
python3 -m venv .venv
source .venv/bin/activate
pip install requirements.txt
python app.py
```