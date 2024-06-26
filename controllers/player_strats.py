#! /usr/bin/python
# -*- coding:utf-8 -*-

from flask import Blueprint
from flask import render_template, session, redirect, request

from connection_bdd import get_db
from controllers.admin_map_agent import pyfetchMap, pyfetchAgent
from controllers.player_session import player_session

player_strats = Blueprint('player_strats', __name__,
                          template_folder = 'templates')


@player_strats.route('/strats_show')
def player_strats_show():
    mycursor = get_db().cursor()
    pyfetchMap()
    pyfetchAgent()
    sql_map = '''SELECT * from map order by libelle;'''
    mycursor.execute(sql_map)
    maps = mycursor.fetchall()
    sql_compo = '''SELECT j.pseudo, m.libelle, a.nomAgent,a.imgAgent, c.idMap FROM compo c
     JOIN agent a on c.idAgent = a.idAgent
     JOIN map m on c.idMap = m.idMap
     JOIN joueurs j on c.idJoueur = j.idJoueur
    ;'''
    mycursor.execute(sql_compo)
    compo = mycursor.fetchall()
    mycursor.execute("select * from dossierPlan;")
    dossier = mycursor.fetchall()
    playersession = player_session()
    return render_template('player/player_strats.html',
                           playersession = playersession,
                           maps = maps,
                           compo = compo,
                           dossier = dossier)


@player_strats.route('/dir/add/<map>')
def new_dir(map):
    print(map)
    playersession = player_session()
    return render_template('player/player_adddir.html', playersession = playersession, map = map)


@player_strats.route('/dir/add', methods = ['post'])
def valid_new_dir():
    mycursor = get_db().cursor()
    name = request.form.get('name', '')
    description = request.form.get('description', '')
    idmap = request.form.get('idmap', '')
    sql1 = '''insert into dossierplan (nomDossier, description, idMap) values (%s,%s,%s)'''
    mycursor.execute(sql1, (name, description, idmap,))

    sql2 = '''select max(idDossier) from dossierplan;'''
    mycursor.execute(sql2)
    id = mycursor.fetchone()
    idDir = id['idDossier']
    files = []

    for file in request.form.items():
        files.append({'file': file,'idDir':idDir})


    sql3 = '''insert into plan (nomPlan, description, Image, idDossier) values  (%s,%s,%s,%s)'''


    get_db().commit()
    return redirect('/strats_show')


@player_strats.route('/dir/delete/<id>')
def delete_dir(id):

    mycursor = get_db().cursor()
    try:
        get_db().begin()
        sql1 = '''select * from plan where idDossier=%s;'''
        mycursor.execute(sql1,(id,))
        plan = mycursor.fetchone()
        if plan:
            sql2 = '''delete from plan where idDossier;'''
            mycursor.execute(sql2, (id,))

        sql3 = '''delete from dossierplan where idDossier=%s;'''
        mycursor.execute(sql3,(id,))
        get_db().commit()
    except Exception as e:
        get_db().rollback()
        print(f"An error occurred: {e}")
    return redirect('/strats_show')

@player_strats.route('/dir/show/<id>')
def show_dir(id):
    mycursor = get_db().cursor()
    sql1 = '''select * from plan where idDossier=%s; '''
    mycursor.execute(sql1,(id,))
    dir = mycursor.fetchall()
    sql2 = '''select nomDossier from dossierplan where idDossier=%s;'''
    mycursor.execute(sql2, (id,))
    name = mycursor.fetchone()
    playersession = player_session()
    get_db().commit()
    return render_template('player/show_dir.html', dir = dir, name = name,playersession = playersession)


@player_strats.route('/dir/edit/<id>')
def edit_dir(id):
    mycursor = get_db().cursor()
    sql1 = '''select * from dossierplan where idDossier=%s;'''
    mycursor.execute(sql1,(id,))
    directory = mycursor.fetchone()
    sql2 = '''select * from plan where idDossier=%s;'''
    mycursor.execute(sql2, (id,))
    plan = mycursor.fetchall()
    playersession = player_session()
    get_db().commit()
    return render_template('player/edit_dir.html',playersession = playersession, directory = directory, plan = plan)