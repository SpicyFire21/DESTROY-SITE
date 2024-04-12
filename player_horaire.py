#! /usr/bin/python
# -*- coding:utf-8 -*-

from flask import Blueprint
from flask import Flask, request, render_template, redirect, flash, session
from werkzeug.security import generate_password_hash, check_password_hash

from connection_bdd import get_db

player_horaire = Blueprint('player_horaire', __name__,
                           template_folder = 'templates')


@player_horaire.route('/horaire_show')
def player_horaire_show():
    return render_template('player/player_horaire.html')