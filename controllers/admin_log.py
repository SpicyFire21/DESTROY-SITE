#! /usr/bin/python
# -*- coding:utf-8 -*-
import os

from flask import session

from connection_bdd import get_db


# fonction de création de log
# prends en paramètre des dictionnaires {'k':'v','k':'v'}
def log_add_api(type, obj):
    mycursor = get_db().cursor()
    id_admin = 1
    liste = [str(obj[key]) for key in obj.keys()]
    list_add = ' | '.join(liste)
    sql_log = '''INSERT INTO log (idAdmin, typeaction, oldaction, newaction, date) VALUES (%s,%s,%s,%s,now())'''
    mycursor.execute(sql_log, (id_admin, type, list_add, "AJOUTÉ"))
    limit_log()
    get_db().commit()



def log_add(type, obj):
    mycursor = get_db().cursor()
    id_admin = session['id_admin']
    liste = [str(obj[key]) for key in obj.keys()]
    list_add = ' | '.join(liste)
    sql_log = '''INSERT INTO log (idAdmin, typeaction, oldaction, newaction, date) VALUES (%s,%s,%s,%s,now())'''
    mycursor.execute(sql_log, (id_admin, type, list_add, "AJOUTÉ"))
    limit_log()
    get_db().commit()

def log_delete(type, obj):
    mycursor = get_db().cursor()

    id_admin = session['id_admin']
    liste = [str(obj[key]) for key in obj.keys()]
    list_del = ' | '.join(liste)
    sql_log = '''INSERT INTO log (idAdmin, typeaction, oldaction, newaction, date) VALUES (%s,%s,%s,%s,now())'''
    mycursor.execute(sql_log, (id_admin, type, list_del, "SUPPRIMÉ"))
    limit_log()
    get_db().commit()


def log_edit(type, before, after):
    try:
        mycursor = get_db().cursor()
        id_admin = session['id_admin']
        newState = False
        before_list = []
        after_list = []

        for key in before.keys() & after.keys():
            if before[key] != after[key]:
                newState = True
                if key != 'mdp' and key != 'titulaire':
                    before_list.append(str(before[key]))
                    after_list.append(str(after[key]))
                elif key == 'titulaire':

                    if before[key] == 1:
                        oldtitu = "Titulaire"
                    else:
                        oldtitu = "Bench"

                    if after[key] == 1:
                        newtitu = "Titulaire"
                    else:
                        newtitu = "Bench"

                    before_list.append(str(oldtitu))
                    after_list.append(str(newtitu))
                elif key == 'mdp':
                    before_list.append("MOT DE PASSE RESET !")
                    after_list.append("MOT DE PASSE MODIFIÉ !")

        oldaction = ' | '.join(before_list)
        newaction = ' | '.join(after_list)

        if newState:
            sql_log = '''INSERT INTO log (idAdmin, typeaction, oldaction, newaction, date)
                         VALUES (%s, %s, %s, %s, NOW());'''
            mycursor.execute(sql_log, (id_admin, type, oldaction, newaction))

        limit_log()
        get_db().commit()
    except Exception as e:
        get_db().rollback()
        print(f"Erreur lors de l'enregistrement du log : {e}")



# supprimer les logs de la bdd et les écrire dans un fichier
def limit_log():
    mycursor = get_db().cursor()

    sql_log = '''SELECT idlog from log order by date Desc limit 200;'''
    mycursor.execute(sql_log)
    logs = mycursor.fetchall()

    sql_print = '''SELECT * from log order by date asc limit 1;'''
    mycursor.execute(sql_print)
    printed = mycursor.fetchone()
    contenu = f'''{printed}'''

    directory = 'log-scripted'
    filename = 'logs_saved.txt'
    full_path = os.path.join(directory, filename)

    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(full_path, 'a', encoding='utf-8') as file:
        file.write(contenu + '\n'+ '\n')
    print("WRITED")



    list_logs = [(log['idlog'],) for log in logs]
    sql_log_saved = '''update log set saved=1 where idlog=%s;'''
    mycursor.executemany(sql_log_saved, list_logs)

    sql_log_del = '''DELETE FROM log where saved=0;'''
    mycursor.execute(sql_log_del)

    sql_logs = '''update log set saved=0 where idlog!=%s;'''
    mycursor.executemany(sql_logs, list_logs)
    get_db().commit()

