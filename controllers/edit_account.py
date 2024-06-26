#! /usr/bin/python
# -*- coding:utf-8 -*-

from flask import Blueprint
from flask import Flask, request, render_template, redirect, flash, session
from werkzeug.security import generate_password_hash, check_password_hash

from connection_bdd import get_db
from controllers.admin_session import admin_session
from controllers.player_session import player_session
from controllers.visitor_session import visitor_session
import io
from flask import Blueprint
from flask import Flask, render_template, request, redirect, url_for, send_file
from werkzeug.utils import secure_filename

from connection_bdd import get_db
from controllers.admin_session import admin_session


edit_account = Blueprint('edit_account', __name__,
                         template_folder = 'templates')


@edit_account.route('/editaccount', methods = ['GET'])
def editaccount():
    if session['fonction'] == 'ADMIN':
        return redirect('/editaccount/admin')
    elif session['fonction'] == 'PLAYER':
        return redirect('/editaccount/player')
    else:
        return redirect('/editaccount/visitor')


@edit_account.route('/editaccount/player', methods = ['POST'])
def valid_player_account():
    mycursor = get_db().cursor()
    id = request.form.get('id')
    pseudo = request.form.get('pseudo', '')
    email = request.form.get('email', '')
    mdp = request.form.get('mdp', '')
    file = request.files['file']
    if file:
        print("img")
        imageBlob = file.read()
        print(imageBlob)
    else:
        print("no img")
        imageBlob = None

    mdp = generate_password_hash(mdp, method = 'pbkdf2:sha256')
    values = (pseudo, email, mdp, imageBlob, id,)
    sql = '''UPDATE utilisateur u
    JOIN joueurs j ON u.idJoueur = j.idJoueur
    set pseudo=%s,email=%s,mdp=%s,u.imgProfile=%s WHERE u.idJoueur=%s'''
    mycursor.execute(sql, values)
    get_db().commit()
    return redirect('/player/index')

###############################

@edit_account.route('/editaccount/visitor',methods = ['GET'])
def edit_visitor():
    mycursor = get_db().cursor()
    id_user = session['id_user']
    sql_u = '''SELECT * FROM utilisateur u WHERE u.idUtilisateur =%s;'''
    mycursor.execute(sql_u, (id_user,))
    visitor = mycursor.fetchone()
    visitorsession = visitor_session()
    get_db().commit()
    return render_template('visitor/visitor_profile.html',visitor=visitor,visitorsession=visitorsession)

@edit_account.route('/editaccount/player',methods = ['GET'])
def edit_player():
    mycursor = get_db().cursor()
    id_user = session['id_player']
    sql_u = '''SELECT * FROM utilisateur u 
    join joueurs j on u.idJoueur = j.idJoueur
    WHERE u.idUtilisateur =%s;'''
    mycursor.execute(sql_u, (id_user,))
    player = mycursor.fetchone()
    playersession = player_session()
    get_db().commit()
    return render_template('player/player_profile.html',player=player,playersession=playersession)

@edit_account.route('/editaccount/admin',methods = ['GET'])
def edit_admin():
    mycursor = get_db().cursor()
    id_user = session['id_admin']
    sql_u = '''SELECT * FROM utilisateur u 
    join `bdd-player`.admin a on u.idAdmin = a.idAdmin
    WHERE u.idUtilisateur =%s;'''
    mycursor.execute(sql_u, (id_user,))
    admin = mycursor.fetchone()
    adminsession = admin_session()
    get_db().commit()
    return render_template('admin/admin_profile.html',admin=admin,adminsession=adminsession)


######################################################

@edit_account.route('/images/<int:id>')
def image(id):
    mycursor = get_db().cursor()
    mycursor.execute("SELECT imgProfile FROM utilisateur WHERE idUtilisateur = %s", (id,))
    image_data = mycursor.fetchone()


    if image_data:
        image_blob = image_data['imgProfile']
        return send_file(io.BytesIO(image_blob), mimetype='image/jpeg')
    else:
        return "Image not found", 404
