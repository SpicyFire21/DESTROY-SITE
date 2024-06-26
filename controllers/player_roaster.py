#! /usr/bin/python
# -*- coding:utf-8 -*-

from flask import Blueprint
from flask import Flask, request, render_template, redirect, flash, session
from werkzeug.security import generate_password_hash, check_password_hash

from connection_bdd import get_db
from controllers.player_session import player_session

player_roaster = Blueprint('player_roaster', __name__,
                           template_folder = 'templates')


@player_roaster.route('/roaster_show')
def player_roaster_show():
    mycursor = get_db().cursor()




    sql = '''SELECT * FROM utilisateur u
    join joueurs j on u.idJoueur = j.idJoueur
    join role r on j.idRole = r.idRole;'''
    mycursor.execute(sql)
    players = mycursor.fetchall()
    nbr_joueurs = len(players)
    print('roaster :',players)

    sql = '''SELECT * FROM utilisateur u
        join joueurs j on u.idJoueur = j.idJoueur
        join role r on j.idRole = r.idRole where j.titulaire=1;'''
    mycursor.execute(sql)
    roaster = mycursor.fetchall()
    nbr_titu = len(roaster)
    print('roaster :', roaster)

    # connecté en tant que
    id_user = session['id_user']
    sql_ps = '''SELECT * FROM utilisateur u 
            join joueurs j on u.idJoueur = j.idJoueur
            where u.idJoueur=%s;'''
    mycursor.execute(sql_ps, (id_user,))
    playersession = mycursor.fetchone()

    get_db().commit()
    return render_template('player/player_roaster.html',
                           players = players,
                           roaster = roaster,
                           nbr_titu = nbr_titu,
                           nbr_joueurs = nbr_joueurs,
                           playersession = playersession)


