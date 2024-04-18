#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, abort, flash, session
from werkzeug.security import generate_password_hash

from connection_bdd import get_db

admin_match_pracc = Blueprint('admin_match_pracc', __name__,
                       template_folder = 'templates')


@admin_match_pracc.route('/admin/matchs_pracc_show')
def admin_match_pracc_show():
    mycursor = get_db().cursor()
    id_user = session['id_user']

    sql = '''SELECT * FROM matchs order by date_match,date_ajout;'''
    mycursor.execute(sql)
    matchs = mycursor.fetchall()

    sql = '''SELECT * FROM pracc order by date_pracc,date_ajout;'''
    mycursor.execute(sql)
    pracc = mycursor.fetchall()

    # connecté en tant que
    id_user = session['id_user']
    sql_ps = '''SELECT * FROM utilisateur u 
            join admin a on u.idAdmin = a.idAdmin
            where u.idJoueur=%s;'''
    mycursor.execute(sql_ps, (id_user,))
    adminsession = mycursor.fetchone()

    get_db().commit()
    return render_template('admin/admin_maths_pracc_show.html', matchs = matchs, pracc = pracc, adminsession = adminsession)


############

@admin_match_pracc.route('/admin/match_add', methods = ['GET'])
def admin_match_add():
    mycursor = get_db().cursor()

    # connecté en tant que
    id_user = session['id_user']
    sql_ps = '''SELECT * FROM utilisateur u 
                join admin a on u.idAdmin = a.idAdmin
                where u.idJoueur=%s;'''
    mycursor.execute(sql_ps, (id_user,))
    adminsession = mycursor.fetchone()
    return render_template('admin/admin_matchs_add.html', adminsession = adminsession)


@admin_match_pracc.route('/admin/match_add', methods = ['POST'])
def valid_admin_match_add():
    mycursor = get_db().cursor()
    name = request.form.get('nom', '')
    date = request.form.get('date', '')
    sql = '''INSERT INTO matchs (nomMatch, date_match, date_ajout) VALUES (%s,%s,now())'''
    mycursor.execute(sql, (name, date,))
    get_db().commit()
    return redirect('/admin/matchs_pracc_show')


@admin_match_pracc.route('/admin/match_edit/<id>', methods = ['GET'])
def admin_match_edit(id):
    mycursor = get_db().cursor()

    sql = '''SELECT * FROM matchs where idMatch=%s;'''
    mycursor.execute(sql, (id,))
    match = mycursor.fetchone()
    # connecté en tant que
    id_user = session['id_user']
    sql_ps = '''SELECT * FROM utilisateur u 
                    join admin a on u.idAdmin = a.idAdmin
                    where u.idJoueur=%s;'''
    mycursor.execute(sql_ps, (id_user,))
    adminsession = mycursor.fetchone()
    return render_template('admin/admin_matchs_edit.html', adminsession = adminsession, match = match)


@admin_match_pracc.route('/admin/match_edit', methods = ['POST'])
def valid_admin_match_edit():
    mycursor = get_db().cursor()
    id = request.form.get('id', '')
    name = request.form.get('nom', '')
    date = request.form.get('date', '')
    sql = '''UPDATE matchs set nomMatch=%s, date_match=%s where idMatch=%s;'''
    mycursor.execute(sql, (name, date, id,))
    get_db().commit()
    return redirect('/admin/matchs_pracc_show')


@admin_match_pracc.route('/admin/match_delete/<id>', methods = ['GET'])
def admin_match_delete(id):
    mycursor = get_db().cursor()
    sql = '''DELETE FROM matchs where idMatch=%s;'''
    mycursor.execute(sql, (id,))
    get_db().commit()
    return redirect('/admin/matchs_pracc_show')

@admin_match_pracc.route('/admin/pracc_add',methods = ['GET'])
def admin_pracc_add():
    mycursor = get_db().cursor()

    # connecté en tant que
    id_user = session['id_user']
    sql_ps = '''SELECT * FROM utilisateur u 
                join admin a on u.idAdmin = a.idAdmin
                where u.idJoueur=%s;'''
    mycursor.execute(sql_ps, (id_user,))
    adminsession = mycursor.fetchone()
    return render_template('admin/admin_pracc_add.html', adminsession = adminsession)

@admin_match_pracc.route('/admin/pracc_add',methods = ['POST'])
def valid_admin_pracc_add():
    mycursor = get_db().cursor()
    name = request.form.get('nom', '')
    date = request.form.get('date', '')
    sql = '''INSERT INTO pracc (nomPracc, date_pracc, date_ajout) VALUES (%s,%s,now())'''
    mycursor.execute(sql, (name, date,))
    get_db().commit()
    return redirect('/admin/matchs_pracc_show')

@admin_match_pracc.route('/admin/pracc_edit/<id>', methods = ['GET'])
def admin_pracc_edit(id):
    mycursor = get_db().cursor()

    sql = '''SELECT * FROM pracc where idPracc=%s;'''
    mycursor.execute(sql, (id,))
    pracc = mycursor.fetchone()
    # connecté en tant que
    id_user = session['id_user']
    sql_ps = '''SELECT * FROM utilisateur u 
                    join admin a on u.idAdmin = a.idAdmin
                    where u.idJoueur=%s;'''
    mycursor.execute(sql_ps, (id_user,))
    adminsession = mycursor.fetchone()
    get_db().commit()
    return render_template('admin/admin_pracc_edit.html', adminsession = adminsession, pracc = pracc)


@admin_match_pracc.route('/admin/pracc_edit', methods = ['POST'])
def valid_admin_pracc_edit():
    mycursor = get_db().cursor()
    id = request.form.get('id', '')
    name = request.form.get('nom', '')
    date = request.form.get('date', '')
    sql = '''UPDATE pracc set nomPracc=%s, date_pracc=%s where idPracc=%s;'''
    mycursor.execute(sql, (name, date, id,))
    get_db().commit()
    return redirect('/admin/matchs_pracc_show')


@admin_match_pracc.route('/admin/pracc_delete/<id>', methods = ['GET'])
def admin_pracc_delete(id):
    mycursor = get_db().cursor()
    sql = '''DELETE FROM pracc where idPracc=%s;'''
    mycursor.execute(sql, (id,))
    get_db().commit()
    return redirect('/admin/matchs_pracc_show')