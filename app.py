# -*- coding:utf-8 -*-

# == Importations == #
from flask import Flask, request, render_template, redirect, session, g, flash, abort, url_for
import pymysql.cursors

from controllers.edit_account import *
from controllers.testimagebdd import *
from controllers.admin_edit_index import *
from controllers.admin_map_agent import *
from controllers.admin_match_pracc import *
from controllers.admin_player import *
from controllers.admin_root import *
from controllers.admin_user import *
from controllers.nologin_index import *
from controllers.visitor_index import *
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
from controllers.visitor_match import *
from controllers.visitor_player import *
# from controllers.visitor_prac import *

# == Configuration == #
app = Flask(__name__)
app.secret_key = 'une cle(token) : grain de sel(any random string)'


@app.route('/')
def show_accueil():
    return render_template('nologin/nologin_index.html')


app.register_blueprint(auth_security)
app.register_blueprint(fixtures_load)

app.register_blueprint(admin_index)
app.register_blueprint(admin_user)
app.register_blueprint(admin_player)
app.register_blueprint(admin_map_agent)
app.register_blueprint(admin_match_pracc)
app.register_blueprint(admin_root)
app.register_blueprint(admin_edit_index)

app.register_blueprint(player_index)
app.register_blueprint(player_roaster)
app.register_blueprint(player_horaire)
app.register_blueprint(player_compo)
app.register_blueprint(player_strats)

app.register_blueprint(visitor_index)
app.register_blueprint(visitor_player)
app.register_blueprint(visitor_match)

app.register_blueprint(nologin_index)

app.register_blueprint(edit_account)

app.register_blueprint(testimagebdd)



if __name__ == '__main__':
    app.run(debug = True, port = 5000)

