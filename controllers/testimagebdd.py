import io
from flask import Blueprint
from flask import Flask, render_template, request, redirect, url_for, send_file
from werkzeug.utils import secure_filename

from connection_bdd import get_db
from controllers.admin_session import admin_session

testimagebdd = Blueprint('testimagebdd', __name__,
                         template_folder = 'templates')


# récupérer les images depuis leur id en bdd pour les afficher
@testimagebdd.route('/images/<int:file_id>')
def image(file_id):
    mycursor = get_db().cursor()
    mycursor.execute("SELECT * FROM images WHERE id = %s", (file_id,))
    image = mycursor.fetchone()

    if image:
        return send_file(io.BytesIO(image['image']), mimetype = 'image/jpeg')
    else:
        return "Image not found", 404


# Affichage
@testimagebdd.route('/test')
def upload_form_show():
    mycursor = get_db().cursor()
    mycursor.execute("SELECT * FROM images;")
    files = mycursor.fetchall()
    adminsession = admin_session()
    return render_template('test/upload.html', files = files, adminsession = adminsession)

# Téléchargement
@testimagebdd.route('/upload', methods = ['POST'])
def upload():
    file = request.files['file']
    if file:
        mycursor = get_db().cursor()
        filename = secure_filename(file.filename)
        imageBlob = file.read()
        mycursor.execute("INSERT INTO images (name, image) VALUES (%s, %s)", (filename, imageBlob))
        get_db().commit()

    return redirect('/test')