#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, abort, flash, session
import pymysql
import requests

from connection_bdd import get_db
from controllers.admin_session import admin_session

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

    adminsession = admin_session()
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
    id_admin = session['id_admin']
    mycursor = get_db().cursor()
    sql = '''delete from indexdiscord where idindexDiscord=%s;'''
    mycursor.execute(sql, (id,))
    get_db().commit()
    return redirect('/admin/index/edit')


@admin_edit_index.route('/admin/player-index-patch/delete/<id>')
def admin_delete_patch(id):
    id_admin = session['id_admin']  # pour les logs admins
    mycursor = get_db().cursor()
    sql = '''delete from indexpatch where idindexPatch=%s;'''
    mycursor.execute(sql, (id,))
    get_db().commit()
    return redirect('/admin/index/edit')


@admin_edit_index.route('/admin/player-index/valid', methods=['POST'])
def admin_valid_newindex():
    mycursor = get_db().cursor()
    try:
        id_admin = session['id_user']
        get_db().begin()
        sql_admin = '''SELECT nomAdmin FROM admin WHERE idAdmin=%s;'''
        mycursor.execute(sql_admin, (id_admin,))
        Admin = mycursor.fetchone()
        if not Admin:
            flash('Admin non trouvé', 'delete')
            return redirect('/admin/index/edit')
        nomAdmin = Admin['nomAdmin']

        discord_upd, patch_upd, discord_add, patch_add = [], [], [], []

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

        if discord_add:
            sql_insert_ds = '''INSERT INTO indexdiscord (nomAdmin, contenu, date) VALUES (%s, %s, NOW());'''
            values_ds = [(item['nomAdmin'], item['content']) for item in discord_add]
            mycursor.executemany(sql_insert_ds, values_ds)

        if patch_add:
            sql_insert_pat = '''INSERT INTO indexpatch (nomAdmin, contenu, date) VALUES (%s, %s, NOW());'''
            values_pat = [(item['nomAdmin'], item['content']) for item in patch_add]
            mycursor.executemany(sql_insert_pat, values_pat)

        if discord_upd:
            sql_update_ds = '''UPDATE indexdiscord SET contenu=%s, date=NOW() WHERE idindexDiscord=%s;'''
            for item in discord_upd:
                mycursor.execute(sql_update_ds, (item['content'], item['id']))

        if patch_upd:
            sql_update_pat = '''UPDATE indexpatch SET contenu=%s, date=NOW() WHERE idindexPatch=%s;'''
            for item in patch_upd:
                mycursor.execute(sql_update_pat, (item['content'], item['id']))
        auto_del()
        get_db().commit()
        flash('Index mis à jour avec succès', 'edited')
    except Exception as e:
        get_db().rollback()
        flash(f"Erreur lors de la mise à jour de l'index: {e}", 'delete')

    return redirect('/admin/index/edit')



def auto_del():
    mycursor = get_db().cursor()
    try:

        sql_del_ds = '''DELETE FROM indexdiscord WHERE TRIM(contenu) = '' AND contenu IS NOT NULL;'''
        sql_del_pat = '''DELETE FROM indexpatch WHERE TRIM(contenu) = '' AND contenu IS NOT NULL;'''

        mycursor.execute(sql_del_ds)
        mycursor.execute(sql_del_pat)

        get_db().commit()
    except Exception as e:
        get_db().rollback()
        print(f"Erreur lors de la suppression automatique des entrées vides: {e}")
    finally:
        mycursor.close()




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