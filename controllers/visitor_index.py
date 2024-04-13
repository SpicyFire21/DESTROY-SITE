#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, abort, flash, session

from connection_bdd import get_db

visitor_index = Blueprint('visitor_index', __name__,
                          template_folder = 'templates')


@visitor_index.route('/visitor/index')
def visitor_show():
    mycursor = get_db().cursor()
    id_user = session['id_user']
    sql = '''SELECT * FROM utilisateur u where u.idUtilisateur = %s;'''
    mycursor.execute(sql, (id_user,))
    user = mycursor.fetchone()
    get_db().commit()
    if user:
        return render_template('visitor/index.html', user = user)
    else:
        flash(u'Votre compte n\'existe pas, veuillez en créer un.', 'alert-warning')
        return redirect('/login')
