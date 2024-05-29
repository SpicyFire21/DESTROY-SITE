#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, abort, flash, session
import pymysql
import requests

from connection_bdd import get_db
from controllers.admin_log import log_add

admin_map_agent = Blueprint('admin_map_agent', __name__,
                            template_folder = 'templates')


@admin_map_agent.route('/admin/mapsagents_show1')
def admin_maps_agents1():
    mycursor = get_db().cursor()
    pyfetchAgent()
    pyfetchMap()

    sql1 = '''SELECT * FROM map order by libelle;'''
    mycursor.execute(sql1)
    maps = mycursor.fetchall()
    sql2 = '''SELECT * FROM agent where nomAgent not like 'None' order by nomAgent;'''
    mycursor.execute(sql2)
    agents = mycursor.fetchall()

    # connecté en tant que
    id_user = session['id_user']
    sql_ps = '''SELECT * FROM utilisateur u 
            join admin a on u.idAdmin = a.idAdmin
            where u.idJoueur=%s;'''
    mycursor.execute(sql_ps, (id_user,))
    adminsession = mycursor.fetchone()

    get_db().commit()
    return render_template('admin/admin_map_agent_show.html', maps = maps, agents = agents, adminsession = adminsession)


def pyfetchAgent():
    list_add = []
    response = requests.get('https://valorant-api.com/v1/agents')
    res = response.json()
    mycursor = get_db().cursor()
    sql_check = '''SELECT * FROM agent;'''
    mycursor.execute(sql_check)
    list_check = [row['nomAgent'] for row in mycursor.fetchall()]

    insert_query = """INSERT INTO agent (nomAgent,imgAgent,roleAgent)VALUES (%s,%s,%s)"""
    data = res['data']

    for row in data:
        if row['isPlayableCharacter'] and row['displayName'] not in list_check:
            img = str(row['displayIcon'])
            bdd_img = "https://media.valorant-api.com/agents/"
            image = img.replace(bdd_img, "")

            role = row['role']['displayName']

            role = 'Initiateur' if role == 'Initiator' else role
            role = 'Sentinelle' if role == 'Sentinel' else role
            role = 'Duelliste' if role == 'Duelist' else role
            role = 'Controlleur' if role == 'Controller' else role

            log = {'displayName': row['displayName']}
            log_add("AGENT", log)
            list_add.append((row['displayName'], image, role,))

    if list_add:
        mycursor.executemany(insert_query, list_add)

    return redirect('/admin/mapsagents_show1')


def pyfetchMap():
    mycursor = get_db().cursor()
    list_add = []
    response = requests.get('https://valorant-api.com/v1/maps')
    res = response.json()

    sql_check = '''SELECT libelle, imgMap FROM map;'''
    mycursor.execute(sql_check)
    list_check = [row['libelle'] for row in mycursor.fetchall()]

    insert_query = """INSERT INTO map (libelle, imgMap) VALUES (%s,%s)"""
    data = res['data']

    for row in data:
        if row['tacticalDescription'] and row['displayName'] not in list_check:
            img = str(row['splash'])
            bdd_img = "https://media.valorant-api.com/maps/"
            image = img.replace(bdd_img, "")
            log = {'displayName': row['displayName']}
            log_add("MAP", log)
            list_add.append((row['displayName'], image))
    if list_add:
        mycursor.executemany(insert_query, list_add)
    return redirect('/admin/mapsagents_show1')


@admin_map_agent.route('/admin/maps_edit/<id>', methods = ['GET'])
def admin_maps_edit(id):
    mycursor = get_db().cursor()
    sql = '''Select * from map where idMap =%s;'''
    mycursor.execute(sql, (id,))
    map = mycursor.fetchone()

    # connecté en tant que
    id_user = session['id_user']
    sql_ps = '''SELECT * FROM utilisateur u 
                join admin a on u.idAdmin = a.idAdmin
                where u.idJoueur=%s;'''
    mycursor.execute(sql_ps, (id_user,))
    adminsession = mycursor.fetchone()
    # print(map)
    get_db().commit()
    return render_template('admin/admin_map_edit.html', adminsession = adminsession, map = map)


@admin_map_agent.route('/admin/maps_edit', methods = ['POST'])
def valid_admin_maps_edit():
    mycursor = get_db().cursor()
    id = request.form.get('id', '')
    newname = request.form.get('libelle', '')
    oldname = request.form.get('hiddenname', '')
    # print(id, newname)
    sql = '''UPDATE map SET libelle=%s where idMap=%s;'''
    mycursor.execute(sql, (newname, id,))
    get_db().commit()
    message = 'Nom de Map modifié ! | ' + oldname + ' → ' + newname
    flash(message, 'edited')
    return redirect('/admin/mapsagents_show2')


@admin_map_agent.route('/admin/agents_edit/<id>', methods = ['GET'])
def admin_agents_edit(id):
    mycursor = get_db().cursor()
    sql = '''Select * from agent where idAgent =%s;'''
    mycursor.execute(sql, (id,))
    agent = mycursor.fetchone()

    # connecté en tant que
    id_user = session['id_user']
    sql_ps = '''SELECT * FROM utilisateur u 
                join admin a on u.idAdmin = a.idAdmin
                where u.idJoueur=%s;'''
    mycursor.execute(sql_ps, (id_user,))
    adminsession = mycursor.fetchone()

    get_db().commit()
    return render_template('admin/admin_agent_edit.html', adminsession = adminsession, agent = agent)


