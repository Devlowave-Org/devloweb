from flask import request, render_template, session, redirect
from App.utils import bdd, utils
import bcrypt


def index():
    return render_template('admin/index.html')

def parametres_generaux():
    return render_template('admin/parametres_generaux.html')

def site_verification():
    devlobdd = bdd.DevloBDD()
    return render_template('admin/verification.html', data=devlobdd.get_site_by_ja(session['ja']))

def domaine():
    devlobdd = bdd.DevloBDD()
    return render_template('admin/domaine.html', data=devlobdd.get_site_by_ja(session['ja']))

def add_page():
    return render_template('admin/add_page.html')

def list_page():
    return render_template('admin/list_page.html')