#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import session

from connection_bdd import get_db


# fonction de création de log
# prends en paramètre des dictionnaires {'k':'v','k':'v'}

def log_add(type, obj):
    mycursor = get_db().cursor()
    id_admin = session['id_user']
    liste = [str(obj[key]) for key in obj.keys()]
    list_add = ' | '.join(liste)
    sql_log = '''INSERT INTO log (idAdmin, typeaction, oldaction, newaction, date) VALUES (%s,%s,%s,%s,now())'''
    mycursor.execute(sql_log, (id_admin, type, list_add, "AJOUTÉ"))
    limit_log()
    get_db().commit()

def log_delete(type, obj):
    mycursor = get_db().cursor()
    id_admin = session['id_user']
    liste = [str(obj[key]) for key in obj.keys()]
    list_del = ' | '.join(liste)
    sql_log = '''INSERT INTO log (idAdmin, typeaction, oldaction, newaction, date) VALUES (%s,%s,%s,%s,now())'''
    mycursor.execute(sql_log, (id_admin, type, list_del, "SUPPRIMÉ"))
    limit_log()
    get_db().commit()


def log_edit(type, before, after):
    mycursor = get_db().cursor()
    id_admin = session['id_user']
    newState = False
    before_list = []
    after_list = []

    for key in before.keys() & after.keys():
        if before[key] != after[key]:
            newState = True
            if key != 'mdp':

                before_list.append(str(before[key]))
                after_list.append(str(after[key]))
            elif before[key] != after[key]:
                before_list.append(str("MOT DE PASSE RESET !"))
                after_list.append(str("MOT DE PASSE MODIFIÉ !"))
    oldaction = ' | '.join(before_list)
    newaction = ' | '.join(after_list)

    if newState:
        sql_log = '''INSERT INTO log (idAdmin, typeaction, oldaction, newaction, date)
                 VALUES (%s, %s, %s, %s, NOW());'''
        mycursor.execute(sql_log, (id_admin, type, oldaction, newaction))

    limit_log()
    get_db().commit()



def limit_log():
    mycursor = get_db().cursor()

    sql_log = '''SELECT idlog from log order by date Desc limit 200;'''
    mycursor.execute(sql_log)
    logs = mycursor.fetchall()

    list_logs = [(log['idlog'],) for log in logs]
    sql_log_saved = '''update log set saved=1 where idlog=%s;'''
    mycursor.executemany(sql_log_saved, list_logs)

    sql_log_del = '''DELETE FROM log where saved=0;'''
    mycursor.execute(sql_log_del)

    sql_logs = '''update log set saved=0 where idlog!=%s;'''
    mycursor.executemany(sql_logs, list_logs)
    get_db().commit()

