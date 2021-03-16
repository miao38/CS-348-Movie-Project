CREATE TABLE users (
    user_id int NOT NULL AUTO_INCREMENT,
    PRIMARY KEY (user_id)
); 

CREATE TABLE IF NOT EXISTS movies (
    movie_id int NOT NULL AUTO_INCREMENT,
    title varchar(255) NOT NULL,
    genre varchar(255),
    year int,
    language varchar(255),
    PRIMARY KEY (movie_id)
);

CREATE TABLE  IF NOT EXISTS watchlist (
    user_id int NOT NULL,
    movie_id int NOT NULL,
    user_rating int,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (movie_id) REFERENCES movies(movie_id)
);

CREATE TABLE  IF NOT EXISTS director (
    director_id int NOT NULL AUTO_INCREMENT,
    director_name varchar(255) NOT NULL,
    PRIMARY KEY (director_id)
);

CREATE TABLE IF NOT EXISTS directorrel (
    movie_id int,
    director_id int,
    FOREIGN KEY (movie_id) REFERENCES movies(movie_id),
    FOREIGN KEY (director_id) REFERENCES director(director_id)
);

CREATE TABLE actor (
    actor_id int NOT NULL AUTO_INCREMENT,
    actor_name varchar(255) NOT NULL,
    PRIMARY KEY (actor_id)
);

CREATE TABLE actorrel (
    movie_id int,
    actor_id int,
    FOREIGN KEY (movie_id) REFERENCES movies(movie_id),
    FOREIGN KEY (actor_id) REFERENCES actor(actor_id)
);

CREATE TABLE ratings (
    movie_id int,
    globalrating int,
    FOREIGN KEY (movie_id) REFERENCES movies(movie_id)
);

CREATE TABLE streamingplatform (
    movie_id int,
    platform varchar(255) NOT NULL,
    FOREIGN KEY (movie_id) REFERENCES movies(movie_id)
);
