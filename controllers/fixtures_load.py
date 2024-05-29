#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import *
from connection_bdd import get_db

fixtures_load = Blueprint('fixtures_load', __name__, template_folder = 'templates')


@fixtures_load.route('/base/init')
def fct_fixtures_load():
    print("BDD INIT")
    cursor = get_db().cursor()
    with open('script.sql', 'r', encoding='utf-8') as f:
        sql = f.read()
        sqlCommands = sql.replace('\n', '').split(';')
        for command in sqlCommands:
            try:
                if command.strip() != '':
                    cursor.execute(command)
                    get_db().commit()
            except IOError:
                print(f"Command skipped: {command}")

    return redirect('/')
