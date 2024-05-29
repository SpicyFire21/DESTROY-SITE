#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, abort, flash, session
from werkzeug.security import generate_password_hash, check_password_hash

from connection_bdd import get_db
from controllers.admin_log import log_delete

admin_root = Blueprint('admin_root', __name__,
                       template_folder = 'templates')


@admin_root.route('/admin/root/login')
def admin_root_login():
    mycursor = get_db().cursor()

    # connecté en tant que
    id_user = session['id_user']
    sql_ps = '''SELECT * FROM utilisateur u 
            join admin a on u.idAdmin = a.idAdmin
            where u.idJoueur=%s;'''
    mycursor.execute(sql_ps, (id_user,))
    adminsession = mycursor.fetchone()

    get_db().commit()
    return render_template('admin/admin_root_login.html', adminsession = adminsession)


@admin_root.route('/admin/root/login', methods = ['POST'])
def root_login():
    mycursor = get_db().cursor()
    login = request.form.get('login')
    mdp = request.form.get('mdp', '')

    sql = '''SELECT * from root where nomRoot=%s;'''
    mycursor.execute(sql, (login,))
    root = mycursor.fetchone()

    if root:
        mdp_check = check_password_hash(root['mdp'], mdp)
        if mdp_check:
            return redirect('/admin/show')
        else:
            flash(u'Vérifier votre mot de passe et essayer encore.', 'alert-warning')
            return redirect('/admin/root/login')
    else:
        flash(u'Vérifier votre login et essayer encore ou vous n\'avez pas de compte.', 'alert-warning')
        return redirect('/admin/root/login')


@admin_root.route('/admin/show')
def admin_show():
    mycursor = get_db().cursor()

    sql = '''SELECT * FROM admin
    join utilisateur u on admin.idAdmin = u.idAdmin;'''
    mycursor.execute(sql)
    admins = mycursor.fetchall()

    # connecté en tant que
    id_user = session['id_user']
    sql_ps = '''SELECT * FROM utilisateur u 
                join admin a on u.idAdmin = a.idAdmin
                where u.idJoueur=%s;'''
    mycursor.execute(sql_ps, (id_user,))
    adminsession = mycursor.fetchone()
    return render_template('admin/admin_show.html', admins = admins, adminsession = adminsession)


@admin_root.route('/admin/admin_delete/<id>')
def admin_delete(id):
    mycursor = get_db().cursor()
    sql_select = '''SELECT idAdmin,nomAdmin FROM admin where idAdmin=%s;'''
    mycursor.execute(sql_select, (id,))
    admin = mycursor.fetchone()
    log_delete("ADMIN", admin)
    sql_delete = '''DELETE FROM admin where idAdmin=%s;'''
    mycursor.execute(sql_delete, (id,))
    sql = '''UPDATE utilisateur set idAdmin=null where idAdmin=%s;'''
    mycursor.execute(sql, (id,))
    get_db().commit()
    return redirect('/admin/root/login')
