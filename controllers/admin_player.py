#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, abort, flash, session

from connection_bdd import get_db

admin_player = Blueprint('admin_player', __name__,
                         template_folder = 'templates')


@admin_player.route('/admin/players_show')
def admin_players_show():
    mycursor = get_db().cursor()
    id_user = session['id_user']

    sql = '''SELECT * FROM utilisateur u
    join joueurs j on u.idJoueur = j.idJoueur
    join role r on j.idRole = r.idRole;'''
    mycursor.execute(sql)
    players = mycursor.fetchall()
    print(players)
    # connecté en tant que
    id_user = session['id_user']
    sql_ps = '''SELECT * FROM utilisateur u 
            join admin a on u.idAdmin = a.idAdmin
            where u.idJoueur=%s;'''
    mycursor.execute(sql_ps, (id_user,))
    adminsession = mycursor.fetchone()

    get_db().commit()
    return render_template('admin/admin_player_show.html', players = players, adminsession = adminsession)


@admin_player.route('/admin/player_edit/<id>', methods = ['GET'])
def admin_player_edit(id):
    mycursor = get_db().cursor()
    sql_player = '''SELECT * FROM joueurs 
    join role r on joueurs.idRole = r.idRole
    where idJoueur=%s;'''
    mycursor.execute(sql_player, (id,))
    player = mycursor.fetchone()

    sql_role = '''SELECT * FROM role;'''
    mycursor.execute(sql_role)
    roles = mycursor.fetchall()
    # connecté en tant que
    id_user = session['id_user']
    sql_ps = '''SELECT * FROM utilisateur u 
                join admin a on u.idAdmin = a.idAdmin
                where u.idJoueur=%s;'''
    mycursor.execute(sql_ps, (id_user,))
    adminsession = mycursor.fetchone()
    print("role", roles)
    get_db().commit()
    return render_template('admin/admin_player_edit.html', player = player, adminsession = adminsession, roles = roles)


@admin_player.route('/admin/player_edit', methods = ['POST'])
def valid_admin_player_edit():
    global titu
    mycursor = get_db().cursor()
    id = request.form.get('id', '')
    pseudo = request.form.get('pseudo', '')
    titulaire = request.form.get('titulaire', '')
    role = request.form.get('role', '')
    sql1 = '''UPDATE joueurs j 
    join role r on j.idRole = r.idRole
    set j.pseudo=%s,j.titulaire=%s, j.idRole=%s where j.idJoueur=%s;'''
    mycursor.execute(sql1, (pseudo, titulaire, role, id,))
    get_db().commit()

    sql2 = '''SELECT * from role where idRole=%s;'''
    mycursor.execute(sql2, (role,))
    jsonreturn = mycursor.fetchone()
    role = jsonreturn['libelle']
    if titulaire == 1:
        titu = "oui"
    else :
        titu = "non"

    message = 'Joueur Modifié ! | pseudo : ' + pseudo + ' | Titulaire : ' + titu + ' | role : ' + role
    flash(message, 'edited')
    return redirect('/admin/players_show')


@admin_player.route('/admin/player_delete/<id>', methods = ['GET'])
def admin_player_delete(id):
    mycursor = get_db().cursor()

    sql = '''SELECT * FROM joueurs where idJoueur=%s;'''
    mycursor.execute(sql, (id,))
    jsonreturn = mycursor.fetchone()
    name = jsonreturn['pseudo']

    sql1 = '''DELETE FROM joueurs where idJoueur=%s;'''
    mycursor.execute(sql1, (id,))

    sql2 = '''Update utilisateur set idJoueur=null where idJoueur=%s;'''
    mycursor.execute(sql2, (id,))
    get_db().commit()
    message = 'Joueur Supprimé ! | ' + name
    flash(message, 'deleted')
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
