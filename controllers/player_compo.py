#! /usr/bin/python
# -*- coding:utf-8 -*-

from flask import Blueprint
from flask import Flask, request, render_template, redirect, flash, session
from werkzeug.security import generate_password_hash, check_password_hash

from connection_bdd import get_db

player_compo = Blueprint('player_compo', __name__,
                           template_folder = 'templates')


@player_compo.route('/compo_show')
def player_compo_show():
    mycursor = get_db().cursor()
    sql_joueurs = '''SELECT * FROM joueurs LIMIT 5  ;'''
    mycursor.execute(sql_joueurs)
    titulaire = mycursor.fetchall()
    sql_map = '''SELECT * FROM map ORDER BY libelle ASC;'''
    mycursor.execute(sql_map)
    maps = mycursor.fetchall()
    get_db().commit()
    return render_template('player/player_compo.html', titulaire=titulaire, maps=maps)