@admin_map_agent.route('/admin/agents_edit', methods = ['POST'])
def valid_admin_agent_edit():
    mycursor = get_db().cursor()
    id = request.form.get('id', '')
    newname = request.form.get('nomAgent', '')
    oldname = request.form.get('hiddenname', '')
    sql = '''UPDATE agent SET nomAgent=%s where idAgent=%s;'''
    mycursor.execute(sql, (newname, id,))
    get_db().commit()
    message = 'Nom d\'Agent modifié ! | ' + oldname + ' → ' + newname
    flash(message, 'edited')
    return redirect('/admin/mapsagents_show2')


# @admin_map_agent.route('/admin/agents_delete/<id>', methods = ['GET'])
# def admin_agent_delete(id):
#     mycursor = get_db().cursor()
#
#     sql_select = '''SELECT * FROM agent where idAgent=%s;'''
#     mycursor.execute(sql_select, (id,))
#     jsonmap = mycursor.fetchone()
#     name = jsonmap['nomAgent']
#
#     sql_del = '''DELETE FROM agent where idAgent=%s;'''
#     mycursor.execute(sql_del, (id,))
#     message = 'Agent Supprimé ! | ' + name
#     flash(message, 'deleted')
#     return redirect('/admin/mapsagents_show2')


# @admin_map_agent.route('/admin/maps_delete/<id>', methods = ['GET'])
# def admin_map_delete(id):
#     mycursor = get_db().cursor()
#
#     sql_select = '''SELECT * FROM map where idMap=%s;'''
#     mycursor.execute(sql_select, (id,))
#     jsonmap = mycursor.fetchone()
#     name = jsonmap['libelle']
#     sql = '''DELETE FROM map where idMap=%s;'''
#     mycursor.execute(sql, (id,))
#     message = 'Map Supprimé ! | ' + name
#     flash(message, 'deleted')
#     return redirect('/admin/mapsagents_show2')


# @admin_map_agent.route('/admin/maps_add', methods = ['GET'])
# def admin_map_add():
#     mycursor = get_db().cursor()
#     # connecté en tant que
#     id_user = session['id_user']
#     sql_ps = '''SELECT * FROM utilisateur u
#                     join admin a on u.idAdmin = a.idAdmin
#                     where u.idJoueur=%s;'''
#     mycursor.execute(sql_ps, (id_user,))
#     adminsession = mycursor.fetchone()
#
#     get_db().commit()
#     return render_template('admin/admin_map_add.html', adminsession = adminsession)

#
# @admin_map_agent.route('/admin/agents_add', methods = ['GET'])
# def admin_agents_add():
#     mycursor = get_db().cursor()
#     # connecté en tant que
#     id_user = session['id_user']
#     sql_ps = '''SELECT * FROM utilisateur u
#                     join admin a on u.idAdmin = a.idAdmin
#                     where u.idJoueur=%s;'''
#     mycursor.execute(sql_ps, (id_user,))
#     adminsession = mycursor.fetchone()
#
#     get_db().commit()
#     return render_template('admin/admin_agent_add.html', adminsession = adminsession)


# @admin_map_agent.route('/admin/maps_add', methods = ['POST'])
# def valid_admin_map_add():
#     mycursor = get_db().cursor()
#     name = request.form.get('libelle', '')
#     sql = '''INSERT INTO map (libelle) VALUES (%s);'''
#     mycursor.execute(sql, (name,))
#     get_db().commit()
#
#     return redirect('/admin/mapsagents_show2')


# @admin_map_agent.route('/admin/agents_add', methods = ['POST'])
# def valid_admin_agent_add():
#     mycursor = get_db().cursor()
#     name = request.form.get('nomAgent', '')
#     sql = '''INSERT INTO agent (nomAgent) VALUES (%s);'''
#     mycursor.execute(sql, (name,))
#     get_db().commit()
#     return redirect('/admin/mapsagents_show2')


@admin_map_agent.route('/admin/mapsagents_show2')
def admin_maps_agents2():
    mycursor = get_db().cursor()
    sql1 = '''SELECT * FROM map order by libelle;'''
    mycursor.execute(sql1)
    maps = mycursor.fetchall()
    sql2 = '''SELECT * FROM agent where nomAgent not like 'None' order by nomAgent;'''
    mycursor.execute(sql2)
    agents = mycursor.fetchall()

    # connecté en tant que
    id_user = session['id_user']
    sql_ps = '''SELECT * FROM utilisateur u 
            join admin a on u.idAdmin = a.idAdmin
            where u.idJoueur=%s;'''
    mycursor.execute(sql_ps, (id_user,))
    adminsession = mycursor.fetchone()

    get_db().commit()
    return render_template('admin/admin_map_agent_show.html', maps = maps, agents = agents, adminsession = adminsession)
