from flask import request, render_template
from utils import bdd, utils
import bcrypt

def connexion():
    if request.method == 'POST':
        if not request.form['email'] or not request.form['password']:
            return render_template('connexion.html', error='Veuillez remplir tous les champs')

        email = request.form['email']
        password = request.form["password"]

        devlobdd = bdd.DevloBDD()
        if utils.is_punished(devlobdd, request.remote_addr):
            return render_template('connexion.html', error="Mail ou mot de passe incorrect")

        if not utils.email_validator(email):
            return render_template('connexion.html', error="Veuillez rentrer un vrai email")

        ja = devlobdd.get_ja_by_mail(email)
        print(f"Voici la JA slon l'email : {ja}")
        if not ja:
            return render_template("connexion.html", error="Mail ou mot de passe incorrect")

        if not devlobdd.is_active(ja[0]):
            return render_template("connexion.html", error="Votre JA n'est pas activé, veuillez regarder vos mails.")

        if not bcrypt.checkpw(password.encode('utf-8'), ja[2]):
            return render_template("connexion.html", error="Mail ou mot de passe incorrect")


    return render_template("connexion.html")