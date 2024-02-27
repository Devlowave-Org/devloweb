from flask import render_template, request
from utils import utils
from utils import bdd
from utils import email_api


def verify_email():
    if request.method == 'POST':
        if not request.form["verif"] or not request.form["ja_id"]:
            return render_template("verification.html", error="Veuillez remplir tous les champs")

        devlobdd = bdd.DevloBDD()

        if devlobdd.code_exists(request.form["verif"]):
            return render_template("verification.html", error="Pas d'erreur")

        devlobdd.add_try(request.remote_addr)
        print("OKKKK")
    return render_template('verification.html')