from flask import render_template, request
from App.utils import bdd, utils


def verify_email():

    if request.method == 'POST':
        if not request.form["verif"] or not request.form["ja_id"]:
            return render_template("verification.html", error="Veuillez remplir tous les champs")

        devlobdd = bdd.DevloBDD()
        if utils.is_punished(devlobdd, request.remote_addr):
            return render_template("verification.html", error="Vous n'êtes pas vérifié")
        try:
            ja_id = utils.ja_id_only(request.form["ja_id"])
        except ValueError as e:
            return render_template("verification.html", error=e)

        if utils.verif_code(devlobdd, ja_id, request.form["verif"]):
            # J'active la JA
            devlobdd.activer_ja(ja_id)
            return render_template("verification.html", error="Vous êtes vérifié")
        else:
            # Sinon je lui fais passer un sale quart d'heure
            utils.add_a_try(devlobdd, request.remote_addr)
            return render_template("verification.html", error="Vous netes pas verifié")

    return render_template('verification.html')