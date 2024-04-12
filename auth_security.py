#! /usr/bin/python
# -*- coding:utf-8 -*-

from flask import Blueprint
from flask import Flask, request, render_template, redirect, flash, session
from werkzeug.security import generate_password_hash, check_password_hash

from connection_bdd import get_db

auth_security = Blueprint('auth_security', __name__,
                          template_folder = 'templates')


@auth_security.route('/login')
def auth_login():
    return render_template('auth/login.html')


@auth_security.route('/login', methods = ['POST'])
def auth_login_post():
    mycursor = get_db().cursor()
    login = request.form.get('login')
    password = request.form.get('password')
    # tuple_select = (login,)
    sql = " SELECT * FROM joueurs WHERE login = %s; "
    retour = mycursor.execute(sql, (login,))
    user = mycursor.fetchone()
    if user:
        mdp_ok = check_password_hash(user['mdp'], password)

        if not mdp_ok:
            flash(u'Vérifier votre mot de passe et essayer encore.', 'alert-warning')
            return redirect('/login')
        else:
            session['login'] = user['login']
            session['fonction'] = user['fonction']
            session['id_user'] = user['idJoueur']
            print("GG")
            if user['fonction'] == 'admin':
                return redirect('/admin/index')
            elif user['fonction'] == 'player':
                return redirect('/player/index')
            else:
                return redirect('/visitor/index')
    else:
        flash(u'Vérifier votre login et essayer encore.', 'alert-warning')
        return redirect('/login')


@auth_security.route('/signup')
def auth_signup():
    return render_template('auth/signup.html')


@auth_security.route('/signup', methods = ['POST'])
def auth_signup_post():
    mycursor = get_db().cursor()
    login = request.form.get('login')
    pseudo = login
    email = request.form.get('email')
    password = request.form.get('password')
    tuple_select = (login, email,)
    sql = " SELECT * FROM joueurs WHERE login = %s AND email = %s; "
    retour = mycursor.execute(sql, tuple_select)
    user = mycursor.fetchone()
    if user:
        flash(u'votre adresse Email et/ou  votre Login existe déjà', 'alert-warning')
        return redirect('/signup')

    # ajouter un nouveau user
    password = generate_password_hash(password, method = 'pbkdf2:sha256')
    tuple_insert = (pseudo, login, email, password, 'player')  # changer player par visitor
    sql = """  INSERT INTO joueurs (pseudo,login,email, mdp,fonction) VALUES (%s, %s, %s, %s, %s);  """
    mycursor.execute(sql, tuple_insert)
    print(tuple_insert)
    get_db().commit()
    sql = """  SELECT last_insert_id() as last_insert_id;  """
    mycursor.execute(sql)
    info_last_id = mycursor.fetchone()
    id_user = info_last_id['last_insert_id']
    print('last_insert_id', id_user)
    session.pop('login', None)
    session.pop('fonction', None)
    session.pop('id_user', None)
    session['login'] = login
    session['fonction'] = 'player'
    session['idJoueur'] = id_user
    return redirect('/')


@auth_security.route('/logout')
def auth_logout():
    session.pop('login', None)
    session.pop('role', None)
    session.pop('id_user', None)
    return redirect('/')


@auth_security.route('/forget-password', methods = ['GET'])
def forget_password():
    return render_template('auth/forget_password.html')
