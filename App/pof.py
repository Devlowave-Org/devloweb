from flask import render_template, Flask, session, redirect, url_for, g, has_app_context, request
import json

def proof_of_concept():
    if 'email' not in session:
        return redirect(url_for('route_connexion'))

    json_site = json.loads(open(f"tmp/{session['ja_id']}/site.json").read())
    print(json_site)

    if request.method == "POST":
        form = request.form.to_dict()
        with open(f"tmp/{session['ja_id']}/site.json", "w") as f:
            json.dump(form, f)
        print(form)

    return render_template("editor/pof.html", data=json_site)