from flask import request, render_template
from utils import bdd, utils
import bcrypt

def connexion():
    if request.method == 'POST':
        if not request.form['email'] or not request.form['password']:
            return render_template('connexion.html', error='Veuillez remplir tous les champs')

        devlobdd = bdd.DevloBDD()
        if utils.is_punished(devlobdd, request.remote_addr):
            return render_template('connexion.html', error="Mail ou mot de passe incorrect")



    return render_template("connexion.html")