import cmath
import calendar 
import base64
import bisect 
import random 
import math
import atexit
import statistics
import re
import sys
import os
import time
import tracemalloc
import datetime
from functools import wraps

from flask import Flask, render_template, request, redirect, url_for, session, make_response, jsonify
from flask_mysqldb import MySQL
import MySQLdb.connections
import MySQLdb
from pymongo import MongoClient
from bson.objectid import ObjectId
import redis
import psycopg2
import psutil
import requests

from helper_functions import help_me
from custom_loggers import messaging_logger
from custom_loggers import payments_logger


# ------ CONFIGURATION ------

# Initialisation
app = Flask(__name__,
            static_url_path='',
            static_folder='static',
            template_folder='templates')
print(app.wsgi_app)

print("flask app :app")
title = "TODO sample application with Flask and Mysql"
heading = "TODO Reminder with Flask and Mysql"
print("heading and title ")
app.secret_key = '123@gari'



# My_Sql configuration
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'cavisson'
app.config['MYSQL_PASSWORD'] = 'cavisson'
app.config['MYSQL_DB'] = 'my_first_db'
mysql = MySQL(app)

# MongoDB configuration
client = MongoClient("mongodb://127.0.0.1:27017")  # host uri
mongo_db = client.admin  # Select the database
todos = mongo_db.testcoll  # Select the collection name

# PostgreSQL configuration
conn = psycopg2.connect(
    database="cavisson",
    user="postgres",
    password="cavisson",
    host="localhost",
    port="5432"
)

r = redis.Redis(host='localhost', port=6379, db=0)


# ------ ROUTES ------

# Index code start
@app.route('/')
@app.route('/login/id=1045', methods=['GET', 'POST'])
def login():
    # print("inside login")
    # print("Login start")
    # print("*************************************************************")
    # r = requests.get("https://www.google.com/")
    # print("*************************************************************")
    # print("Login End")
    # x = requests.get("http://172.24.1.48:5443/")
    # x = requests.get("http://172.24.1.48:5443/display")
    # r = requests.get("http://127.0.0.1:5000/")
    # x = requests.get("http://10.10.40.24:8080/tiny")
    # print(r.status_code)
    # print("\n\n\n\n", r.text, "\n\n\n")
    # messaging_logger.warning("this is a messaging log")
    # payments_logger.warning("this is payments log")
    # import requests
    # r = requests.get("https://www.google.com/search?q=a")
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        print("inside if")
        username = request.form['username']
        password = request.form['password']
        print("mysql", type(mysql))
        print("mysql.connection", type(mysql.connection))
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM accounts WHERE username = % s AND password = % s', (username, password, ))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            msg = 'Logged in successfully !'
            return render_template('index.html', msg=msg)
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg=msg)


@app.route("/index")
def index():
    if 'loggedin' in session:
        return render_template("index.html")
    return redirect(url_for('login'))
# Index code End




# Register Code start
@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form and 'address' in request.form and 'city' in request.form and 'country' in request.form and 'postalcode' in request.form and 'organisation' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        organisation = request.form['organisation']
        address = request.form['address']
        city = request.form['city']
        state = request.form['state']
        country = request.form['country']
        postalcode = request.form['postalcode']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM accounts WHERE username = % s', (username, ))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'name must contain only characters and numbers !'
        else:
            cursor.execute('INSERT INTO accounts VALUES (NULL, % s, % s, % s, % s, % s, % s, % s, % s, % s)',
                           (username, password, email, organisation, address, city, state, country, postalcode, ))
            mysql.connection.commit()
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg=msg)
#Register Code End




#Display Code Start
@app.route("/display")
def display():
    help_me()
    print(sys.version)
    storeurlsforcall()
    storedemographics()
    getmediamodes("name")
    gethhtpstatus()
    getuserdetails()
    hitcount()
    fetch()
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        # cursor.execute('SELECT * FROM products')
        cursor.execute('SELECT * FROM accounts ORDER BY id DESC')
        cursor.execute("SELECT VERSION()")
        cursor.execute("SELECT * FROM accounts LIMIT 5")
        cursor.execute('SELECT * FROM accounts WHERE id = % s',
                       (session['id'], ))
        account = cursor.fetchone()
        return render_template("display.html", account=account)
        # gethhtpstatus()
    return redirect(url_for('login'))
#Display Code End




