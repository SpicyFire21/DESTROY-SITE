#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import *
from connection_bdd import get_db

fixtures_load = Blueprint('fixtures_load', __name__, template_folder = 'templates')


@fixtures_load.route('/base/init')
def fct_fixtures_load():
    cursor = get_db().cursor()

    with open('script.sql', 'r') as f:
        sql = f.read()
        sqlCommands = sql.replace('\n', '').split(';')
        for command in sqlCommands:
            print('sql :',sqlCommands)
            try:
                if command.strip() != '':
                    cursor.execute(command)
                    get_db().commit()
            except IOError:
                print(f"Command skipped: {command}")

    return redirect('/')
