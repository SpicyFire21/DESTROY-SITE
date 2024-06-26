from flask import session

from connection_bdd import get_db


def visitor_session():
    mycursor = get_db().cursor()
    id = session['id_user']
    sql_ps = '''SELECT idUtilisateur,nomUtilisateur,imgProfile FROM utilisateur where idUtilisateur=%s;'''
    mycursor.execute(sql_ps, (id,))
    visitorsession = mycursor.fetchone()
    get_db().commit()
    return visitorsession
