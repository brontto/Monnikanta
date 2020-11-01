from flask import Flask
from flask import redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from os import getenv

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

@app.route("/")
def index():
    result = db.session.execute("SELECT COUNT(*) FROM pokemons")
    count = result.fetchone()[0]
    result = db.session.execute("SELECT name FROM pokemons")
    pokemons = result.fetchall()
    return render_template("index.html", count=count, pokemons=pokemons) 

