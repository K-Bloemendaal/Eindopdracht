import sqlite3, os
from flask import g

DATABASE = "database.sqlite3"

# Function to get a database connection
def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db

# Close the database connection when the app context ends
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()

# Initialize the database (create tables if they don't exist)
def init_db():
    db = get_db()
    with open("database.sql", mode="r") as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

# Insert a new submission into the database
def insert_gebruiker(gebruikersnaam, email, wachtwoord):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO gebruikers (Gebruikersnaam, Email, Wachtwoord) VALUES (?, ?, ?)", (gebruikersnaam, email, wachtwoord))
    db.commit()

def login_gebruiker(email):
    return query_db("SELECT Gebruiker_ID, Gebruikersnaam, Email, Wachtwoord FROM gebruikers WHERE Email = ?", (email,), True)

def insert_contact(naam, email, thema, bericht):
    db = get_db()
    cursor = db.cursor()

    activiteit = get_activiteit(thema)
    if activiteit is None:
        return False
    
    cursor.execute("INSERT INTO contact (Naam, Email, Bericht, Activiteit_ID) VALUES (?, ?, ?, ?)", (naam, email, bericht, activiteit[0]))
    db.commit()
    return True

def get_activiteit(thema):
    return query_db("SELECT Activiteit_ID, Thema FROM activiteiten WHERE Thema = ?", (thema,), True)

def get_thema(activiteit_id):
    return query_db("SELECT Activiteit_ID, Thema, Titel FROM activiteiten WHERE Activiteit_ID = ?", (activiteit_id,), True)

def get_favorieten(gebruiker_id):
    return query_db("SELECT Gebruiker_ID, Activiteit_ID FROM favorieten WHERE Gebruiker_ID = ?", (gebruiker_id,))

def insert_favoriet(gebruiker_id, thema):
    db = get_db()
    cursor = db.cursor()

    activiteit = get_activiteit(thema)
    if activiteit is None:
        return False
    
    cursor.execute("INSERT INTO favorieten (Gebruiker_ID, Activiteit_ID) VALUES (?, ?)", (gebruiker_id, activiteit[0]))
    db.commit()
    return True

def delete_favoriet(gebruiker_id, thema):
    db = get_db()
    cursor = db.cursor()

    activiteit = get_activiteit(thema)
    if activiteit is None:
        return False
    
    cursor.execute("DELETE FROM favorieten WHERE Gebruiker_ID = ? AND Activiteit_ID = ?", (gebruiker_id, activiteit[0]))
    db.commit()
    return True

def insert_submission(name, height, pyramid):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO submissions (name, height, pyramid) VALUES (?, ?, ?)", (name, height, pyramid))
    db.commit()

# Retrieve all submissions from the database
def get_submissions():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT name, height, pyramid FROM submissions")
    return cursor.fetchall()