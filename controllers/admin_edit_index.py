#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, abort, flash, session
import pymysql
import requests

from connection_bdd import get_db

admin_edit_index = Blueprint('admin_edit_index', __name__,
                             template_folder = 'templates')


@admin_edit_index.route('/admin/index/edit')
def admin_edit_index_show():
    mycursor = get_db().cursor()

    sql_discord = '''SELECT * FROM indexDiscord order by idindexDiscord;'''
    mycursor.execute(sql_discord)
    discord = mycursor.fetchall()

    sql_patch = '''SELECT * FROM indexPatch order by idindexPatch;'''
    mycursor.execute(sql_patch)
    patch = mycursor.fetchall()

    # connecté en tant que
    id_user = session['id_user']
    sql_ps = '''SELECT * FROM utilisateur u 
               join admin a on u.idAdmin = a.idAdmin
               where u.idJoueur=%s;'''
    mycursor.execute(sql_ps, (id_user,))
    adminsession = mycursor.fetchone()
    auto_del()
    get_db().commit()
    return render_template('admin/admin_edit_index.html', adminsession = adminsession, discord = discord, patch = patch)


# @admin_edit_index.route('/admin/player-index-discord/add')
# def admin_add_discord():
#     id_user = session['id_user']
#     mycursor = get_db().cursor()
#     sql_admin = '''select nomAdmin from admin where idAdmin=%s;'''
#     mycursor.execute(sql_admin, (id_user,))
#     nom = mycursor.fetchone()
#     sql_ds = '''insert into indexdiscord (nomAdmin, date) VALUES (%s,now());'''
#     mycursor.execute(sql_ds, (nom['nomAdmin'],))
#     get_db().commit()
#     return redirect('/admin/index/edit')
#
#
# @admin_edit_index.route('/admin/player-index-patch/add')
# def admin_add_patch():
#     id_user = session['id_user']
#     mycursor = get_db().cursor()
#     sql_admin = '''select nomAdmin from admin where idAdmin=%s;'''
#     mycursor.execute(sql_admin, (id_user,))
#     nom = mycursor.fetchone()
#     sql_ds = '''insert into indexpatch (nomAdmin, date) VALUES (%s,now());'''
#     mycursor.execute(sql_ds, (nom['nomAdmin'],))
#     get_db().commit()
#     return redirect('/admin/index/edit')


@admin_edit_index.route('/admin/player-index-discord/delete/<id>')
def admin_delete_discord(id):
    id_user = session['id_user']
    mycursor = get_db().cursor()
    sql = '''delete from indexdiscord where idindexDiscord=%s;'''
    mycursor.execute(sql, (id,))
    get_db().commit()
    return redirect('/admin/index/edit')


@admin_edit_index.route('/admin/player-index-patch/delete/<id>')
def admin_delete_patch(id):
    id_user = session['id_user']  # pour les logs admins
    mycursor = get_db().cursor()
    sql = '''delete from indexpatch where idindexPatch=%s;'''
    mycursor.execute(sql, (id,))
    get_db().commit()
    return redirect('/admin/index/edit')


@admin_edit_index.route('/admin/player-index/valid', methods = ['POST'])
def admin_valid_newindex():
    id_user = session['id_user']
    mycursor = get_db().cursor()
    id_user = session['id_user']
    sql_admin = '''SELECT nomAdmin From admin where idAdmin=%s;'''
    mycursor.execute(sql_admin, (id_user,))
    Admin = mycursor.fetchone()
    nomAdmin = Admin['nomAdmin']
    print(nomAdmin)
    discord_upd = []
    patch_upd = []
    discord_add = []
    patch_add = []

    for key, value in request.form.items():
        if key.startswith('discord_'):
            discord_id = key.split('discord_')[1]
            discord_upd.append({'id': discord_id, 'content': value})
        elif key.startswith('patch_'):
            patch_id = key.split('patch_')[1]
            patch_upd.append({'id': patch_id, 'content': value})
        elif key.startswith('newDiscord'):

            discord_add.append({'nomAdmin': nomAdmin, 'content': value})
        elif key.startswith('newPatch'):

            patch_add.append({'nomAdmin': nomAdmin, 'content': value})

    # Traitement des données
    print("Discord upd:", discord_upd)
    print("Patch upd:", patch_upd)
    print("Discord add:", discord_add)
    print("Patch add:", patch_add)

    if discord_add:
        sql_insert_ds = '''INSERT INTO indexdiscord (nomAdmin, contenu, date) VALUES (%s,%s,NOW());'''
        values_ds = [(item['nomAdmin'], item['content']) for item in discord_add]
        print(values_ds)
        mycursor.executemany(sql_insert_ds, values_ds)
    if patch_add:
        sql_insert_pat = '''INSERT INTO indexpatch (nomAdmin, contenu, date) VALUES (%s,%s,NOW());'''
        values_pat = [(item['nomAdmin'], item['content']) for item in patch_add]
        print(values_pat)
        mycursor.executemany(sql_insert_pat, values_pat)

    auto_del()

    get_db().commit()
    return redirect('/admin/index/edit')


def auto_del():
    mycursor = get_db().cursor()
    sql_del_ds = '''DELETE FROM indexdiscord WHERE TRIM(contenu) = '' AND contenu IS NOT NULL;'''
    sql_del_pat = '''DELETE FROM indexpatch WHERE TRIM(contenu) = '' AND contenu IS NOT NULL;'''
    mycursor.execute(sql_del_ds)
    mycursor.execute(sql_del_pat)
    get_db().commit()
    return "deleted"



@admin_edit_index.route('/admin/player-index-discord/deleteall')
def deleteall_discord():
    mycursor = get_db().cursor()
    sql = '''DELETE FROM indexdiscord'''
    mycursor.execute(sql)
    get_db().commit()
    return redirect('/admin/index/edit')

@admin_edit_index.route('/admin/player-index-patch/deleteall')
def deleteall_patch():
    mycursor = get_db().cursor()
    sql = '''DELETE FROM indexpatch'''
    mycursor.execute(sql)
    get_db().commit()
    return redirect('/admin/index/edit')