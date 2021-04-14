from flask import Flask, render_template, request
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
from flaskext.mysql import MySQL

app = Flask(__name__)

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'BoilerMakers'
app.config['MYSQL_DATABASE_DB'] = 'cs348projectdb'
app.config['MYSQL_DATABASE_HOST'] = '34.121.109.50'
mysql.init_app(app)

# CONNECTION VARIABLES
conn = mysql.connect()
conn.autocommit = False
cursor = conn.cursor()
engine = sqlalchemy.create_engine(
    'mysql+mysqlconnector://root:BoilerMakers@34.121.109.50/cs348projectdb',
    echo=True)
Base = declarative_base()
class User(Base):
  __tablename__ = 'users'
  user_id = Column(String, primary_key = True)

  def __repr__(self):
    return "<User(id='%s')>" % (self.user_id)


# USER VARIABLES
gUserID = ""

# FUNCTIONS
@app.route("/")
def main():
  return render_template('index.html')

@app.route("/signup")
def sigin():
  return render_template('signup.html')

def orm_test(user_id):
  Base.metadata.create_all(engine)
  Session = sessionmaker(bind=engine)
  session = Session()
  new_user = User(user_id=user_id)
  session.add(new_user)
  session.commit()


@app.route("/handle_login", methods=["GET", "POST"])
def handle_login():
  global gUserID
  gUserID = request.form.get("inputUserID")
  print("login, " + gUserID)
  
  cursor.execute("SELECT user_id from users where user_id like %s;", (gUserID))
  res = cursor.fetchone()
  
  if not res:
    print("User does not exist. Create ID")
    #cursor.execute("INSERT INTO users(user_id) values (%s)", (gUserID))
    orm_test(gUserID)
    conn.commit()
  else:
    print("User already exists. Just log in")

  print("Login complete: UserID: " + gUserID)
  return render_template('index.html')


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

@app.route("/display_watchlist_table", methods=["GET"])
def display_watchlist_table():  
  cursor.execute("SELECT watchlist.movie_id, movies.title, movies.genre, movies.year, movies.language, mov_dir.director_name, mov_act.actor_name, sp.platform, user_rating FROM watchlist JOIN movies ON watchlist.movie_id = movies.movie_id JOIN (SELECT movie_id, director_name FROM directorrel JOIN director on directorrel.director_id = director.director_id) mov_dir ON watchlist.movie_id = mov_dir.movie_id JOIN (SELECT movie_id, actor_name FROM actorrel JOIN actor on actorrel.actor_id = actor.actor_id) mov_act ON watchlist.movie_id = mov_act.movie_id JOIN streamingplatform sp ON watchlist.movie_id = sp.movie_id WHERE watchlist.user_id = %s;", gUserID)

  table = "<html> <table border = '1'>"
  table = table + "<tr>\n"
  table = table + "<td>Movie ID</td><td>Title</td><td>Genre</td><td>Year</td><td>Language</td><td>Dirctor</td><td>Actors</td><td>Platform</td><td>Your Rating</td>\n"
  table = table + "</tr>\n"
  prev_movie = -1
  prev_title = ''
  prev_genre = ''
  prev_year = 0
  prev_lang = ''
  prev_dir = ''
  prev_plat = ''
  prev_rating = 0
  actor_list = []

  for (movie_id, title, genre, year, language, director_name, actor_name, platform, user_rating) in cursor:
    if prev_movie == movie_id:
      actor_list.append(actor_name)
    elif prev_movie == -1:
      prev_movie = movie_id
      prev_title = title
      prev_genre = genre
      prev_year = year
      prev_lang = language
      prev_dir = director_name
      prev_plat = platform
      prev_rating = user_rating
      actor_list = []
      actor_list.append(actor_name)
    else:
      table = table + "<tr>\n"
      actor_string = str(actor_list).replace("', '",",<br/>").strip("['").strip("']")
      table = table + "<td>" + str(prev_movie) + "</td><td>" + prev_title + "</td><td>" + prev_genre + "</td><td>" + str(prev_year) + "</td><td>" + prev_lang + "</td><td>" + prev_dir +  "</td><td>" + actor_string + "</td><td>" + prev_plat + "</td><td>" + str(prev_rating) + "\n"
      table = table + "</tr>\n"
      prev_movie = movie_id
      prev_title = title
      prev_genre = genre
      prev_year = year
      prev_lang = language
      prev_dir = director_name
      prev_plat = platform
      prev_rating = user_rating
      actor_list = []
      actor_list.append(actor_name)
  
  if prev_movie == -1:
    table = table + "<td colspan= 9>" + "Uh oh!...You do not currently have any movies in your Watch List :(" + "<br/>" + "Start building your Watch List by adding movies from the Search page"
  else:
    table = table + "<tr>\n"
    actor_string = str(actor_list).replace("', '",",<br/>").strip("['").strip("']")
    table = table + "<td>" + str(prev_movie) + "</td><td>" + prev_title + "</td><td>" + prev_genre + "</td><td>" + str(prev_year) + "</td><td>" + prev_lang + "</td><td>" + prev_dir +  "</td><td>" + actor_string + "</td><td>" + prev_plat + "</td><td>" + str(prev_rating) + "\n"
    table = table + "</tr>\n"
    table = table + "</table><a href=\"/display_watchlist\"></a></html>" 
    
  return table

@app.route("/display_watchlist", methods=["GET", "POST"])
def display_watchlist():
  return render_template("watchlist.html", watchlist = display_watchlist_table())

@app.route("/handle_watch_data", methods=["POST"])
def handle_watch_data():
  movie_id = None
  rating = None
  movie_id = request.form["movieId"]

  if request.form.get("btnDelete") == "btnDelete":
    cursor.execute("DELETE FROM watchlist WHERE user_id = %s and movie_id = %s;", (gUserID, movie_id))
    conn.commit()
  elif request.form.get("btnRate") == "btnRate":
    rating = request.form["rating"]
    if rating == '':
      rating = None
    cursor.execute("UPDATE watchlist SET user_rating = %s WHERE user_id = %s and movie_id = %s;", (rating, gUserID, movie_id))
    conn.commit()
  
  return display_watchlist()

if __name__ == "__main__":
  app.run(debug=True)