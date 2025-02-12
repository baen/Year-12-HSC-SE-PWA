import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

def GetDB():

    # Connect to the database and return the connection object
    db = sqlite3.connect("movington.db")
    db.row_factory = sqlite3.Row

    return db

# def GetAllReviews():

#     # Connect, query all guesses and then return the data
#     db = GetDB()
#     reviews = db.execute("""SELECT Reviews.movie_title, Reviews.review_text, Reviews.rating, Reviews.posted_time, Users.username
#                             FROM Reviews JOIN Users IN Reviews.user_id = Users.id
#                             ORDER BY posted_time DESC""").fetchall()
#     ## movie_title, review_text, rating, user_id, posted_time
    
#     db.close()
#     return reviews

def GetAllReviews():
    db = GetDB()
    reviews = db.execute("""SELECT Reviews.movie_title, Reviews.review_text, Reviews.rating,
                                    Reviews.posted_time, Users.username
                             FROM Reviews
                             JOIN Users ON Reviews.user_id = Users.id
                             ORDER BY posted_time DESC""").fetchall()
    db.close()
    return reviews

def CheckLogin(username, password):

    db = GetDB()

    # Ask the database for a single user matching the provided name
    user = db.execute("SELECT * FROM Users WHERE username=? COLLATE NOCASE", (username,)).fetchone()

    # Do they exist?
    if user is not None:
        # OK they exist, is their password correct
        if check_password_hash(user['password'], password):
            # They got it right, return their details 
            return user
        
    # If we get here, the username or password failed.
    return None

def RegisterUser(username, password):

    # Check if they gave us a username and password
    if username is None or password is None:
        return False

    # Attempt to add them to the database
    db = GetDB()
    hash = generate_password_hash(password)
    db.execute("INSERT INTO Users(username, password) VALUES(?, ?)", (username, hash,))
    db.commit()

    return True

def AddReview(movie_title, review_text, rating, user_id, posted_time):
   
    # Check if any boxes were empty
    if movie_title is None or rating is None or review_text is None or user_id is None or posted_time is None:
        return False
    # Get the DB and add the guess
    db = GetDB()
    db.execute("INSERT INTO Reviews(movie_title, review_text, rating, user_id, posted_time) VALUES (?, ?, ?, ?, ?)",
               (movie_title, review_text, rating, user_id, posted_time))
    db.commit()

    return True