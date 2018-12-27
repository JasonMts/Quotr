from flask import Flask, render_template, json
import MySQLdb
from flask import Response
from flask import request


app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route('/init')
def init():
    try:
       db = MySQLdb.connect("db", "root", "root")
       cursor = db.cursor()
       cursor.execute("DROP DATABASE IF EXISTS QUOTES")
       cursor.execute("CREATE DATABASE QUOTES")
       cursor.execute("USE QUOTES")
       sql = """CREATE TABLE quotes(Id INT AUTO_INCREMENT, Author varchar(48),
                     BookTitle varchar(256), Quote varchar(256), PRIMARY KEY (Id));"""
       cursor.execute(sql)
       db.commit()
       return "\nDB Initialization done\n\n"
    except (MySQLdb.Error, MySQLdb.Warning) as e:
       return "MySQL Error: %s" % str(e)

@app.route("/quotes/add", methods=['POST'])
def add():
    try:
       db = MySQLdb.connect("db","root","root")
       cursor = db.cursor()
       cursor.execute("USE QUOTES")
       # req_json = request.get_json()
       cursor.execute("INSERT INTO quotes (Author, BookTitle, Quote) VALUES (%s,%s,%s)",
             (request.form['Author'], request.form['BookTitle'], request.form['Quote']))
       db.commit()
       return Response("Added\n\n", status=200, mimetype='application/json')

    except (MySQLdb.Error, MySQLdb.Warning) as e:
       return "MySQL Error: %s" % str(e)

# @app.route("/quotes/<Uid>")
# def getquotes():
#     try:
#         db = MySQLdb.connect("db","root","root")
#         cursor = db.cursor()
#         cursor.execute("USE QUOTES")
#         cursor.execute("select Author, BookTitle, Quote from courses where ID=" + str(uid))
#         data = cursor.fetchall()
#         if data:
#             return json.dumps(data)
#         else:
#             return "\n\nRecord not found\n\n"
#
#     except (MySQLdb.Error, MySQLdb.Warning) as e:
#         return "MySQL Error: %s" % str(e)

@app.route("/quotes/getall", methods=['POST'])
def getquotesall():
    try:
        db = MySQLdb.connect("db","root","root")
        cursor = db.cursor()
        cursor.execute("USE QUOTES")
        cursor.execute("select * from quotes WHERE BookTitle=%s", [request.form['QuoteSearch']]);
        data = cursor.fetchall()
        if data:
            return json.dumps(data)
        else:
            return "\n\nRecord not found\n\n"

    except (MySQLdb.Error, MySQLdb.Warning) as e:
        return "MySQL Error: %s" % str(e)


if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)
    # r = requests.post('', data = {'key':'value'})
