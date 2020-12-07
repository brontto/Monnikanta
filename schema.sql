
DROP TABLE IF EXISTS userPokemons;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS pokemons;

CREATE TABLE pokemons (id SERIAL PRIMARY KEY, name TEXT, type TEXT, description TEXT);

INSERT INTO pokemons (name, type, description) VALUES ('Pikachu','Electric','Sähkörotta');
INSERT INTO pokemons (name, type, description) VALUES ('Bulbasaur','Grass','Kasvipokemon');
INSERT INTO pokemons (name, type, description) VALUES ('Meow','Normal','Kissapokemon');
 
CREATE TABLE users (id SERIAL PRIMARY KEY, username TEXT, password TEXT, admin BOOLEAN);


CREATE TABLE userPokemons (
    user_id INTEGER REFERENCES users,
    pokemon_id INTEGER REFERENCES pokemons
);
