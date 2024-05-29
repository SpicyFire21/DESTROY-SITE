#! /usr/bin/python
# -*- coding:utf-8 -*-

from flask import Blueprint
from flask import render_template, session

from connection_bdd import get_db
from controllers.admin_map_agent import pyfetchMap, pyfetchAgent

player_strats = Blueprint('player_strats', __name__,
                          template_folder = 'templates')


@player_strats.route('/strats_show')
def player_strats_show():
    mycursor = get_db().cursor()
    pyfetchMap()
    pyfetchAgent()
    sql_map = '''SELECT * from map;'''
    mycursor.execute(sql_map)
    maps = mycursor.fetchall()


    sql_compo = '''SELECT j.pseudo, m.libelle, a.nomAgent, c.idMap FROM compo c
     JOIN agent a on c.idAgent = a.idAgent
     JOIN map m on c.idMap = m.idMap
     JOIN joueurs j on c.idJoueur = j.idJoueur
    ;'''
    mycursor.execute(sql_compo)
    compo = mycursor.fetchall()
    print("compo", compo)
    print("maps", maps)

    # connecté en tant que
    id_user = session['id_user']
    sql_ps = '''SELECT * FROM utilisateur u 
            join joueurs j on u.idJoueur = j.idJoueur
            where u.idJoueur=%s;'''
    mycursor.execute(sql_ps, (id_user,))
    playersession = mycursor.fetchone()

    return render_template('player/player_strats.html',
                           playersession =playersession,
                           maps = maps,
                           compo = compo)
