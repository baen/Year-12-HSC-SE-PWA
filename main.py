from flask import Flask, render_template, request, redirect, url_for, flash, session
import db
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

app = Flask(__name__)
app.secret_key = "gtg"

@app.route('/')
def index():
    # Use an absolute/relative path that correctly points to your database folder.
    conn = sqlite3.connect('movington.db')
    # Set the row factory to sqlite3.Row to allow dictionary-like access.
    reviews = db.GetAllReviews()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Reviews')
    conn.close()
    return render_template('index.html', Reviews=reviews)

@app.route("/login", methods=["GET", "POST"])
def Login():
    
    if session.get('username') != None:
        return redirect("/")
    # They sent us data, get the username and password
    # then check if their details are correct.
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        # Did they provide good details
        user = db.CheckLogin(username, password)
        if user:
            # Yes! Save their username and id then
            session['id'] = user['id']
            session['username'] = user['username']

            # Send them back to the homepage
            return redirect("/")

    return render_template("login.html")

@app.route("/logout")
def Logout():
    session.clear()
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def Register():
    
    if session.get('username') != None:
        return redirect("/")
    
    # If they click the submit button, let's register
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        # Try and add them to the DB
        if db.RegisterUser(username, password):
            # Success! Let's go to the homepage
            return redirect("/")
        
    return render_template("register.html")

@app.route("/add", methods=["GET","POST"])
def Add():

        # Check if they are logged in first
    if session.get('username') == None:
        return redirect("/")
    posted_time = datetime.now().strftime("%Y-%m-%d")
    # Did they click submit?
    if request.method == "POST":
        movie_title = request.form['movie_title']
        review_text = request.form['review_text']       
        rating = request.form['rating']       
        user_id = session['id']

        # Send the data to add our new guess to the db
        db.AddReview(movie_title, review_text, rating, user_id, posted_time)

    return render_template("add.html")


app.run(debug=True, port=5000)