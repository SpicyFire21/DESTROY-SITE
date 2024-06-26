#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, abort, flash, session

from connection_bdd import get_db
from controllers.admin_log import log_delete, log_edit
from controllers.admin_session import admin_session

admin_player = Blueprint('admin_player', __name__, template_folder = 'templates')


@admin_player.route('/admin/players_show')
def admin_players_show():
    mycursor = get_db().cursor()
    try:
        id_user = session['id_user']
        sql = '''SELECT * FROM utilisateur u
                 JOIN joueurs j ON u.idJoueur = j.idJoueur
                 JOIN role r ON j.idRole = r.idRole;'''
        mycursor.execute(sql)
        players = mycursor.fetchall()

        adminsession = admin_session()
        get_db().commit()
    except Exception as e:
        flash(f"Erreur lors du chargement des joueurs : {e}", 'delete')
        players = []
        adminsession = admin_session()
    return render_template('admin/admin_player_show.html', players = players, adminsession = adminsession)


@admin_player.route('/admin/player_edit/<id>', methods = ['GET'])
def admin_player_edit(id):
    mycursor = get_db().cursor()
    try:
        sql_player = '''SELECT * FROM joueurs 
                        JOIN role r ON joueurs.idRole = r.idRole
                        WHERE idJoueur=%s;'''
        mycursor.execute(sql_player, (id,))
        player = mycursor.fetchone()
        sql_role = '''SELECT * FROM role;'''
        mycursor.execute(sql_role)
        roles = mycursor.fetchall()
        adminsession = admin_session()
        get_db().commit()
    except Exception as e:
        flash(f"Erreur lors du chargement du joueur : {e}", 'delete')
        player = {}
        roles = []
        adminsession = admin_session()
    return render_template('admin/admin_player_edit.html', player = player, adminsession = adminsession, roles = roles)


@admin_player.route('/admin/player_edit', methods = ['POST'])
def valid_admin_player_edit():
    global titu
    mycursor = get_db().cursor()
    try:
        get_db().begin()
        id = request.form.get('id', '')
        pseudo = request.form.get('pseudo', '')
        titulaire = request.form.get('titulaire', '')
        role = request.form.get('role', '')

        sql_old = '''SELECT * from joueurs where idJoueur=%s;'''
        mycursor.execute(sql_old,(id,))
        old = mycursor.fetchone()


        sql1 = '''UPDATE joueurs j 
                  JOIN role r ON j.idRole = r.idRole
                  SET j.pseudo=%s, j.titulaire=%s, j.idRole=%s 
                  WHERE j.idJoueur=%s;'''
        mycursor.execute(sql1, (pseudo, titulaire, role, id,))

        sql_new = '''SELECT * from joueurs where idJoueur=%s;'''
        mycursor.execute(sql_new, (id,))
        new = mycursor.fetchone()

        sql2 = '''SELECT * FROM role WHERE idRole=%s;'''
        mycursor.execute(sql2, (role,))
        jsonreturn = mycursor.fetchone()
        role = jsonreturn['libelle']
        if titulaire == "1":
            titu = "oui"
        else:
            titu = "non"
        message = 'Joueur Modifié ! | pseudo : ' + pseudo + ' | Titulaire : ' + titu + ' | role : ' + role
        if old !=new:

            flash(message, 'edited')
        log_edit("JOUEUR",old,new)
        get_db().commit()
    except Exception as e:
        get_db().rollback()
        flash(f"Erreur lors de la modification du joueur : {e}", 'delete')
    return redirect('/admin/players_show')


@admin_player.route('/admin/player_delete/<id>', methods = ['GET'])
def admin_player_delete(id):
    mycursor = get_db().cursor()
    try:
        get_db().begin()
        sql = '''SELECT * FROM joueurs WHERE idJoueur=%s;'''
        mycursor.execute(sql, (id,))
        jsonreturn = mycursor.fetchone()
        name = jsonreturn['pseudo']

        sql1 = '''DELETE FROM joueurs WHERE idJoueur=%s;'''
        mycursor.execute(sql1, (id,))

        sql2 = '''UPDATE utilisateur SET idJoueur=NULL WHERE idJoueur=%s;'''
        mycursor.execute(sql2, (id,))
        get_db().commit()
        log_delete("JOUEUR", jsonreturn)
        message = 'Joueur Supprimé ! | ' + name
        flash(message, 'deleted')
    except Exception as e:
        get_db().rollback()
        flash(f"Erreur lors de la suppression du joueur : {e}", 'delete')
    return redirect('/admin/players_show')

# @admin_player.route('/admin/admin_delete/<id>', methods = ['GET'])
# def admin_admin_delete(id):
#     mycursor = get_db().cursor()
#     sql1 = '''DELETE FROM admin where idAdmin=%s;'''
#     mycursor.execute(sql1, (id,))
#
#     sql2 = '''Update utilisateur set idAdmin=null where idAdmin=%s;'''
#     mycursor.execute(sql2, (id,))
#     get_db().commit()
#     return redirect('/admin/players_show')
