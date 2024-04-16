#! /usr/bin/python
# -*- coding:utf-8 -*-

from flask import Blueprint
from flask import Flask, request, render_template, redirect, flash, session
from werkzeug.security import generate_password_hash, check_password_hash

from connection_bdd import get_db

player_roaster = Blueprint('player_roaster', __name__,
                           template_folder = 'templates')


@player_roaster.route('/roaster_show')
def player_roaster_show():
    mycursor = get_db().cursor()
    sql = '''SELECT * FROM utilisateur u
    join joueurs j on u.idJoueur = j.idJoueur
    join role r on j.idRole = r.idRole
    where u.fonction like 'player';'''
    mycursor.execute(sql)
    roaster = mycursor.fetchall()
    nbr_joueurs = len(roaster)
    print('roaster :',roaster)

    # connecté en tant que
    id_user = session['id_user']
    sql_ps = '''SELECT * FROM utilisateur u 
            join joueurs j on u.idJoueur = j.idJoueur
            where u.idJoueur=%s;'''
    mycursor.execute(sql_ps, (id_user,))
    playersession = mycursor.fetchone()

    get_db().commit()
    return render_template('player/player_roaster.html',
                           roaster = roaster,
                           nbr_joueurs = nbr_joueurs,
                           playersession = playersession)


@player_roaster.route('/editaccount_player', methods =['GET'])
def editaccount():
    mycursor = get_db().cursor()
    id_user = session['id_user']
    sql_all = '''SELECT * FROM utilisateur u
    JOIN joueurs j ON u.idJoueur = j.idJoueur
    WHERE u.idUtilisateur =%s;'''
    mycursor.execute(sql_all,(id_user,))
    compte = mycursor.fetchone()
    print(compte)

    # connecté en tant que
    id_user = session['id_user']
    sql_ps = '''SELECT * FROM utilisateur u 
                join joueurs j on u.idJoueur = j.idJoueur
                where u.idJoueur=%s;'''
    mycursor.execute(sql_ps, (id_user,))
    playersession = mycursor.fetchone()

    get_db().commit()
    return render_template('player/player_profile.html', compte = compte, playersession = playersession )

@player_roaster.route('/editaccount_player', methods =['POST'])
def valid_editaccount():
    mycursor = get_db().cursor()
    id = request.form.get('id')
    pseudo = request.form.get('pseudo', '')
    email = request.form.get('email', '')
    mdp = request.form.get('mdp', '')
    mdp = generate_password_hash(mdp, method = 'pbkdf2:sha256')
    sql ='''UPDATE utilisateur u
    JOIN joueurs j ON u.idJoueur = j.idJoueur
    set pseudo=%s,email=%s,mdp=%s WHERE u.idJoueur=%s'''
    mycursor.execute(sql, (pseudo,email,mdp,id,))
    get_db().commit()
    return redirect('/player/index')
