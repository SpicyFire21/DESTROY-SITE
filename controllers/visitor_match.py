#! /usr/bin/python
# -*- coding:utf-8 -*-

from flask import Blueprint
from flask import Flask, request, render_template, redirect, flash, session
from werkzeug.security import generate_password_hash, check_password_hash

from connection_bdd import get_db

visitor_match = Blueprint('visitor_match', __name__,
                          template_folder = 'templates')


@visitor_match.route('/visitor/match_show')
def visitor_match_show():
    mycursor = get_db().cursor()
    sql = '''SELECT * FROM matchs order by date_match,date_ajout;'''
    mycursor.execute(sql)
    matchs = mycursor.fetchall()


    sql = '''SELECT * FROM pracc order by date_pracc,date_ajout;'''
    mycursor.execute(sql)
    pracc = mycursor.fetchall()

    # connecté en tant que
    id_user = session['id_user']
    sql_ps = '''SELECT * FROM utilisateur u
            where u.idUtilisateur=%s;'''
    mycursor.execute(sql_ps, (id_user,))
    visitorsession = mycursor.fetchone()
    get_db().commit()
    return render_template('visitor/visitor_matchs_pracc_show.html',
                           matchs = matchs,
                           visitorsession = visitorsession,
                           pracc = pracc)


# @visitor_match.route('/visitor/match_add', methods = ['GET'])
# def visitor_match_add():
#     mycursor = get_db().cursor()
#
#     # connecté en tant que
#     id_user = session['id_user']
#     sql_ps = '''SELECT * FROM utilisateur u
#                 where u.idUtilisateur=%s;'''
#     mycursor.execute(sql_ps, (id_user,))
#     visitorsession = mycursor.fetchone()
#     get_db().commit()
#     return render_template('visitor/visitor_matchs_add.html', visitorsession = visitorsession)
#
#
# @visitor_match.route('/visitor/match_add', methods = ['POST'])
# def valid_visitor_match_add():
#     mycursor = get_db().cursor()
#     name = request.form.get('nom', '')
#     date = request.form.get('date', '')
#     sql = '''INSERT INTO matchs (nomMatch, date_match, date_ajout) VALUES (%s,%s,now())'''
#     mycursor.execute(sql, (name, date,))
#     get_db().commit()
#     return redirect('/visitor/match_show')

#
# @visitor_match.route('/visitor/match_edit/<id>', methods = ['GET'])
# def visitor_match_edit(id):
#     mycursor = get_db().cursor()
#
#     sql = '''SELECT * FROM matchs where idMatch=%s;'''
#     mycursor.execute(sql, (id,))
#     match = mycursor.fetchone()
#     # connecté en tant que
#     id_user = session['id_user']
#     sql_ps = '''SELECT * FROM utilisateur u
#                 where u.idUtilisateur=%s;'''
#     mycursor.execute(sql_ps, (id_user,))
#     visitorsession = mycursor.fetchone()
#     get_db().commit()
#     return render_template('visitor/visitor_matchs_edit.html', visitorsession = visitorsession, match = match)
#
#
# @visitor_match.route('/visitor/match_edit', methods = ['POST'])
# def valid_visitor_match_edit():
#     mycursor = get_db().cursor()
#     id = request.form.get('id', '')
#     name = request.form.get('nom', '')
#     date = request.form.get('date', '')
#     sql = '''UPDATE matchs set nomMatch=%s, date_match=%s where idMatch=%s;'''
#     mycursor.execute(sql, (name, date, id,))
#     get_db().commit()
#     return redirect('/visitor/match_show')
#
#
# @visitor_match.route('/visitor/match_delete/<id>', methods = ['GET'])
# def visitor_match_delete(id):
#     mycursor = get_db().cursor()
#     sql = '''DELETE FROM matchs where idMatch=%s;'''
#     mycursor.execute(sql, (id,))
#     get_db().commit()
#     return redirect('/visitor/match_show')
#
# @visitor_match.route('/visitor/pracc_edit/<id>', methods = ['GET'])
# def visitor_pracc_edit(id):
#     mycursor = get_db().cursor()
#
#     sql = '''SELECT * FROM pracc where idPracc=%s;'''
#     mycursor.execute(sql, (id,))
#     pracc = mycursor.fetchone()
#     # connecté en tant que
#     id_user = session['id_user']
#     sql_ps = '''SELECT * FROM utilisateur u
#                 where u.idUtilisateur=%s;'''
#     mycursor.execute(sql_ps, (id_user,))
#     visitorsession = mycursor.fetchone()
#     get_db().commit()
#     return render_template('visitor/visitor_pracc_edit.html', visitorsession = visitorsession, pracc = pracc)
#
#
# @visitor_match.route('/visitor/pracc_edit', methods = ['POST'])
# def valid_visitor_pracc_edit():
#     mycursor = get_db().cursor()
#     id = request.form.get('id', '')
#     name = request.form.get('nom', '')
#     date = request.form.get('date', '')
#     sql = '''UPDATE pracc set nomPracc=%s, date_pracc=%s where idPracc=%s;'''
#     mycursor.execute(sql, (name, date, id,))
#     get_db().commit()
#     return redirect('/visitor/match_show')
#
#
# @visitor_match.route('/visitor/pracc_delete/<id>', methods = ['GET'])
# def visitor_pracc_delete(id):
#     mycursor = get_db().cursor()
#     sql = '''DELETE FROM pracc where idPracc=%s;'''
#     mycursor.execute(sql, (id,))
#     get_db().commit()
#     return redirect('/visitor/match_show')
