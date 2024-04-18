#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint, jsonify
from flask import Flask, request, render_template, redirect, abort, flash, session

from connection_bdd import get_db

nologin_index = Blueprint('nologin_index', __name__,
                        template_folder = 'templates')



@nologin_index.route('/nologin/index')
def nologin():
    return render_template('nologin/nologin_index.html')