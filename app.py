# -*- coding:utf-8 -*-

# == Importations == #
from flask import Flask, request, render_template, redirect, session, g, flash, abort, url_for
import pymysql.cursors

from controllers.admin_index import *
from controllers.fixtures_load import *
from controllers.auth_security import *
from flask import Blueprint
from subprocess import run
import os

from controllers.player_horaire import *
from controllers.player_index import *
from controllers.player_roaster import *
from controllers.player_compo import *
from controllers.player_strats import *




# == Configuration == #
app = Flask(__name__)
app.secret_key = 'une cle(token) : grain de sel(any random string)'


@app.route('/')
def show_accueil():
    return render_template('auth/layout.html')


app.register_blueprint(auth_security)
app.register_blueprint(fixtures_load)

app.register_blueprint(admin_index)


app.register_blueprint(player_index)
app.register_blueprint(player_roaster)
app.register_blueprint(player_horaire)
app.register_blueprint(player_compo)
app.register_blueprint(player_strats)





if __name__ == '__main__':
    app.run(debug = True, port = 5000)