#Update Code Start
@app.route("/update", methods=['GET', 'POST'])
def update():
    msg = ''
    if 'loggedin' in session:
        if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form and 'address' in request.form and 'city' in request.form and 'country' in request.form and 'postalcode' in request.form and 'organisation' in request.form:
            username = request.form['username']
            password = request.form['password']
            email = request.form['email']
            organisation = request.form['organisation']
            address = request.form['address']
            city = request.form['city']
            state = request.form['state']
            country = request.form['country']
            postalcode = request.form['postalcode']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(
                'SELECT * FROM accounts WHERE username = % s', (username, ))
            account = cursor.fetchone()
            if account:
                msg = 'Account already exists !'
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                msg = 'Invalid email address !'
            elif not re.match(r'[A-Za-z0-9]+', username):
                msg = 'name must contain only characters and numbers !'
            else:
                cursor.execute('UPDATE accounts SET username =% s, password =% s, email =% s, organisation =% s, address =% s, city =% s, state =% s, country =% s, postalcode =% s WHERE id =% s', (
                    username, password, email, organisation, address, city, state, country, postalcode, (session['id'], ), ))
                mysql.connection.commit()
                msg = 'You have successfully updated !'
        elif request.method == 'POST':
            msg = 'Please fill out the form !'
        return render_template("update.html", msg=msg)
    return redirect(url_for('login'))
#Update Code End





#MongoDB code Start
@app.route("/mongodb")
def mongodb():
    if 'loggedin' in session:
        # mongodb_call(todos)
        users = todos.find()
        # return render_template("mongodb.html",)
        return render_template('demo.html', users=users)


@app.route('/edit/<string:user_id>', methods=['GET', 'POST'])
def edit(user_id):
    user = todos.find_one({'_id': ObjectId(user_id)})

    if request.method == 'POST':
        updated_user = {
            'name': request.form['name'],
            'email': request.form['email']
        }
        todos.update_one({'_id': ObjectId(user_id)}, {'$set': updated_user})
        return redirect('/mongodb')

    return render_template('edit.html', user=user)


@app.route('/delete/<string:user_id>')
def delete(user_id):
    todos.delete_one({'_id': ObjectId(user_id)})
    return redirect('/mongodb')


@app.route('/add_user', methods=['POST'])
def add_user():
    new_user = {
        'name': request.form['name'],
        'email': request.form['email']
    }
    todos.insert_one(new_user)
    return redirect('/mongodb')
#MongoDB code End




#Redis Code Start
@app.route("/redis_page")
def redis_page():
    if 'loggedin' in session:
        keys = r.keys('*')
        return render_template("redis.html")
@app.route("/redis_create", methods=["POST"])
def redis_create():
    if request.method == "POST":
        key = request.form["key"]
        value = request.form["value"]
        create_data(key, value)
        return redirect(url_for("redis_page"))


@app.route("/redis_read", methods=["GET"])
def redis_read():
    key = request.args.get("key")
    print("Reading key:", key)
    value = r.get(key)
    if value is not None:
        value = value.decode()
    print("Value:", value)
    return render_template("redis.html", value=value)


@app.route("/redis_update", methods=["POST"])
def redis_update():
    if request.method == "POST":
        key = request.form["key"]
        new_value = request.form["new_value"]
        update_data(key, new_value)
        return redirect(url_for("redis_page"))


@app.route("/redis_delete", methods=['POST'])
def redis_delete():
    key = request.form["key"]
    delete_data(key)
    return redirect(url_for("redis_page"))
#Redis code End




#Multiple_SQL Code Start
@app.route('/multiple_sql')
def multiple_sql():
    # Display account information from the 'accounts' table
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM userdetails")
    accounts = cursor.fetchall()
    cursor.close()
    return render_template('multiple_sql.html', accounts=accounts)

@app.route('/add_userdetails', methods=['POST'])
def add_userdetails():
    if request.method == 'POST':
        id = request.form['id']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        

        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO userdetails (id,firstname,lastname) VALUES (%s, %s, %s)", (id,firstname,lastname))
        mysql.connection.commit()
        cursor.close()

        return redirect(url_for('multiple_sql'))
#Multiple_SQL Code End




#PostgreSQL code Start
@app.route('/postgre_sql')
def postgre_sql():
    cursor = conn.cursor()
    cursor.execute("SELECT id, task, completed FROM todos")
    tasks = cursor.fetchall()
    cursor.close()
    return render_template('postgresql.html', tasks=tasks)


