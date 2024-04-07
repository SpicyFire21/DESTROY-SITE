# -*- coding:utf-8 -*-

# == Importations == #
from flask import Flask, request, render_template, redirect, session, g, flash, abort, url_for
import pymysql.cursors

from controllers.admin_index import admin_index
from controllers.fixtures_load import *
from controllers.auth_security import *
from flask import Blueprint
from subprocess import run
import os

from controllers.player_index import player_index

# == Configuration == #
app = Flask(__name__)
app.secret_key = 'une cle(token) : grain de sel(any random string)'


@app.route('/')
def show_accueil():
    return render_template('auth/layout.html')


app.register_blueprint(auth_security)
app.register_blueprint(fixtures_load)

app.register_blueprint(player_index)
app.register_blueprint(admin_index)







if __name__ == '__main__':
    app.run(debug = True, port = 5000)

