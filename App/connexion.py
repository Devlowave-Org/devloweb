from flask import request, render_template, session, redirect, url_for
from App.utils import bdd, utils
import bcrypt

def connexion(devlobdd):
    if 'email' in session:
        return redirect(url_for('route_home'))
    
    if request.method == 'POST':
        if not request.form['email'] or not request.form['password']:
            return render_template('connexion.html', error='Veuillez remplir tous les champs')

        email = request.form['email']
        password = request.form["password"]
        ip = request.remote_addr

        if utils.is_punished(devlobdd, ip):
            return render_template('connexion.html', error="Mail ou mot de passe incorrect")

        if not utils.email_validator(email):
            return render_template('connexion.html', error="Veuillez rentrer un vrai email")

        ja = devlobdd.get_ja_by_mail(email)
        print(f"Voici la JA slon l'email : {ja}")
        if not ja:
            utils.add_a_try(devlobdd, ip)
            return render_template("connexion.html", error="Mail ou mot de passe incorrect")

        if not devlobdd.is_active(ja[0]):
            return render_template("connexion.html", error="Votre JA n'est pas activé, veuillez regarder vos mails.")


        if not bcrypt.checkpw(password.encode('utf-8'), ja[2].encode()):
            utils.add_a_try(devlobdd, ip)
            return render_template("connexion.html", error="Mail ou mot de passe incorrect")

        # Création de sa session / cookies
        utils.create_session(ja[0], ja[1], ip, email, ja[-1])
        return redirect('/home')

    return render_template("connexion.html")