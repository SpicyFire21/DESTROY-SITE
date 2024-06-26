#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, abort, flash, session
from werkzeug.security import generate_password_hash

from connection_bdd import get_db
from controllers.admin_log import log_add, log_edit, log_delete
from controllers.admin_session import admin_session

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

    adminsession = admin_session()

    get_db().commit()
    return render_template('admin/admin_maths_pracc_show.html', matchs = matchs, pracc = pracc,
                           adminsession = adminsession)


############

@admin_match_pracc.route('/admin/match_add', methods = ['GET'])
def admin_match_add():
    mycursor = get_db().cursor()

    adminsession = admin_session()
    return render_template('admin/admin_matchs_add.html', adminsession = adminsession)


@admin_match_pracc.route('/admin/match_add', methods = ['POST'])
def valid_admin_match_add():
    mycursor = get_db().cursor()
    try:
        get_db().begin()
        name = request.form.get('nom', '').strip()
        date = request.form.get('date', '').strip()

        if not name or not date:
            flash('Le nom et la date sont obligatoires.', 'deleted')
            return redirect('/admin/matchs_pracc_show')

        sql_insert = '''INSERT INTO matchs (nomMatch, date_match, date_ajout) VALUES (%s, %s, NOW())'''
        mycursor.execute(sql_insert, (name, date,))

        sql_select = '''SELECT * FROM matchs WHERE nomMatch=%s AND date_match=%s ORDER BY idMatch DESC LIMIT 1'''
        mycursor.execute(sql_select, (name, date,))
        log = mycursor.fetchone()

        log_add("MATCH", log)

        get_db().commit()
        flash('Match ajoutée !', 'add')
    except Exception as e:
        get_db().rollback()
        print(f"Erreur lors de l'ajout de la Match : {e}")
        flash(f"Erreur lors de l'ajout de la Match : {e}", 'deleted')

    return redirect('/admin/matchs_pracc_show')


@admin_match_pracc.route('/admin/match_edit/<id>', methods = ['GET'])
def admin_match_edit(id):
    mycursor = get_db().cursor()

    sql = '''SELECT * FROM matchs where idMatch=%s;'''
    mycursor.execute(sql, (id,))
    match = mycursor.fetchone()
    adminsession = admin_session()
    return render_template('admin/admin_matchs_edit.html', adminsession = adminsession, match = match)


@admin_match_pracc.route('/admin/match_edit', methods = ['POST'])
def valid_admin_match_edit():
    mycursor = get_db().cursor()
    global ee
    try:
        get_db().begin()
        id = request.form.get('id', '')
        name = request.form.get('nom', '')
        date = request.form.get('date', '')

        sql_old = ''' select * from matchs where idMatch=%s;'''
        mycursor.execute(sql_old, (id,))
        old = mycursor.fetchone()
        sql = '''UPDATE matchs set nomMatch=%s, date_match=%s where idMatch=%s;'''
        mycursor.execute(sql, (name, date, id,))

        sql_new = ''' select * from matchs where idMatch=%s;'''
        mycursor.execute(sql_new, (id,))
        new = mycursor.fetchone()
        log_edit("MATCH", old, new)
        get_db().commit()
        if old != new:
            message = "Match modifiée"
            flash(message, 'add')
    except Exception as ee:

        get_db().rollback()
        print("Erreur lors de la modification du Match")
        message = f"Erreur lors de la modification du Match - {ee}"
        flash(message, 'deleted')
    return redirect('/admin/matchs_pracc_show')


@admin_match_pracc.route('/admin/match_delete/<id>', methods = ['GET'])
def admin_match_delete(id):
    mycursor = get_db().cursor()
    try:
        get_db().begin()
        sql_select = '''SELECT * FROM matchs WHERE idMatch = %s;'''
        mycursor.execute(sql_select, (id,))
        log = mycursor.fetchone()

        sql_delete = '''DELETE FROM matchs WHERE idMatch = %s;'''
        mycursor.execute(sql_delete, (id,))

        log_delete("MATCH", log)

        get_db().commit()
        print("Suppression de la Match !")
        message = "Match supprimée !"
        flash(message, 'add')
    except Exception as e:
        get_db().rollback()
        print(f"Erreur lors de la suppression du Match - {e}")
        message = f"Erreur lors de la suppression du Match - {e}"
        flash(message, 'deleted')

    return redirect('/admin/matchs_pracc_show')


