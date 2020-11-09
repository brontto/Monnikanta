CREATE TABLE pokemons (id SERIAL PRIMARY KEY, name TEXT);
INSERT INTO pokemons (name) VALUES ('Pikachu');
INSERT INTO pokemons (name) VALUES ('Bulbasaur');
INSERT INTO pokemons (name) VALUES ('Meow');

CREATE TABLE users (id SERIAL PRIMARY KEY, username TEXT, password TEXT);
