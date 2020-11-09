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

    sql = "SELECT username FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()    
    if user != None:
        error = "Käyttäjänimi on jo varattu"
    else:
        hash_value = generate_password_hash(password)
        sql = "INSERT INTO users (username,password) VALUES (:username,:password)"
        db.session.execute(sql, {"username":username,"password":hash_value})
        db.session.commit()

        session["username"] = username
        return redirect("/")

    return render_template("signup.html", error=error)

@app.route("/pokemons")
def pokemons():
    result = db.session.execute("SELECT COUNT(*) FROM pokemons")
    count = result.fetchone()[0]
    result = db.session.execute("SELECT name FROM pokemons")
    pokemons = result.fetchall()
    return render_template("pokemons.html", count=count, pokemons=pokemons) 

@app.route("/pokemons/<int:id>")
def pokemon(id):
    sql = "SELECT name FROM pokemons WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    pokemon = result.fetchone()[0]
    return str(pokemon)
