from flask import request, render_template, session, redirect
from App.utils import bdd, utils
import bcrypt

def index():
    return render_template('admin/index.html')

def parametres_generaux():
    return render_template('admin/parametres_generaux.html')