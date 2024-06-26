#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, abort, flash, session

from connection_bdd import get_db
from controllers.player_session import player_session

player_index = Blueprint('player_index', __name__,
                         template_folder = 'templates')


@player_index.route('/player/index')
def player_show():
    mycursor = get_db().cursor()
    id_user = session['id_user']
    print('id_user', id_user)
    sql = '''SELECT * FROM joueurs WHERE idJoueur = %s;'''
    mycursor.execute(sql, (id_user,))
    player = mycursor.fetchone()
    print(player)

    sql_match = '''SELECT * FROM matchs order by date_match asc LIMIT 10;'''
    mycursor.execute(sql_match)
    matchs = mycursor.fetchall()

    sql_discord = '''SELECT * FROM indexDiscord;'''
    mycursor.execute(sql_discord)
    discord = mycursor.fetchall()

    sql_patch = '''SELECT * FROM indexPatch;'''
    mycursor.execute(sql_patch)
    patch = mycursor.fetchall()

    playersession = player_session()


    if player:
        return render_template('player/index.html', player = player,
                               playersession = playersession,
                               matchs = matchs,
                               discord = discord,
                               patch = patch)
    else:
        flash(u'Vous n\'avez pas les droits pour être inscrit en tant que Joueur ou votre compte n\'existe pas.', 'alert-warning')
        return redirect('/login')
