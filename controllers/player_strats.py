#! /usr/bin/python
# -*- coding:utf-8 -*-

from flask import Blueprint
from flask import Flask, request, render_template, redirect, flash, session
from werkzeug.security import generate_password_hash, check_password_hash

from connection_bdd import get_db

player_strats = Blueprint('player_strats', __name__,
                          template_folder = 'templates')


@player_strats.route('/strats_show')
def player_strats_show():
    mycursor = get_db().cursor()



    # connecté en tant que
    id_user = session['id_user']
    sql_ps = '''SELECT * FROM utilisateur u 
            join joueurs j on u.idJoueur = j.idJoueur
            where u.idJoueur=%s;'''
    mycursor.execute(sql_ps, (id_user,))
    playersession = mycursor.fetchone()

    return render_template('player/player_strats.html', playersession =playersession)
