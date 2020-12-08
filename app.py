
from flask import Flask
from flask import redirect, render_template, request, session
from os import getenv
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

import database

@app.route("/")
def index():
    if session.get('username') != None:
        user = database.get_user_by_name(session["username"])
        return render_template("index.html", admin=user[3])

    return render_template("index.html")



@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    
    error = None

    user = database.get_password_by_username(username)

    if user == None:
        error = "Ei käyttäjätunnusta"
    else:
        hash_value = user[0]
        if check_password_hash(hash_value,password):
            session["username"] = username
            return redirect("/")
        else:
            error = "Väärä salasana"

    return render_template("index.html", error=error)

    

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

@app.route("/signup")
def getsignup():
   return render_template("signup.html")

@app.route("/signup", methods=["POST"])
def signup():
    username = request.form["username"]
    password = request.form["password"]
    admin = request.form.get('admin') != None

    user = database.get_user_by_name(username)
      
    if username == "" or password == "":
        error = "Täytä kaikki kentät"
    elif user != None:
        error = "Käyttäjänimi on jo varattu"
    else:
        database.add_user(username, password, admin)
        session["username"] = username
        return redirect("/")

    return render_template("signup.html", error=error)

@app.route("/pokemons")
def pokemons():
    count = database.get_pokemon_count()
    pokemons = database.get_pokemons()

    if session.get('username') != None:
        user = database.get_user_by_name(session["username"])
        return render_template("pokemons.html", count=count, pokemons=pokemons, admin=user[3]) 

    return render_template("pokemons.html", count=count, pokemons=pokemons) 

@app.route("/pokemons/<int:id>")
def pokemon(id):
    pokemon = database.get_pokemon_by_id(id)
    
    if session.get('username') != None:
        user = database.get_user_by_name(session["username"])
        return render_template("pokemon.html", pokemon=pokemon, admin=user[3]) 

    return render_template("pokemon.html", pokemon=pokemon)

@app.route("/profile")
def profile():
    if session.get('username') == None:
        return redirect("/")

    user = database.get_user_by_name(session["username"])
    pokemons = database.get_user_pokemons(user[0])
    
    if pokemons != None:
        return render_template("profile.html", pokemons=pokemons, admin=user[3])
        
    return render_template("profile.html", admin=user[3])

@app.route("/profile", methods=["POST"])
def profileadd():
    id = request.form["id"]
    
    user = database.get_userid_by_name(session["username"])  
    database.add_userpokemon(user[0], id)
    return redirect("/profile")


@app.route("/add")
def add():
    if session.get('username') == None:
        return redirect("/")
    
    user = database.get_user_by_name(session["username"])

    if user[3] == False:
        return redirect("/")
    
    return render_template("add.html")

@app.route("/add", methods=["POST"])
def addpokemon():
    if session.get('username') == None:
        return redirect("/")

    user = database.get_user_by_name(session["username"])

    if user[3] == False:
        return redirect("/")
    
    name = request.form["name"]
    tyyppi = request.form["type"]
    kuvaus = request.form["kuvaus"]

    database.add_pokemon(name, tyyppi, kuvaus)

    return redirect("/pokemons")
