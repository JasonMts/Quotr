from flask import Flask, render_template, json
import MySQLdb
from flask import Response
from flask import request
# from redis import Redis
import hashlib
import os
import redis
import sys



app = Flask(__name__)
R_SERVER = redis.Redis(host=os.environ.get('REDIS_HOST', 'redis'), port=6379)


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

        #this is needed because ajax sends differently than curl
        if request.form:
            cursor.execute("INSERT INTO quotes (Author, BookTitle, Quote) VALUES (%s,%s,%s)",
                 (request.form['Author'], request.form['BookTitle'], request.form['Quote']))
        else:
            data = request.get_json(force=True)
            cursor.execute("INSERT INTO quotes (Author, BookTitle, Quote) VALUES (%s,%s,%s)",
                 (data['Author'], data['BookTitle'], data['Quote']))

        db.commit()
        return Response("Added\n\n", status=200, mimetype='application/json')

    except (MySQLdb.Error, MySQLdb.Warning) as e:
       return "MySQL Error: %s" % str(e)


# @app.route("/quotes/add", methods=['POST'])
# def add():
#     try:
#         db = MySQLdb.connect("db","root","root")
#         cursor = db.cursor()
#         cursor.execute("USE QUOTES")
#         # req_json = request.get_json()
#         data = request.get_json(force=True)
#         cursor.execute("INSERT INTO quotes (Author, BookTitle, Quote) VALUES (%s,%s,%s)",
#              (data['Author'], data['BookTitle'], data['Quote']))
#         db.commit()
#         return Response("Added\n\n", status=200, mimetype='application/json')
#
#     except (MySQLdb.Error, MySQLdb.Warning) as e:
#        return "MySQL Error: %s" % str(e)

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
        if request.form:
            uid = request.form['QuoteSearch']
        else:
            data = request.get_json(force=True)
            uid = data['QuoteSearch']

        hash1 = str(uid).encode('utf-8')
        hash = hashlib.sha256(hash1).hexdigest()
        key = "sql_cache:" + hash

        returnval = ""

        if (R_SERVER.get(key)):
            return json.dumps("\n\nFrom Cache\n" + R_SERVER.get(key).decode('utf-8'))
        else:
            db = MySQLdb.connect("db","root","root")
            cursor = db.cursor()
            cursor.execute("USE QUOTES")
            cursor.execute("select * from quotes WHERE BookTitle=%s", [uid]);
            data = cursor.fetchall()
            if data:
                # return json.dumps(data)
                R_SERVER.set(key, str(data))
                R_SERVER.expire(key, 500)
                return json.dumps(R_SERVER.get(key).decode('utf-8'))
            else:
                return "\n\nRecord not found\n\n"

    except (MySQLdb.Error, MySQLdb.Warning) as e:
        return "MySQL Error: %s" % str(e)


if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)
    # r = requests.post('', data = {'key':'value'})
