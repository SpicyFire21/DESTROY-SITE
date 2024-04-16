#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, abort, flash, session
from werkzeug.security import generate_password_hash

from connection_bdd import get_db

admin_user = Blueprint('admin_user', __name__,
                       template_folder = 'templates')


@admin_user.route('/admin/users_show')
def admin_users_show():
    mycursor = get_db().cursor()
    id_user = session['id_user']

    sql = '''SELECT * FROM utilisateur;'''
    mycursor.execute(sql)
    users = mycursor.fetchall()

    # connecté en tant que
    id_user = session['id_user']
    sql_ps = '''SELECT * FROM utilisateur u 
            join admin a on u.idAdmin = a.idAdmin
            where u.idJoueur=%s;'''
    mycursor.execute(sql_ps, (id_user,))
    adminsession = mycursor.fetchone()

    get_db().commit()
    return render_template('admin/admin_users_show.html', users = users, adminsession = adminsession)


@admin_user.route('/admin/users_edit/<id>', methods = ['GET'])
def admin_users_edit(id):
    mycursor = get_db().cursor()
    sql = '''SELECT * FROM utilisateur where idUtilisateur=%s;'''
    mycursor.execute(sql, (id,))
    user = mycursor.fetchone()

    # connecté en tant que
    id_user = session['id_user']
    sql_ps = '''SELECT * FROM utilisateur u 
                join admin a on u.idAdmin = a.idAdmin
                where u.idJoueur=%s;'''
    mycursor.execute(sql_ps, (id_user,))
    adminsession = mycursor.fetchone()

    get_db().commit()
    return render_template('admin/admin_users_edit.html', adminsession = adminsession, user = user)


@admin_user.route('/admin/users_edit', methods = ['POST'])
def valid_admin_users_edit():
    mycursor = get_db().cursor()
    id = request.form.get('id', '')
    name = request.form.get('nom', '')
    login = request.form.get('login', '')
    email = request.form.get('email', '')
    # mdp = request.form.get('mdp', '')

    # mdp = generate_password_hash(mdp, method = 'pbkdf2:sha256')

    sql = '''UPDATE utilisateur u set u.nomUtilisateur=%s, u.login=%s, u.email=%s where u.idUtilisateur=%s;'''
    mycursor.execute(sql, (name, login, email, id))
    get_db().commit()
    return redirect('/admin/users_show')


@admin_user.route('/admin/users_delete/<id>', methods = ['GET'])
def admin_users_delete(id):
    mycursor = get_db().cursor()
    sql = '''DELETE FROM utilisateur where idUtilisateur=%s;'''
    mycursor.execute(sql, (id,))
    get_db().commit()
    return redirect('/admin/users_show')


@admin_user.route('/admin/users_add_player/<id>', methods = ['GET'])
def admin_users_add_player(id):
    mycursor = get_db().cursor()

    sql_select = '''SELECT * FROM utilisateur u where idUtilisateur=%s;'''
    mycursor.execute(sql_select, (id,))
    jsonreturn = mycursor.fetchone()
    pseudo = jsonreturn['nomUtilisateur']
    titulaire = 0
    print(jsonreturn)
    role = 8
    sql_insert = '''INSERT INTO joueurs (pseudo, titulaire,idRole) VALUES (%s,%s,%s);'''
    mycursor.execute(sql_insert, (pseudo, titulaire,role))

    sql_id_select = '''SELECT max(idJoueur) from joueurs;'''
    mycursor.execute(sql_id_select)
    id_player_js = mycursor.fetchone()
    print(id_player_js)
    id_player = id_player_js['max(idJoueur)']

    sql_id_add = '''UPDATE utilisateur set idJoueur=%s where idUtilisateur=%s;'''
    mycursor.execute(sql_id_add, (id_player, id,))

    get_db().commit()
    return redirect('/admin/users_show')

@admin_user.route('/admin/users_add_admin/<id>', methods = ['GET'])
def admin_users_add_admin(id):
    mycursor = get_db().cursor()

    sql_select = '''SELECT * FROM utilisateur u where idUtilisateur=%s;'''
    mycursor.execute(sql_select, (id,))
    jsonreturn = mycursor.fetchone()
    pseudo = jsonreturn['nomUtilisateur']

    print(jsonreturn)

    sql_insert = '''INSERT INTO admin (nomAdmin) VALUES (%s);'''
    mycursor.execute(sql_insert, (pseudo,))

    sql_id_select = '''SELECT max(idAdmin) from admin;'''
    mycursor.execute(sql_id_select)
    id_player_js = mycursor.fetchone()
    print(id_player_js)
    id_player = id_player_js['max(idAdmin)']

    sql_id_add = '''UPDATE utilisateur set idAdmin=%s where idUtilisateur=%s;'''
    mycursor.execute(sql_id_add, (id_player, id,))

    get_db().commit()
    return redirect('/admin/users_show')