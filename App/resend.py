from flask import render_template, request, redirect, url_for
from App.utils import bdd, utils


def verify_email(devlobdd):

    if request.method == 'POST':
        if not request.form["ja_id"]:
            return render_template("verification.html", error="Veuillez remplir tous les champs")

        try:
            ja_id = utils.ja_id_only(request.form["ja_id"])
        except ValueError as e:
            return render_template("verification.html", error=e)



    return render_template('verification.html')