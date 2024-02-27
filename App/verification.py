from flask import render_template, request
from utils import utils
from utils import bdd
from utils import email_api


def verify_email():
    if request.method == 'POST':
        if not request.form["verif"] or not request.form["ja_id"]:
            return render_template("verification.html", error="Veuillez remplir tous les champs")

        devlobdd = bdd.DevloBDD()
        try:
            ja_id = utils.ja_id_only(request.form["ja_id"])
        except ValueError as e:
            return render_template("verification.html", error=e)

        if utils.verif_code(devlobdd, ja_id, request.form["verif"]):
            return render_template("verification.html", error="Vous êtes vérifié")
        else:
            return render_template("verification.html", error="Vous netes pas verifié")

    return render_template('verification.html')