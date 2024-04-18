#! /usr/bin/python
# -*- coding:utf-8 -*-

from flask import Blueprint
from flask import Flask, request, render_template, redirect, flash, session
from werkzeug.security import generate_password_hash, check_password_hash

from connection_bdd import get_db

visitor_player = Blueprint('visitor_player', __name__,
                           template_folder = 'templates')


@visitor_player.route('/visitor/player_show')
def visitor_player_show():
    mycursor = get_db().cursor()
    sql = '''SELECT * FROM utilisateur u
    join joueurs j on u.idJoueur = j.idJoueur
    join role r on j.idRole = r.idRole;'''
    mycursor.execute(sql)
    players = mycursor.fetchall()



    # connecté en tant que
    id_user = session['id_user']
    sql_ps = '''SELECT * FROM utilisateur u
            where u.idUtilisateur=%s;'''
    mycursor.execute(sql_ps, (id_user,))
    visitorsession = mycursor.fetchone()

    get_db().commit()
    return render_template('visitor/visitor_player_show.html',
                           players = players,
                           visitorsession = visitorsession)