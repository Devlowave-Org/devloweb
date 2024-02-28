from flask import request, render_template


def connexion():
    if request.method == 'POST':
        if request.form['']:
            pass
    return render_template("connexion.html")