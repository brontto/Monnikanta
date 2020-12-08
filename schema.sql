
DROP TABLE IF EXISTS userPokemons;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS pokemons;

CREATE TABLE pokemons (id SERIAL PRIMARY KEY, nimi TEXT, tyyppi TEXT, kuvaus TEXT);

INSERT INTO pokemons (nimi, tyyppi, kuvaus) VALUES ('Pikachu','Sähkö','Sähkörotta mallia vikkelä');
INSERT INTO pokemons (nimi, tyyppi, kuvaus) VALUES ('Bulbasaur','Ruoho','Kasvipokemon ruoskii ku orjapiiskuri');
INSERT INTO pokemons (nimi, tyyppi, kuvaus) VALUES ('Meow','Normaali','Kissapokemon sanoo miaaaaau');
 
CREATE TABLE users (id SERIAL PRIMARY KEY, username TEXT, password TEXT, admin BOOLEAN);


CREATE TABLE userPokemons (
    user_id INTEGER REFERENCES users,
    pokemon_id INTEGER REFERENCES pokemons
);
