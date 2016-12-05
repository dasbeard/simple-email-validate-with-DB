from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector
import re
app=Flask(__name__)
mysql=MySQLConnector(app,'friendsdb')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
app.secret_key="SecretKey"

@app.route('/', methods=['GET'])
def index():

    return render_template('index.html')

@app.route('/validate', methods=['POST'])
def validate():
    if len(request.form['email']) < 1:
        flash("Email cannot be blank!")
        return redirect('/')
    elif not EMAIL_REGEX.match(request.form['email']):
        flash('Invalid Email Address!')
        return redirect('/')
    else:
        query = """INSERT INTO email (email, created_at, updated_at)
                    Values (:email, NOW(), NOW())"""
        data = {'email':request.form['email']}
        mysql.query_db(query, data)
        return redirect('/success')

@app.route('/success')
def success():
    query = "SELECT * FROM email"
    emails = mysql.query_db(query)
    return render_template('success.html', all_emails= emails)


app.run(debug=True)