@app.route('/add_post', methods=['POST'])
def add_task():
    task = request.form['task']
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO todos (task, completed) VALUES (%s, %s)", (task, False))
    conn.commit()
    cursor.close()
    return redirect(url_for('postgre_sql'))


@app.route('/update_post/<int:id>', methods=['POST'])
def update_task(id):
    storeurlsforcall()
    completed = request.form.get('completed')
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE todos SET completed = %s WHERE id = %s", (completed, id))
    conn.commit()
    cursor.close()
    return redirect(url_for('postgre_sql'))


@app.route('/delete_post/<int:id>')
def delete_task(id):
    storeurlsforcall()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM todos WHERE id = %s", (id,))
    conn.commit()
    cursor.close()
    return redirect(url_for('postgre_sql'))
#Postgre SQL code End




#HTTP code Start
@app.route('/http_page')
def http_page():
    print("\n\nhttp page\n\n")
    r = requests.get("https://www.bing.com/search?q=a")
    return render_template("http_page.html")

# @app.route('/http_post', methods=['POST'])
# def post_example():
#     return "POST request example."

# @app.route('/http_put', methods=['PUT'])
# def put_example():
#     return "PUT request example."

# @app.route('/http_delete', methods=['DELETE'])
# def delete_example():
#     return "DELETE request example."
#HTTP code End




#Exception code start
@app.route("/exception")
def exception():
    if 'loggedin' in session:
        # hitcount()
        a = 1//0
        return render_template("exception.html")   
#Exception code End


# Logout Code start
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))
# Logout Code start

# ------ FUNCTIONS ------ 

def redis_call():
    #r = redis.Redis(host='localhost', port=6379, db=0)
    r.set('redis', 'call')
    value = r.get('redis')
    print("value of redis is ->", value.decode()) 


def create_data(key, value):
    r.set(key, value)


def read_data(key):
    return r.get(key)


def update_data(key, new_value):
    r.set(key, new_value)


def delete_data(key):
    r.delete(key)


def storedemographics():
    # time.sleep()
    print("in dummy function$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    return ("Hey hi ,It is a dummy function ")


def getmediamodes(name):
    print("name-------------->", name)
    return "dummy"
    # run()


def hitcount():
    print(" *******Hi everyone good wishes to all of you,enjoy the day********** ")
    # a=1//0
    # r = requests.get("jsbcdhkjrnmdenjbdnrncjb")

    return "Hi everyone good wishes to all of you,enjoy the day"


def getuserdetails():
    data1 = [1, 3, 4, 5, 7, 9, 2]
    x = statistics.mean(data1)
    statistics.median(data1)
    statistics.stdev(data1)
    atexit.register(goodbye, 'Donny', 'nice')
    print('in dummy 2****************************************************************')
    return "This is the testing method please check it correctly "


def goodbye(name, adjective):
    print('Goodbye %s, it was %s to meet you.' % (name, adjective))


def storeurlsforcall():
    print('*******************************dummy**************************')
    time.sleep(0.001)
    cmath.isnan(2 + 3j)
    base64.b64encode(b'data to be encoded')
    calendar.setfirstweekday(calendar.SUNDAY)
    # d = datetime.timedelta(microseconds=-1)
    return "This is the testing method please check it correctly "


def gethhtpstatus():
    #r = requests.get("http://127.0.0.1:5010/")
    # r = requests.get("https://www.google.com/search?q=a")
    # print(r.status_code)
    pass


def fetch():
    mylist = ["apple", "banana", "cherry"]
    random.shuffle(mylist)
    math.floor(0.6)
    data = [('red', 5), ('blue', 1), ('yellow', 8), ('black', 0)]
    data.sort(key=lambda r: r[1])
    keys = [r[1] for r in data]
    aaaa = data[bisect.bisect_left(keys, 0)]
    bbbb = data[bisect.bisect_right(keys, 0)]
    cccc = data[bisect.bisect_right(keys, 0)]
    print('dummy')


def run():
    app.run(host="0.0.0.0", port=5000)
    # app.run(ssl_context='adhoc', host="0.0.0.0", port=5001)  # For HTTPS
    # app.run()


# STAND ALONE

if __name__ == "__main__":
    run()
