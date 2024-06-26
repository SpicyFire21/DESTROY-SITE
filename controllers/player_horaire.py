#! /usr/bin/python
# -*- coding:utf-8 -*-

from flask import Blueprint
from flask import Flask, request, render_template, redirect, flash, session
from werkzeug.security import generate_password_hash, check_password_hash

from connection_bdd import get_db
from controllers.player_session import player_session

player_horaire = Blueprint('player_horaire', __name__,
                           template_folder = 'templates')


@player_horaire.route('/horaire/show')
def player_horaire_show():
    mycursor = get_db().cursor()
    id_user = session['id_user']

    sql_jour = '''SELECT * FROM jour;'''
    mycursor.execute(sql_jour)
    jours = mycursor.fetchall()
    sql_heure = '''SELECT * FROM heure;'''
    mycursor.execute(sql_heure)
    heures = mycursor.fetchall()

    sql_horaire = '''SELECT * FROM horaire where idJoueur =%s;'''
    mycursor.execute(sql_horaire, (id_user,))
    horaires = mycursor.fetchall()

    sql_player = '''SELECT * FROM joueurs where titulaire=1;'''
    mycursor.execute(sql_player)
    players = mycursor.fetchall()

    playersession = player_session()
    return render_template('player/player_horaire.html',
                           playersession = playersession,
                           jours = jours,
                           heures = heures,
                           horaires = horaires,
                           players = players)


@player_horaire.route('/horaire/fetch', methods=['POST'])
def player_horaire_fetch():
    mycursor = get_db().cursor()
    id_user = session['id_user']
    data = request.json

    try:
        get_db().begin()

        sql_select_all = '''SELECT * FROM horaire WHERE idJoueur=%s;'''
        mycursor.execute(sql_select_all, (id_user,))
        allHoraire = mycursor.fetchall()

        for horaire in allHoraire:
            heure = int(horaire['idHeure'])
            jour = int(horaire['idJour'])
            frontend_exists = False

            for itemdata in data:
                col = int(itemdata['col'])
                row = int(itemdata['row'])
                if row == heure and col == jour:
                    frontend_exists = True
                    break

            if not frontend_exists:
                sql_delete = '''DELETE FROM horaire WHERE idJoueur=%s AND idHeure=%s AND idJour=%s;'''
                mycursor.execute(sql_delete, (id_user, heure, jour))

        for itemdata in data:
            col = int(itemdata['col'])
            row = int(itemdata['row'])
            bdd_exists = False

            for horaire in allHoraire:
                heure = int(horaire['idHeure'])
                jour = int(horaire['idJour'])
                if row == heure and col == jour:
                    bdd_exists = True
                    break

            if not bdd_exists:
                sql_insert = '''INSERT INTO horaire (idJoueur, idHeure, idJour) VALUES (%s, %s, %s);'''
                mycursor.execute(sql_insert, (id_user, row, col))

        get_db().commit()
    except Exception as e:
        get_db().rollback()
        flash(f"Erreur lors de la mise à jour des horaires : {e}", 'error')
        return redirect('/error_page')

    return redirect('/horaire/show')



@player_horaire.route('/horaire/reset', methods = ['POST'])
def player_horaire_reset():
    mycursor = get_db().cursor()
    id_user = session['id_user']
    sql_delete = '''DELETE FROM horaire where idJoueur=%s;'''
    mycursor.execute(sql_delete, (id_user,))
    return redirect('/horaire/show')
