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

    sql_joueurs = '''SELECT * FROM joueurs LIMIT 5 ;'''
    mycursor.execute(sql_joueurs)
    titulaire = mycursor.fetchall()

    sql_map = '''SELECT * FROM map ORDER BY libelle ASC;'''
    mycursor.execute(sql_map)
    maps = mycursor.fetchall()

    sql_agent = '''SELECT * FROM agent ORDER BY nomAgent ASC;'''
    mycursor.execute(sql_agent)
    agents = mycursor.fetchall()

    # Utilisation des valeurs récupérées dans les requêtes précédentes
    selected_map_id = [item['idMap'] for item in maps]
    selected_joueur_id = [item['idJoueur'] for item in titulaire]
    selected_agent_id = [item['idAgent'] for item in agents]

    # Construction de la requête SQL en utilisant des tuples de valeurs
    sql_compo = '''SELECT j.pseudo,m.libelle,a.nomAgent,j.idJoueur,m.idMap,a.idAgent FROM compo 
                   JOIN agent a ON compo.idAgent = a.idAgent
                   JOIN map m ON compo.idMap = m.idMap
                   JOIN joueurs j ON compo.idJoueur = j.idJoueur
                   WHERE compo.idMap IN %s AND compo.idJoueur IN %s AND compo.idAgent IN %s;'''

    # Exécution de la requête SQL en passant les tuples de valeurs
    mycursor.execute(sql_compo, (tuple(selected_map_id), tuple(selected_joueur_id), tuple(selected_agent_id)))
    compo = mycursor.fetchall()

    print('compo : ', compo)

    get_db().commit()
    return render_template('player/player_compo.html', titulaire=titulaire, maps=maps, agents=agents,
                           compo=compo)





@player_compo.route('/compo_edit', methods = ['POST'])
def player_compo_edit():
    mycursor = get_db().cursor()
    id_player = request.form.get('Joueurs', '')
    id_map = request.form.get('Map', '')
    id_agent = request.form.get('Agent', '')
    sql_select = '''SELECT * FROM compo 
    JOIN agent a ON compo.idAgent = a.idAgent
    JOIN map m ON compo.idMap = m.idMap
    JOIN joueurs j ON compo.idJoueur = j.idJoueur
    WHERE compo.idJoueur=%s AND compo.idMap=%s;'''
    mycursor.execute(sql_select, (id_player, id_map, ))
    pick = mycursor.fetchone()
    print('player : ', id_player)
    print('map : ', id_map)
    print('agent : ', id_agent)
    print(pick)
    if pick:
        print('upd')
        sql_update = '''UPDATE compo SET compo.idAgent = %s WHERE compo.idJoueur=%s AND compo.idMap=%s;'''
        mycursor.execute(sql_update, (id_agent, id_player, id_map,))
        get_db().commit()
    else:
        print('ins')
        sql_insert = '''INSERT INTO compo (idJoueur, idMap, idAgent) VALUES (%s,%s,%s);'''
        mycursor.execute(sql_insert, (id_player, id_map, id_agent,))
        get_db().commit()
    # je dois choisir la ligne choisie par id joueur et map
    # je modifier grace a l'id agent
    return redirect('/compo_show')


@player_compo.route('/delete_column/<id_player>', methods = ['GET'])
def player_compo_delete_column(id_player):
    mycursor = get_db().cursor()
    sql = '''DELETE FROM compo WHERE compo.idJoueur=%s;'''
    mycursor.execute(sql,(id_player,))
    get_db().commit()
    return redirect('/compo_show')

@player_compo.route('/delete_row/<id_map>', methods = ['GET'])
def player_compo_delete_row(id_map):
    mycursor = get_db().cursor()
    sql = '''DELETE FROM compo WHERE compo.idMap=%s;'''
    mycursor.execute(sql, (id_map,))
    get_db().commit()
    return redirect('/compo_show')