from flask import session

from connection_bdd import get_db


def admin_session():
    mycursor = get_db().cursor()
    id_user = session['id_admin']
    sql_ps = '''SELECT a.idAdmin, a.nomAdmin,u.imgProfile FROM utilisateur u 
    join admin a on u.idAdmin = a.idAdmin
    where a.idAdmin=%s;'''
    mycursor.execute(sql_ps, (id_user,))
    adminsession = mycursor.fetchone()
    get_db().commit()
    return adminsession
