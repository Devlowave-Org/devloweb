from flask import render_template, request, redirect, url_for
from App.utils import utils


def verify_email(devlobdd):

    if request.method == 'POST':
        if not request.form["verif"] or not request.form["ja_id"]:
            return render_template("verification.html", error="Veuillez remplir tous les champs")

        if utils.is_punished(devlobdd, request.remote_addr):
            return render_template("verification.html", error="Désolé mais vous avez fait trop de tentatives")
        try:
            ja_id = utils.ja_id_only(request.form["ja_id"])
        except ValueError as e:
            return render_template("verification.html", error=e)

        if devlobdd.is_active(ja_id):
            return render_template('connexion.html', error="Vous êtes déjà activé")

        if utils.verif_code(devlobdd, ja_id, request.form["verif"]):
            # J'active la JA
            # et je supprime e code de verif
            utils.create_ja_folder(ja_id)
            utils.set_default_value_to_json_site(ja_id)
            devlobdd.activer_email_ja(ja_id)
            devlobdd.delete_code(ja_id)
            devlobdd.init_website(ja_id, "", "beta")
            return redirect(url_for("route_home"))
        else:
            # Sinon je lui fais passer un sale quart d'heure
            utils.add_a_try(devlobdd, request.remote_addr)
            return render_template("verification.html", error="Vous n'êtes pas verifié")

    return render_template('verification.html')