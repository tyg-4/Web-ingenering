from dataclasses import dataclass
import random
from typing import List
from fastapi import FastAPI, HTTPException
import uvicorn
import psycopg2
from fastapi.middleware.cors import CORSMiddleware

db = psycopg2.connect("host=localhost dbname=WebAppAPI user=postgres password=Diladada1982/( port=5489")
cur = db.cursor()

@dataclass(frozen=True)
class Film:
    title: str
    director: str
    year: int
    actors: List[str]

app = FastAPI()

cur.execute("DROP TABLE IF EXISTS actors")
db.commit()
cur.execute("DROP TABLE IF EXISTS films")
db.commit()

cur.execute("CREATE TABLE films ( id SERIAL PRIMARY KEY, title VARCHAR(100), director VARCHAR(100), year INT );")
db.commit()
cur.execute("CREATE TABLE actors ( idact SERIAL PRIMARY KEY, actor1 VARCHAR(100), actor2 VARCHAR(100), actor3 VARCHAR(100), actor4 VARCHAR(100), actor5 VARCHAR(100), actor6 VARCHAR(100), actor7 VARCHAR(100) );")
db.commit()

cur.execute("INSERT INTO films (title, director, year) VALUES ('Drive', 'Nicolas Winding Refn', 2011)")
db.commit()
cur.execute("INSERT INTO actors (actor1, actor2, actor3, actor4, actor5, actor6, actor7) VALUES ('Ryan Gosling', 'Carey Mulligan', 'Bryan Cranston', 'Albert Brooks', '', '', '')")
db.commit()
cur.execute("INSERT INTO films (title, director, year) VALUES ('The Dark Knight', 'Christopher Nolan', 2008)")
db.commit()
cur.execute("INSERT INTO actors (actor1, actor2, actor3, actor4, actor5, actor6, actor7) VALUES ('Christian Bale', 'Heath Ledger', 'Aaron Eckhart', 'Maggie Gyllenhaal', 'Gary Oldman', 'Michael Caine', 'Morgan Freeman')")
db.commit()
cur.execute("INSERT INTO films (title, director, year) VALUES ('Interstellar', 'Christopher Nolan', 2014)")
db.commit()
cur.execute("INSERT INTO actors (actor1, actor2, actor3, actor4, actor5, actor6, actor7) VALUES ('Matthew McConaughey', 'Anne Hathaway', 'Jessica Chastain', 'Mackenzie Foy', 'Michael Caine', '', '')")
db.commit()
cur.execute("INSERT INTO films (title, director, year) VALUES ('The Gentelmen', 'Guy Ritchie', 2019)")
db.commit()
cur.execute("INSERT INTO actors (actor1, actor2, actor3, actor4, actor5, actor6, actor7) VALUES ('Matthew McConaughey', 'Charlie Hunnam', 'Henry Golding', 'Hugh Grant', 'Michelle Dockery', 'Jeremy Strong', 'Eddie Marsan')")
db.commit()
cur.execute("INSERT INTO films (title, director, year) VALUES ('Spider-Man', 'Sam Raimi', 2002)")
db.commit()
cur.execute("INSERT INTO actors (actor1, actor2, actor3, actor4, actor5, actor6, actor7) VALUES ('Tobey Maguire', 'Willem Dafoe', 'Kirsten Dunst', 'James Franco', 'Cliff Robertson', 'Rosemary Harris', 'J.K. Simmons')")
db.commit()
DATA_FILMS = []

def correctFilm(film):
    i = 5
    actors = [1, 1, 1, 1, 1, 1, 1]
    while (i < 12):
        if film[i] == "":
            break
        actors[i-5] = film[i]
        i += 1
    for d in range (0, 7, 1):
        try:
            actors.remove(1)
        except:
            break
    return Film(film[1], film[2], film[3], actors)

def correctDBFilms(films):
    i = 0
    dtbs = []
    while (i < len(films)):
        dtbs.append(correctFilm(films[i]))
        i += 1
    return dtbs

cur.execute("SELECT * FROM films, actors WHERE id = idact")
films = cur.fetchall()
DATA_FILMS = correctDBFilms(films)

@app.get("/")
async def home():
    return {"message": "Welcome to films app!"}

@app.get("/list_of_films")
async def list_of_films():
    return {"Films": DATA_FILMS}

@app.get("/get_by_id/{Index}")
async def get_by_id(Index: int):
    if(Index < 0 or Index > (len(DATA_FILMS)-1)):
        raise HTTPException(404, f"Index {Index} is out of range {len(DATA_FILMS)}.")
    else:
        return {"film": DATA_FILMS[Index]}

@app.get("/movie_for_tonight")
async def random_film():
    return random.choice(DATA_FILMS)

@app.post("/add_film")
async def add_film(film: Film):
    stractor = "actor1"
    stractorval = f"'{film.actors[0]}'"
    for i in range (1, len(film.actors), 1):
        stractor += f", actor{i+1}"
        stractorval += f", '{film.actors[i]}'"
    cur.execute(f"INSERT INTO films (title, director, year) VALUES ('{film.title}', '{film.director}', {film.year})")
    db.commit()
    cur.execute(f"INSERT INTO actors ({stractor}) VALUES ({stractorval})")
    db.commit()
    cur.execute("SELECT * FROM films, actors WHERE id = idact")
    films = cur.fetchall()
    DATA_FILMS = correctDBFilms(films)
    return {"message": f"film '{film.title}' was added."}
