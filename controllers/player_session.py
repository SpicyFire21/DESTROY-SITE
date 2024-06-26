from flask import session

from connection_bdd import get_db


def player_session():
    mycursor = get_db().cursor()
    id = session['id_player']
    sql_ps = '''SELECT j.idJoueur, j.pseudo,u.imgProfile FROM utilisateur u
    join joueurs j on u.idJoueur = j.idJoueur
    where j.idJoueur=%s;'''
    mycursor.execute(sql_ps, (id,))
    playersession = mycursor.fetchone()
    get_db().commit()
    return playersession



