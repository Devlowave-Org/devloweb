from flask import request, render_template, session, redirect
from App.utils import bdd, utils
import bcrypt


def index():
    return render_template('home/index.html')

def parametres_generaux():
    return render_template('home/parametres_generaux.html')

def site_verification():
    devlobdd = bdd.DevloBDD()
    return render_template('home/verification.html', data=devlobdd.get_site_by_ja(session['ja']))

def domaine():
    devlobdd = bdd.DevloBDD()
    return render_template('home/domaine.html', data=devlobdd.get_site_by_ja(session['ja']))

def add_page():
    return render_template('home/add_page.html')

def list_page():
    return render_template('home/list_page.html')