@admin_match_pracc.route('/admin/pracc_add', methods = ['GET'])
def admin_pracc_add():
    mycursor = get_db().cursor()

    adminsession = admin_session()
    return render_template('admin/admin_pracc_add.html', adminsession = adminsession)


@admin_match_pracc.route('/admin/pracc_add', methods = ['POST'])
def valid_admin_pracc_add():
    mycursor = get_db().cursor()
    try:
        get_db().begin()
        name = request.form.get('nom', '').strip()
        date = request.form.get('date', '').strip()

        if not name or not date:
            flash('Le nom et la date sont obligatoires.', 'deleted')
            return redirect('/admin/matchs_pracc_show')

        sql_insert = '''INSERT INTO pracc (nomPracc, date_pracc, date_ajout) VALUES (%s, %s, NOW())'''
        mycursor.execute(sql_insert, (name, date,))

        sql_select = '''SELECT * FROM pracc WHERE nomPracc=%s AND date_pracc=%s ORDER BY idPracc DESC LIMIT 1'''
        mycursor.execute(sql_select, (name, date,))
        log = mycursor.fetchone()

        log_add("PRACC", log)

        get_db().commit()
        flash('Pracc ajoutée !', 'add')
    except Exception as e:
        get_db().rollback()
        print(f"Erreur lors de l'ajout de la Pracc : {e}")
        flash(f"Erreur lors de l'ajout de la Pracc : {e}", 'deleted')

    return redirect('/admin/matchs_pracc_show')


@admin_match_pracc.route('/admin/pracc_edit/<id>', methods = ['GET'])
def admin_pracc_edit(id):
    mycursor = get_db().cursor()

    sql = '''SELECT * FROM pracc where idPracc=%s;'''
    mycursor.execute(sql, (id,))
    pracc = mycursor.fetchone()
    adminsession = admin_session()
    get_db().commit()
    return render_template('admin/admin_pracc_edit.html', adminsession = adminsession, pracc = pracc)


@admin_match_pracc.route('/admin/pracc_edit', methods = ['POST'])
def valid_admin_pracc_edit():
    mycursor = get_db().cursor()
    global ee
    try:
        get_db().begin()
        id = request.form.get('id', '')
        name = request.form.get('nom', '')
        date = request.form.get('date', '')

        sql_old = ''' select * from pracc where idPracc=%s;'''
        mycursor.execute(sql_old,(id,))
        old = mycursor.fetchone()
        sql = '''UPDATE pracc set nomPracc=%s, date_pracc=%s where idPracc=%s;'''
        mycursor.execute(sql, (name, date, id,))

        sql_new = ''' select * from pracc where idPracc=%s;'''
        mycursor.execute(sql_new, (id,))
        new = mycursor.fetchone()
        log_edit("PRACC", old, new)
        get_db().commit()
        if old != new:
            message = "Pracc modifiée avec succès"
            flash(message, 'add')
    except Exception as ee:

        get_db().rollback()
        print("Erreur lors de la modification de la Pracc")
        message = f"Erreur lors de la modification de la Pracc - {ee}"
        flash(message, 'deleted')
    return redirect('/admin/matchs_pracc_show')


@admin_match_pracc.route('/admin/pracc_delete/<id>', methods = ['GET'])
def admin_pracc_delete(id):
    mycursor = get_db().cursor()
    try:
        sql_select = '''SELECT * FROM pracc WHERE idPracc = %s;'''
        mycursor.execute(sql_select, (id,))
        log = mycursor.fetchone()

        sql_delete = '''DELETE FROM pracc WHERE idPracc = %s;'''
        mycursor.execute(sql_delete, (id,))

        log_delete("PRACC", log)

        get_db().commit()
        print("Suppression de la Pracc !")
        message = "Pracc supprimée avec !"
        flash(message, 'add')
    except Exception as e:
        get_db().rollback()
        print(f"Erreur lors de la suppression de la Pracc - {e}")
        message = f"Erreur lors de la suppression de la Pracc - {e}"
        flash(message, 'deleted')

    return redirect('/admin/matchs_pracc_show')

