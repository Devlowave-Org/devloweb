from zipfile import error

from flask import render_template, request, redirect, url_for
from App.utils import bdd, utils


def resend_email(devlobdd):
    if request.method == 'POST':
        if not request.form["email"]:
            return render_template("resend.html", error="Veuillez remplir tous les champs")

        ja = devlobdd.get_ja_by_mail(request.form["email"])
        if not ja:
            return render_template("resend.html", error="Il n'y a aucune JA associée à cet email...")

        ja_id = ja[0]

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