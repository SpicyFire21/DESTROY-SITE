#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint, jsonify
from flask import Flask, request, render_template, redirect, abort, flash, session

from connection_bdd import get_db

admin_index = Blueprint('admin_index', __name__,
                        template_folder = 'templates')


@admin_index.route('/admin/index')
def admin_show():
    mycursor = get_db().cursor()
    id_user = session['id_user']
    print(id_user)
    sql = '''SELECT * FROM utilisateur u
        join admin a on u.idAdmin = a.idAdmin
        where u.idUtilisateur = %s;'''
    mycursor.execute(sql, (id_user,))
    staff = mycursor.fetchone()
    print('staff', staff)

    # connecté en tant que
    id_user = session['id_user']
    sql_ps = '''SELECT * FROM utilisateur u 
            join admin a on u.idAdmin = a.idAdmin
            where u.idJoueur=%s;'''
    mycursor.execute(sql_ps, (id_user,))
    adminsession = mycursor.fetchone()

    get_db().commit()
    if staff:
        return render_template('admin/index.html', staff = staff, adminsession = adminsession)
    else:
        flash(u'Vous n\'avez pas les droits pour être inscrit en tant qu\' Admin ou votre compte n\'existe pas.',
              'alert-warning')
        return redirect('/login')




@admin_index.route('/testjs/show', methods = ['GET'])
def testjs_show():
    mycursor = get_db().cursor()
    # connecté en tant que
    id_user = session['id_user']
    sql_ps = '''SELECT * FROM utilisateur u 
                    join admin a on u.idAdmin = a.idAdmin
                    where u.idJoueur=%s;'''
    mycursor.execute(sql_ps, (id_user,))
    adminsession = mycursor.fetchone()
    get_db().commit()
    return render_template('test/testjs.html', adminsession = adminsession)
