from flask import Flask, render_template, request

from flaskext.mysql import MySQL

app = Flask(__name__)

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'BoilerMakers'
app.config['MYSQL_DATABASE_DB'] = 'cs348projectdb'
app.config['MYSQL_DATABASE_HOST'] = '34.121.109.50'
mysql.init_app(app)

conn = mysql.connect()

cursor = conn.cursor()

@app.route("/")
def main():
  return render_template('index.html')

@app.route("/signup")
def sigin():
  return render_template('signup.html')

@app.route("/search_test", methods=["GET", "POST"])
def search_test():
  cursor.execute("SELECT DISTINCT genre FROM movies;")
  genrelist = cursor.fetchall()
  cursor.execute("SELECT DISTINCT language FROM movies;")
  languagelist = cursor.fetchall()
  ratinglist = [1,2,3,4,5,6,7,8,9]
  return render_template("search.html", genrelist = genrelist, languagelist = languagelist, ratinglist = ratinglist)

@app.route("/handle_search_data", methods=["POST"])
def handle_search_data():
  category = None
  inputText = None
  genre = None
  rating = None
  language = None
  

  category = request.form.get("category")
  inputText = request.form.get("inputText")
  genre = request.form.get("genre")
  rating = request.form.get("rating")
  language = request.form.get("language")

  print("Category: " + category)
  print("Input: " + inputText)
  print("Genre: " + genre)
  print("Rating: " + rating)
  print("Language: " + language)
  
  return display_search(category, inputText, genre, rating, language)


def display_search(category, inputText, genre, rating, language):  
  
  likePattern = "%"+inputText+"%"

  if category == "Movie" or category == "%":
    cursor.execute("SELECT movies.movie_id, title, genre, language, globalrating from movies JOIN ratings on movies.movie_id = ratings.movie_id WHERE title like %s AND genre like %s AND language like %s AND globalrating >= %s;", (likePattern, genre, language, rating))
  elif category == "Director":
    cursor.execute("SELECT movies.movie_id, title, genre, language, globalrating from movies JOIN ratings on movies.movie_id = ratings.movie_id JOIN directorrel on movies.movie_id=directorrel.movie_id JOIN director on directorrel.director_id = director.director_id WHERE director_name like %s AND genre like %s AND language like %s AND globalrating >= %s;", (likePattern, genre, language, rating))
  elif category == "Actor":
    cursor.execute("SELECT movies.movie_id, title, genre, language, globalrating from movies JOIN ratings on movies.movie_id = ratings.movie_id JOIN actorrel on movies.movie_id=actorrel.movie_id JOIN actor on actorrel.actor_id=actor.actor_id WHERE actor_name like %s AND genre like %s AND language like %s AND globalrating >= %s;", (likePattern, genre, language, rating))
  else:
    print("ERROR ! ERROR ! Category")
  
  print(type(cursor))
  table = "<html> <table border = '1'>"
  table = table + "<tr>\n"
  table = table + "<td>Movie ID</td><td>Title</td><td>Genre</td><td>Language</td><td>Rating</td>\n"
  table = table + "</tr>\n"
  movie_id = 1
  for (movie_id, title, genre, language, rating) in cursor:
    table = table + "<tr>\n"
    table = table + "<td>" + str(movie_id) + "</td><td>" + title + "</td><td>" + genre + "</td><td>" + language + "</td><td>" + str(rating) + "</td><td>\n"
    table = table + "</tr>\n"
    movie_id += 1

  table = table + "</table><a href=\"/search_test\">GO BACK</a></html>" 
  
  return table

@app.route("/handle_watchlist_data", methods=["POST"])
def handle_watchlist_data():
  watchlistName = None
  

  watchlistName = request.form.get("watchlistName")

  print(watchlistName)
  
  return "".join(["<HTML>Added movie ", watchlistName, " to watchlist!!</HTML>"])

if __name__ == "__main__":
  app.run(debug=True)