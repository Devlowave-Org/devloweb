from flask import render_template, Flask, session, redirect, url_for, g, has_app_context, request


def proof_of_concept():
    if request.method == "POST":
        if not request.form['titre'] or not request.form['valeur1']:
            return render_template("pof.html", error="Veuillez remplir tous les champs")

        form = request.form.to_dict()
        print(form)

    return render_template("pof.html")