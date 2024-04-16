#! /usr/bin/python
# -*- coding:utf-8 -*-

from flask import Blueprint
from flask import Flask, request, render_template, redirect, flash, session
from werkzeug.security import generate_password_hash, check_password_hash

from connection_bdd import get_db

player_horaire = Blueprint('player_horaire', __name__,
                           template_folder = 'templates')


@player_horaire.route('/horaire_show')
def player_horaire_show():
    mycursor = get_db().cursor()

    sql_jour ='''SELECT * FROM jour;'''
    mycursor.execute(sql_jour)
    jours = mycursor.fetchall()
    sql_heure = '''SELECT * FROM heure;'''
    mycursor.execute(sql_heure)
    heures = mycursor.fetchall()

    # connecté en tant que
    id_user = session['id_user']
    sql_ps = '''SELECT * FROM utilisateur u 
                join joueurs j on u.idJoueur = j.idJoueur
                where u.idJoueur=%s;'''
    mycursor.execute(sql_ps, (id_user,))
    playersession = mycursor.fetchone()

    return render_template('player/player_horaire.html', playersession = playersession, jours = jours , heures = heures)