SET FOREIGN_KEY_CHECKS = 0;
# MOVIE
insert into movies(movie_id, title, genre, year, language) values (2, "Joker", "Drama", "2019", "English"); # increment

# DIRECTOR RELATION
insert into directorrel(movie_id, director_id) values ((Select movie_id from movies where title = "Joker"), 2); # increment

# DIRECTOR
insert into director(director_id, director_name) values ((select director_id from directorrel where movie_id = (Select movie_id from movies where title = "Joker")), "Todd Phillips");

# ACTOR RELATIONS
insert into actorrel(movie_id, actor_id) values ((Select movie_id from movies where title = "Joker"), 3); # increment
insert into actor(actor_id, actor_name) values (3, "Joaquin Phoenix"); # ---------> same number as above

insert into actorrel(movie_id, actor_id) values ((Select movie_id from movies where title = "Joker"), 4); # increment
insert into actor(actor_id, actor_name) values (4, "Robert De Niro"); # --------> same number as above


# STREAMING PLATFORM
insert into streamingplatform(movie_id, platform) values ((Select movie_id from movies where title = "Joker"), "HBO");

# RATINGS
insert into ratings(movie_id, globalrating) values ((Select movie_id from movies where title = "Joker"), 8.4);
SET FOREIGN_KEY_CHECKS = 1;