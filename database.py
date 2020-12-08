from app import app
from flask_sqlalchemy import SQLAlchemy
from os import getenv
from werkzeug.security import generate_password_hash

app.secret_key = getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


def get_user_by_name(username):
    sql = "SELECT * FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()    
    return user

def get_userid_by_name(username):
    sql = "SELECT id FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()  
    return user

def get_password_by_username(username):
    sql = "SELECT password FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    return user   

def get_pokemons():
    result = db.session.execute("SELECT * FROM pokemons")
    pokemons = result.fetchall()
    return pokemons

def get_pokemon_count():
    result = db.session.execute("SELECT COUNT(*) FROM pokemons")
    count = result.fetchone()[0]
    return count

def get_pokemon_by_id(id):
    sql = "SELECT * FROM pokemons WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    pokemon = result.fetchone()
    return pokemon

def get_user_pokemons(id):
    sql = "SELECT pokemons.id, pokemons.nimi FROM userPokemons JOIN pokemons ON pokemons.id = userPokemons.pokemon_id WHERE user_id=:user_id"
    result = db.session.execute(sql, {"user_id":id})
    pokemons = result.fetchall()
    return pokemons

def get_pokemons_search(query, hakutermi):
    if hakutermi == "nimi":
        sql = "SELECT * FROM pokemons WHERE nimi LIKE :query"
    elif hakutermi == "tyyppi":
        sql = "SELECT * FROM pokemons WHERE tyyppi LIKE :query"
    elif hakutermi == "kuvaus":
        sql = "SELECT * FROM pokemons WHERE kuvaus LIKE :query"
    else:
        sql = "SELECT * FROM pokemons WHERE nimi LIKE :query OR tyyppi LIKE :query OR kuvaus LIKE :query"

    result = db.session.execute(sql, {"query":"%"+query+"%"})
    pokemons = result.fetchall()
    return pokemons

def add_user(username, password, admin):
    hash_value = generate_password_hash(password)
    sql = "INSERT INTO users (username,password,admin) VALUES (:username,:password,:admin)"
    db.session.execute(sql, {"username":username,"password":hash_value,"admin":admin})
    db.session.commit()

def add_userpokemon(user_id, pokemon_id):
    sql = "INSERT INTO userpokemons (user_id, pokemon_id) VALUES (:user_id,:pokemon_id)"
    db.session.execute(sql, {"user_id":user_id,"pokemon_id":pokemon_id})
    db.session.commit()
    
def add_pokemon(nimi, tyyppi, kuvaus):
    sql = "INSERT INTO pokemons (nimi, tyyppi, kuvaus) VALUES (:nimi,:tyyppi,:kuvaus)"
    db.session.execute(sql, {"nimi":nimi,"tyyppi":tyyppi,"kuvaus":kuvaus})
    db.session.commit()
