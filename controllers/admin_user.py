#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, abort, flash, session
from werkzeug.security import generate_password_hash, check_password_hash

from connection_bdd import get_db
from controllers.admin_log import log_edit, log_delete, log_add
from controllers.admin_session import admin_session

admin_user = Blueprint('admin_user', __name__,
                       template_folder = 'templates')


@admin_user.route('/admin/users_show')
def admin_users_show():
    mycursor = get_db().cursor()
    id_user = session['id_user']

    sql = '''SELECT * FROM utilisateur;'''
    mycursor.execute(sql)
    users = mycursor.fetchall()

    adminsession = admin_session()

    get_db().commit()
    return render_template('admin/admin_users_show.html', users = users, adminsession = adminsession)


@admin_user.route('/admin/users_edit/<id>', methods = ['GET'])
def admin_users_edit(id):
    mycursor = get_db().cursor()
    sql = '''SELECT * FROM utilisateur where idUtilisateur=%s;'''
    mycursor.execute(sql, (id,))
    user = mycursor.fetchone()

    adminsession = admin_session()

    get_db().commit()
    return render_template('admin/admin_users_edit.html', adminsession = adminsession, user = user)


@admin_user.route('/admin/users_edit', methods = ['POST'])
def valid_admin_users_edit():
    mycursor = get_db().cursor()

    try:
        get_db().begin()
        id = request.form.get('id', '')
        name = request.form.get('nom', '')
        login = request.form.get('login', '')
        email = request.form.get('email', '')
        mdp = request.form.get('mdp', '')

        sql_oldaction = '''SELECT * FROM utilisateur WHERE idUtilisateur=%s;'''
        mycursor.execute(sql_oldaction, (id,))
        old = mycursor.fetchone()

        if not old:
            flash('Utilisateur introuvable', 'danger')
            return redirect('/admin/users_show')
        mdp_check = check_password_hash(old['mdp'], mdp)
        if not mdp or mdp_check:
            mdp = old['mdp']

        sql_update = '''UPDATE utilisateur SET nomUtilisateur=%s, login=%s, email=%s,mdp=%s WHERE idUtilisateur=%s;'''
        mycursor.execute(sql_update, (name, login, email, mdp, id))

        sql_newaction = '''SELECT * FROM utilisateur WHERE idUtilisateur=%s;'''
        mycursor.execute(sql_newaction, (id,))
        new = mycursor.fetchone()

        if not new:
            flash('Erreur lors de la mise à jour des données utilisateur', 'danger')
            return redirect('/admin/users_show')

        log_edit("UTILISATEURS", old, new)
        get_db().commit()
        if new != old:
            flash('Utilisateur modifié avec succès', 'edited')
    except Exception as e:
        get_db().rollback()
        print(f"Erreur lors de la modifiation de l'utilisateur: {e}")
        flash('Erreur lors de la modifiation de l\'utilisateur', 'delete')
    return redirect('/admin/users_show')


@admin_user.route('/admin/users_delete/<id>', methods = ['GET'])
def admin_users_delete(id):
    mycursor = get_db().cursor()
    try:
        get_db().begin()
        sql = '''SELECT idUtilisateur, idJoueur, idAdmin FROM utilisateur WHERE idUtilisateur = %s;'''
        mycursor.execute(sql, (id,))
        jsonreturn = mycursor.fetchone()
        log_delete("UTILISATEUR", jsonreturn)
        if jsonreturn:
            id_j = jsonreturn['idJoueur']
            id_a = jsonreturn['idAdmin']
            if id_a:
                sql3 = '''DELETE FROM admin WHERE idAdmin = %s;'''
                mycursor.execute(sql3, (id_a,))
            if id_j:
                sql2 = '''DELETE FROM joueurs WHERE idJoueur = %s;'''
                mycursor.execute(sql2, (id_j,))
            sql1 = '''DELETE FROM utilisateur WHERE idUtilisateur = %s;'''
            mycursor.execute(sql1, (id,))

            get_db().commit()
        else:
            flash('Utilisateur introuvable', 'danger')
            return redirect('/admin/users_show')

    except Exception as e:

        get_db().rollback()
        print(f"Erreur lors de la suppression de l'utilisateur: {e}")
        flash('Erreur lors de la suppression de l\'utilisateur', 'delete')

    return redirect('/admin/users_show')


