#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, abort, flash, session

from connection_bdd import get_db

player_index = Blueprint('player_index', __name__,
                         template_folder = 'templates')


@player_index.route('/player/index')
def player_show():
    mycursor = get_db().cursor()
    id_user = session['id_user']
    sql = '''SELECT * FROM joueurs WHERE idJoueur = %s;'''
    mycursor.execute(sql, (id_user,))
    joueurs = mycursor.fetchone()
    return render_template('player/index.html',joueurs = joueurs)
