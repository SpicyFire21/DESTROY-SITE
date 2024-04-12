from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g, app
import pymysql.cursors
import os

from dotenv import load_dotenv
import pymysql.cursors

app = Flask(__name__)
app.secret_key = 'une cle(token) : grain de sel(any random string)'

##################
# Authentification
##################

# Middleware de sécurité

@app.before_request
def before_request():
     if request.path.startswith('/admin') or request.path.startswith('/client'):
        if 'role' not in session:
            return redirect('/login')
        else:
            if (request.path.startswith('/client') and session['role'] != 'ROLE_client') or (request.path.startswith('/admin') and session['role'] != 'ROLE_admin'):
                print('pb de route : ', session['role'], request.path.title(), ' => deconnexion')
                session.pop('login', None)
                session.pop('role', None)
                return redirect('/login')



load_dotenv('./.env')
def get_db():
    if "db" not in g:
        g.db = pymysql.connect(
            host = "localhost",
            user = "root",
            password = "",
            database = "BDD-player",
            charset = "utf8mb4",
            cursorclass = pymysql.cursors.DictCursor,
        )
    return g.db


@app.teardown_appcontext
def teardown_db(exception):
    db = g.pop("db", None)
    if db is not None:
        db.close()