@admin_user.route('/admin/users_add_player/<id>', methods=['GET'])
def admin_users_add_player(id):
    mycursor = get_db().cursor()

    try:
        get_db().begin()

        sql_log = '''SELECT idUtilisateur, nomUtilisateur, login, email, fonction, connected, idAdmin, idJoueur FROM utilisateur WHERE idUtilisateur=%s;'''
        mycursor.execute(sql_log, (id,))
        log = mycursor.fetchone()

        sql_select = '''SELECT * FROM utilisateur WHERE idUtilisateur=%s;'''
        mycursor.execute(sql_select, (id,))
        user = mycursor.fetchone()

        if not user:
            flash('Utilisateur introuvable', 'danger')
            return redirect('/admin/users_show')

        pseudo = user['nomUtilisateur']
        titulaire = 0
        role = 8

        sql_insert = '''INSERT INTO joueurs (pseudo, titulaire, idRole) VALUES (%s, %s, %s);'''
        mycursor.execute(sql_insert, (pseudo, titulaire, role))

        sql_id_select = '''SELECT MAX(idJoueur) AS idJoueur FROM joueurs;'''
        mycursor.execute(sql_id_select)
        new_player = mycursor.fetchone()

        if not new_player:
            flash('Erreur lors de la récupération du nouvel ID du joueur', 'danger')
            get_db().rollback()
            return redirect('/admin/users_show')

        id_player = new_player['idJoueur']

        sql_update_user = '''UPDATE utilisateur SET idJoueur=%s WHERE idUtilisateur=%s;'''
        mycursor.execute(sql_update_user, (id_player, id))

        log_add("JOUEUR", log)
        get_db().commit()

        message = f'Utilisateur promu Joueur ! | {pseudo}'
        flash(message, 'success')
    except Exception as e:
        get_db().rollback()
        print(f"Erreur lors de l'ajout du joueur : {e}")
        flash(f"Erreur lors de l'ajout du joueur : {e}", 'danger')

    return redirect('/admin/users_show')



@admin_user.route('/admin/users_add_admin/<id>', methods=['GET'])
def admin_users_add_admin(id):
    mycursor = get_db().cursor()

    try:
        get_db().begin()

        sql_select = '''SELECT idUtilisateur, nomUtilisateur, login, email, fonction, connected, idAdmin, idJoueur FROM utilisateur WHERE idUtilisateur=%s;'''
        mycursor.execute(sql_select, (id,))
        user = mycursor.fetchone()

        if not user:
            flash('Utilisateur introuvable', 'danger')
            return redirect('/admin/users_show')

        pseudo = user['nomUtilisateur']

        sql_insert = '''INSERT INTO admin (nomAdmin) VALUES (%s);'''
        mycursor.execute(sql_insert, (pseudo,))

        sql_id_select = '''SELECT MAX(idAdmin) AS idAdmin FROM admin;'''
        mycursor.execute(sql_id_select)
        new_admin = mycursor.fetchone()

        if not new_admin:
            flash('Erreur lors de la récupération du nouvel ID admin', 'danger')
            get_db().rollback()
            return redirect('/admin/users_show')

        id_admin = new_admin['idAdmin']

        sql_update_user = '''UPDATE utilisateur SET idAdmin=%s WHERE idUtilisateur=%s;'''
        mycursor.execute(sql_update_user, (id_admin, id))

        log_add("ADMIN", user)

        get_db().commit()

        message = f'Utilisateur promu Administrateur ! | {pseudo}'
        flash(message, 'success')
    except Exception as e:
        get_db().rollback()
        print(f"Erreur lors de l'ajout de l'admin : {e}")
        flash(f"Erreur lors de l'ajout de l'admin : {e}", 'danger')

    return redirect('/admin/users_show')

