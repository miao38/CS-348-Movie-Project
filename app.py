from flask import Flask, render_template, request

from flaskext.mysql import MySQL

app = Flask(__name__)

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'BoilerMakers'
app.config['MYSQL_DATABASE_DB'] = 'cs348projectdb'
app.config['MYSQL_DATABASE_HOST'] = '34.67.4.58'
mysql.init_app(app)

conn = mysql.connect()

cursor = conn.cursor()

@app.route("/")
def main():
  return render_template('index.html')

@app.route("/signup")
def sigin():
  return render_template('signup.html')

@app.route("/search")
def search():
  cursor.execute('SELECT * from movies;')
  
  table = "<html> <table border = '1'>"
  
  for (name) in cursor:
    table = table + "<tr>\n"
    table = table + "<td>Movie Name</td><td>" + ''.join(name) + "</td>"

  table = table + "</table> </html>"
  return table

if __name__ == "__main__":
  app.run()