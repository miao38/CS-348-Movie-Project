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

@app.route("/search_test")
def search_test():
  cursor.execute("SELECT DISTINCT genre FROM movies;")
  genrelist = cursor.fetchall()
  cursor.execute("SELECT DISTINCT language FROM movies;")
  languagelist = cursor.fetchall()
  ratinglist = [1,2,3,4,5]
  return render_template("search.html", genrelist = genrelist, languagelist = languagelist, ratinglist = ratinglist)

@app.route("/search")
def search():
  cursor.execute('SELECT * from movies;')
  
  print(type(cursor))
  table = "<html> <table border = '1'>"
  table = table + "<tr>\n"
  table = table + "<td>Movie ID</td><td>Title</td><td>Genre</td><td>Year</td><td>Language</td>\n"
  table = table + "</tr>\n"
  movie_id = 1
  for (movie_id, title, genre, year, language) in cursor:
    table = table + "<tr>\n"
    table = table + "<td>" + str(movie_id) + "</td><td>" + title + "</td><td>" + genre + "</td><td>" + str(year) + "</td><td>" + language + "</td><td>\n"
    table = table + "</tr>\n"
    movie_id += 1

  table = table + "</table> </html>"
  return table

if __name__ == "__main__":
  app.run(debug=True)