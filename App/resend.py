from flask import render_template, request, redirect, url_for
from App.utils import bdd, utils


def resend_email(devlobdd):
    devlobdd.ja_exists("8166")

    if request.method == 'POST':
        if not request.form["ja_id"]:
            return render_template("resend.html", error="Veuillez remplir tous les champs")

        try:
            ja_id = utils.ja_id_only(request.form["ja_id"])
        except ValueError as e:
            return render_template("resend.html", error=e)

        if devlobdd.is_active(ja_id):
            return render_template("resend.html", error="Votre JA est déjà activée")

        row = devlobdd.get_code_via_jaid(ja_id)
        if not row and devlobdd.ja_exists(ja_id):
            utils.etape_verification(devlobdd, ja_id)
        if devlobdd.ja_exists(ja_id):
            utils.update_verif_code(devlobdd, row)
            return render_template("verification.html", ok="Le code a bien été envoyé")
        return render_template("resend.html", error="Une erreur est survenue")

    return render_template('resend.html')