#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, abort, flash, session

from connection_bdd import get_db

admin_index = Blueprint('admin_index', __name__,
                        template_folder='templates')

@admin_index.route('/admin/index')
def admin_show():
    return render_template('admin/index.html')