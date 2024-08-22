from datetime import datetime

from flask import request, render_template, session, redirect, url_for
from App.utils import utils
import bcrypt



def forgot_password(devlobdd):
    if 'email' in session:
        return redirect(url_for('route_home'))

    if request.method == 'POST':
        if not request.form['ja_id']:
            return render_template('forgot_password.html', error='Veuillez remplir votre identifiant JA')

        try:
            ja_id = utils.ja_id_only(ja_id=request.form['ja_id'])
        except ValueError as e:
            return render_template('forgot_password.html', error="Veuillez transmettre un identifiant valide.")

        ip = request.remote_addr

        if utils.is_punished(devlobdd, ip):
            return render_template('forgot_password.html', error="Une erreur est survenue")


        ja = devlobdd.get_ja_byid(ja_id)
        if not ja:
            utils.add_a_try(devlobdd, ip)
            return render_template("forgot_password.html", error="Un mail a été envoyé si le compte existe.")

        email = ja[1]
        utils.magic_link(devlobdd, ja_id, email)
        return render_template("forgot_password.html", error="Un mail a été envoyé si le compte existe.")


    return render_template("forgot_password.html")


def reset_password(devlobdd):
    if 'email' in session:
        return redirect(url_for('route_home'))

    ip = request.remote_addr
    if utils.is_punished(devlobdd, ip):
        return render_template('reset_password.html', error="Une erreur est survenue")


    if request.method == 'POST':
        if not request.form['code'] or not request.form['password'] or not request.form['email']:
            return render_template('reset_password.html', error='Veuillez remplir tous les champs')

        if not devlobdd.magic_link_exists(code=request.form['code']):
            return render_template('reset_password.html', error='Code incorrect')

        row = devlobdd.get_magic_link(code=request.form['code'])
        ja = devlobdd.get_ja_byid(row[1])

        if ja[1] != request.form['email']:
            return render_template('reset_password.html', error='Email incorrect')

        code_date = datetime.strptime(row[2], "%Y-%m-%d %H:%M:%S.%f")
        delta = datetime.now() - code_date
        if delta.seconds > 1800:
            return render_template('reset_password.html', error='Le code n\'est plus valide')



        if len(request.form['password']) < 12:
            return render_template('inscription.html', error="Veuillez avoir un mot de passe d'au moins 12 caractères")
        hashed_pass = bcrypt.hashpw(request.form['password'].encode("utf-8"), bcrypt.gensalt())
        devlobdd.change_password(ja[0], hashed_pass)



    return render_template("reset_password.html")
