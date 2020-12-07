from flask import Flask
from flask import redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from os import getenv
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
app.secret_key = getenv("SECRET_KEY")



@app.route("/")
def index():
    if session.get('username') != None:
        sql = "SELECT * FROM users WHERE username=:username"
        result = db.session.execute(sql, {"username":session["username"]})
        user = result.fetchone()
        return render_template("index.html", admin=user[3])

    return render_template("index.html")



@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    
    error = None

    sql = "SELECT password FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()    
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

    print("admin")
    print(admin)

    sql = "SELECT username FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()    
    if username == "" or password == "":
        error = "Täytä kaikki kentät"
    elif user != None:
        error = "Käyttäjänimi on jo varattu"
    else:
        hash_value = generate_password_hash(password)
        sql = "INSERT INTO users (username,password,admin) VALUES (:username,:password,:admin)"
        db.session.execute(sql, {"username":username,"password":hash_value,"admin":admin})
        db.session.commit()

        session["username"] = username
        return redirect("/")

    return render_template("signup.html", error=error)

@app.route("/pokemons")
def pokemons():
    result = db.session.execute("SELECT COUNT(*) FROM pokemons")
    count = result.fetchone()[0]
    result = db.session.execute("SELECT * FROM pokemons")
    pokemons = result.fetchall()

    if session.get('username') != None:
        sql = "SELECT * FROM users WHERE username=:username"
        result = db.session.execute(sql, {"username":session["username"]})
        user = result.fetchone()
        return render_template("pokemons.html", count=count, pokemons=pokemons, admin=user[3]) 

    return render_template("pokemons.html", count=count, pokemons=pokemons) 

@app.route("/pokemons/<int:id>")
def pokemon(id):
    sql = "SELECT * FROM pokemons WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    pokemon = result.fetchone()
    
    if session.get('username') != None:
        sql = "SELECT * FROM users WHERE username=:username"
        result = db.session.execute(sql, {"username":session["username"]})
        user = result.fetchone()
        return render_template("pokemon.html", pokemon=pokemon, admin=user[3]) 

    return render_template("pokemon.html", pokemon=pokemon)

@app.route("/profile")
def profile():
    if session.get('username') == None:
        return redirect("/")

    sql = "SELECT * FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":session["username"]})
    user = result.fetchone()
    
    sql = "SELECT pokemons.id, pokemons.name FROM userPokemons JOIN pokemons ON pokemons.id = userPokemons.pokemon_id WHERE user_id=:user_id"
    result = db.session.execute(sql, {"user_id":user[0]})
    pokemons = result.fetchall()
    print(pokemons)
    if pokemons != None:
        return render_template("profile.html", pokemons=pokemons, admin=user[3])
        
    return render_template("profile.html", admin=user[3])

@app.route("/profile", methods=["POST"])
def profileadd():
    id = request.form["id"]

    sql = "SELECT id FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":session["username"]})
    user = result.fetchone()    
    print(id)
    print(user[0])
    sql = "INSERT INTO userpokemons (user_id, pokemon_id) VALUES (:user_id,:pokemon_id)"
    db.session.execute(sql, {"user_id":user[0],"pokemon_id":id})
    db.session.commit()
    return redirect("/profile")


@app.route("/add")
def add():
    if session.get('username') == None:
        return redirect("/")

    sql = "SELECT * FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":session["username"]})
    user = result.fetchone()

    if user[3] == False:
        return redirect("/")
    
    return render_template("add.html")

@app.route("/add", methods=["POST"])
def addpokemon():
    if session.get('username') == None:
        return redirect("/")

    sql = "SELECT * FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":session["username"]})
    user = result.fetchone()

    if user[3] == False:
        return redirect("/")
    
    name = request.form["name"]
    tyyppi = request.form["type"]
    kuvaus = request.form["kuvaus"]

    ('Pikachu','Electric','Sähkörotta')
    sql = "INSERT INTO pokemons (name, type, description) VALUES (:name,:type,:kuvaus)"
    db.session.execute(sql, {"name":name,"type":tyyppi,"kuvaus":kuvaus})
    db.session.commit()

    return redirect("/pokemons")
