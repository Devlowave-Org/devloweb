from flask import render_template, Flask, session, redirect, url_for, g, has_app_context, request
import json

def proof_of_concept():
    if 'email' not in session:
        return redirect(url_for('route_connexion'))

    if request.method != "POST":
        return render_template("pof.html", error="Veuillez remplir tous les champs")

    if not request.form['titre'] or not request.form['valeur1']:
        return render_template("pof.html", error="Veuillez remplir tous les champs")

    form = request.form.to_dict()
    json_site = open(f"tmp/{session['ja_id']}/site.json")
    print(form)

    return render_template("pof.html")