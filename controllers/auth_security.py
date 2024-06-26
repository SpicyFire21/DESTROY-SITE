#! /usr/bin/python
# -*- coding:utf-8 -*-

from flask import Blueprint
from flask import Flask, request, render_template, redirect, flash, session
from werkzeug.security import generate_password_hash, check_password_hash

from connection_bdd import get_db
from controllers.admin_log import log_add

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
    fonction = request.form.get('fonction', '')

    sql = " SELECT * FROM utilisateur WHERE login = %s; "
    mycursor.execute(sql, (login,))
    user = mycursor.fetchone()
    print('user', user)
    if user:
        mdp_ok = check_password_hash(user['mdp'], password)
        if not mdp_ok:
            flash(u'Vérifier votre mot de passe et essayer encore.', 'alert-warning')
            return redirect('/login')
        else:
            user['fonction'] = fonction
            session['login'] = user['login']
            session['fonction'] = user['fonction']
            session['id_user'] = user['idUtilisateur']
            session['id_admin'] = user['idAdmin']
            session['id_player'] = user['idJoueur']

            print("conn",session['login'],session['fonction'],session['id_user'],session['id_admin'],session['id_player'] )

            sql_c = '''UPDATE utilisateur u set u.connected=1, u.fonction=%s where idUtilisateur=%s;'''
            mycursor.execute(sql_c,(fonction,user['idUtilisateur'],))

            if session['fonction'] == 'ADMIN':
                return redirect('/admin/index')
            elif session['fonction'] == 'PLAYER':
                return redirect('/player/index')
            else:
                return redirect('/visitor/index')
    else:
        flash(u'Vérifier votre login et essayer encore ou vous n\'avez pas de compte.', 'alert-warning')
        return redirect('/login')


@auth_security.route('/signup')
def auth_signup():
    return render_template('auth/signup.html')


@auth_security.route('/signup', methods=['POST'])
def auth_signup_post():
    mycursor = get_db().cursor()
    login = request.form.get('login')
    pseudo = login
    email = request.form.get('email')
    password = request.form.get('password')

    try:
        get_db().begin()

        tuple_select = (login, email,)
        sql = "SELECT * FROM utilisateur WHERE login = %s OR email = %s;"
        mycursor.execute(sql, tuple_select)
        user = mycursor.fetchone()

        if user:
            flash(u'Votre adresse Email et/ou votre Login existe déjà', 'alert-warning')
            return redirect('/signup')

        password_hashed = generate_password_hash(password, method='pbkdf2:sha256')
        tuple_insert = (pseudo, login, email, password_hashed, 'visitor',)
        sql_insert = """INSERT INTO utilisateur (nomUtilisateur, login, email, mdp, fonction) VALUES (%s, %s, %s, %s, %s);"""
        mycursor.execute(sql_insert, tuple_insert)

        sql_last_id = "SELECT LAST_INSERT_ID() as last_insert_id;"
        mycursor.execute(sql_last_id)
        info_last_id = mycursor.fetchone()
        id_user = info_last_id['last_insert_id']

        session.pop('login', None)
        session.pop('fonction', None)
        session.pop('id_user', None)
        session['login'] = login
        session['fonction'] = 'player'
        session['id_user'] = id_user

        sql_log = '''SELECT idUtilisateur, nomUtilisateur, login, email FROM utilisateur WHERE idUtilisateur=%s;'''
        mycursor.execute(sql_log, (id_user,))
        log = mycursor.fetchone()
        log_add("UTILISATEUR", log)
        
        get_db().commit()

        return redirect('/')

    except Exception as e:
        # Rollback en cas d'erreur
        get_db().rollback()
        print(f"Erreur lors de l'inscription: {e}")
        flash(u"Erreur lors de l'inscription. Veuillez réessayer.", 'alert-danger')
        return redirect('/signup')



@auth_security.route('/logout')
def auth_logout():
    mycursor = get_db().cursor()


    id = session['id_user']

    sql_c = '''UPDATE utilisateur u set u.connected=0 where idUtilisateur=%s;'''
    mycursor.execute(sql_c, (id,))
    session.pop('login', None)
    session.pop('role', None)
    session.pop('id_user', None)
    return redirect('/')


@auth_security.route('/forget-password', methods = ['GET'])
def forget_password():
    return render_template('auth/forget_password.html')
