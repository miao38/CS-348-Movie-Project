#SET FOREIGN_KEY_CHECKS = 0;
# MOVIE
insert into movies(title, genre, year, language) values ("Mission: Impossible 7", "Action", "2021", "English"); # increment

# DIRECTOR RELATION
insert ignore into director(director_name) select ("Christopher McQuarrie") where not exists (select * from director where director_name = "Christopher McQuarrie");

insert into directorrel(movie_id, director_id) values ((Select movie_id from movies where title = "Mission: Impossible 7"), (select director_id from director where director_name="Christopher McQuarrie")); # increment

# ACTOR RELATIONS


insert ignore into actor(actor_name) select ("Tom Cruise") where not exists (select * from actor where actor_name = "Tom Cruise"); # ---------> same number as above
insert into actorrel(movie_id, actor_id) values ((Select movie_id from movies where title = "Mission: Impossible 7"), (select actor_id from actor where actor_name = "Tom Cruise" )); # increment


insert ignore into actor(actor_name) select ("Vanessa Kirby") where not exists (select * from actor where actor_name = "Vanessa Kirby"); # --------> same number as above
insert into actorrel(movie_id, actor_id) values ((Select movie_id from movies where title = "Mission: Impossible 7"), (select actor_id from actor where actor_name = "Vanessa Kirby" )); # increment


# STREAMING PLATFORM
insert into streamingplatform(movie_id, platform) values ((Select movie_id from movies where title = "Mission: Impossible 7"), "Hulu");

# RATINGS
insert into ratings(movie_id, globalrating) values ((Select movie_id from movies where title = "Mission: Impossible 7"), null);
#SET FOREIGN_KEY_CHECKS = 1;