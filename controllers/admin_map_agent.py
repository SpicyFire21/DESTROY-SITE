#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, abort, flash, session
import pymysql
import requests

from connection_bdd import get_db
from controllers.admin_log import log_add, log_add_api
from controllers.admin_session import admin_session

admin_map_agent = Blueprint('admin_map_agent', __name__, template_folder='templates')

@admin_map_agent.route('/admin/mapsagents_show1')
def admin_maps_agents1():
    global maps, agents, adminsession
    mycursor = get_db().cursor()
    try:
        pyfetchAgent()
        pyfetchMap()

        sql1 = '''SELECT * FROM map order by libelle;'''
        mycursor.execute(sql1)
        maps = mycursor.fetchall()
        sql2 = '''SELECT * FROM agent where nomAgent not like 'None' order by nomAgent;'''
        mycursor.execute(sql2)
        agents = mycursor.fetchall()

        id_admin = session['id_admin']
        adminsession = admin_session()
        get_db().commit()
    except Exception as e:
        flash(f"Erreur lors du chargement des agents et des maps: {e}", 'delete')
    return render_template('admin/admin_map_agent_show.html', maps=maps, agents=agents, adminsession=adminsession)

def pyfetchAgent():
    mycursor = get_db().cursor()
    try:
        get_db().begin()
        list_add = []
        response = requests.get('https://valorant-api.com/v1/agents')
        res = response.json()
        sql_check = '''SELECT * FROM agent;'''
        mycursor.execute(sql_check)
        list_check = [row['nomAgent'] for row in mycursor.fetchall()]

        insert_query = """INSERT INTO agent (nomAgent,imgAgent,roleAgent) VALUES (%s,%s,%s)"""
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
                log_add_api("AGENT", log)
                list_add.append((row['displayName'], image, role))

        if list_add:
            mycursor.executemany(insert_query, list_add)
        get_db().commit()
    except Exception as e:
        get_db().rollback()
        flash(f"Erreur lors de la mise à jour des agents: {e}", 'delete')

def pyfetchMap():
    mycursor = get_db().cursor()
    try:
        get_db().begin()
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
                log_add_api("MAP", log)
                list_add.append((row['displayName'], image))

        if list_add:
            mycursor.executemany(insert_query, list_add)
        get_db().commit()
    except Exception as e:
        get_db().rollback()
        flash(f"Erreur lors de la mise à jour des maps: {e}", 'delete')

# @admin_map_agent.route('/admin/maps_edit/<id>', methods=['GET'])
# def admin_maps_edit(id):
#     global adminsession, map
#     mycursor = get_db().cursor()
#     try:
#         sql = '''Select * from map where idMap = %s;'''
#         mycursor.execute(sql, (id,))
#         map = mycursor.fetchone()
#         adminsession = admin_session()
#         get_db().commit()
#     except Exception as e:
#         flash(f"Erreur lors du chargement de la map: {e}", 'delete')
#     return render_template('admin/admin_map_edit.html', adminsession=adminsession, map=map)
# 
# @admin_map_agent.route('/admin/maps_edit', methods=['POST'])
# def valid_admin_maps_edit():
#     mycursor = get_db().cursor()
#     try:
#         get_db().begin()
#         id = request.form.get('id', '')
#         newname = request.form.get('libelle', '')
#         oldname = request.form.get('hiddenname', '')
#         sql = '''UPDATE map SET libelle = %s where idMap = %s;'''
#         mycursor.execute(sql, (newname, id,))
#         get_db().commit()
#         message = 'Nom de Map modifié ! | ' + oldname + ' → ' + newname
#         flash(message, 'edited')
#     except Exception as e:
#         get_db().rollback()
#         flash(f"Erreur lors de la modification de la map: {e}", 'delete')
#     return redirect('/admin/mapsagents_show2')
# 
# @admin_map_agent.route('/admin/agents_edit/<id>', methods=['GET'])
# def admin_agents_edit(id):
#     global adminsession, agent
#     mycursor = get_db().cursor()
#     try:
#         sql = '''Select * from agent where idAgent = %s;'''
#         mycursor.execute(sql, (id,))
#         agent = mycursor.fetchone()
#         adminsession = admin_session()
#         get_db().commit()
#     except Exception as e:
#         flash(f"Erreur lors du chargement de l'agent: {e}", 'delete')
#     return render_template('admin/admin_agent_edit.html', adminsession=adminsession, agent=agent)
# 
# @admin_map_agent.route('/admin/agents_edit', methods=['POST'])
# def valid_admin_agent_edit():
#     mycursor = get_db().cursor()
#     try:
#         get_db().begin()
#         id = request.form.get('id', '')
#         newname = request.form.get('nomAgent', '')
#         oldname = request.form.get('hiddenname', '')
#         sql = '''UPDATE agent SET nomAgent = %s where idAgent = %s;'''
#         mycursor.execute(sql, (newname, id,))
#         get_db().commit()
#         message = 'Nom d\'Agent modifié ! | ' + oldname + ' → ' + newname
#         flash(message, 'edited')
#     except Exception as e:
#         get_db().rollback()
#         flash(f"Erreur lors de la modification de l'agent: {e}", 'delete')
#     return redirect('/admin/mapsagents_show2')

@admin_map_agent.route('/admin/mapsagents_show2')
def admin_maps_agents2():
    global maps, agents, adminsession
    mycursor = get_db().cursor()
    try:
        sql1 = '''SELECT * FROM map order by libelle;'''
        mycursor.execute(sql1)
        maps = mycursor.fetchall()
        sql2 = '''SELECT * FROM agent where nomAgent not like 'None' order by nomAgent;'''
        mycursor.execute(sql2)
        agents = mycursor.fetchall()

        id_admin = session['id_admin']
        adminsession = admin_session()
        get_db().commit()
    except Exception as e:
        flash(f"Erreur lors du chargement des agents et des maps: {e}", 'delete')
    return render_template('admin/admin_map_agent_show.html', maps=maps, agents=agents, adminsession=adminsession)
