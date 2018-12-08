from flask import Flask, render_template
import MySQLdb


app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/init")
def init():
    try:
       db = MySQLdb.connect("mysql","root","password")
       #get access to database
       cursor = db.cursor()
       cursor.execute("DROP DATABASE IF EXISTS QUOTES")
       cursor.execute("CREATE DATABASE QUOTES")
       cursor.execute("USE QUOTES")
       sql = """CREATE TABLE quotes(Id INT, Author varchar(48),
                     BookTitle varchar(256), Quote varchar(256));"""
       cursor.execute(sql)
       db.commit()
       return "\nDB Initialization done\n\n"
    except (MySQLdb.Error, MySQLdb.Warning) as e:
       return "MySQL Error: %s" % str(e)

@app.route("/quotes/add", methods=['POST'])

def add():
    try:
       db = MySQLdb.connect("mysql","root","password")
       cursor = db.cursor()
       cursor.execute("USE QUOTES")
       req_json = request.get_json()
       cursor.execute("INSERT INTO quotes (Id, Author, BookTitle, Quote) VALUES (%s,%s,%s,%s)",
             (req_json['Uid'], req_json['Author'], req_json['BookTitle'], req_json['Quote']))
       db.commit()
       return Response("Added\n\n", status=200, mimetype='application/json')
    except (MySQLdb.Error, MySQLdb.Warning) as e:
       return "MySQL Error: %s" % str(e)

@app.

if __name__ == "__main__":
    app.run(debug=True)
