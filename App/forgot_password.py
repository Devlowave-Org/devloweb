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

        if devlobdd.get_magic_link_by_ja(ja_id):
            row = devlobdd.get_magic_link_exists_by_ja(ja_id)
            delta = datetime.now() - row[2]

            if delta.seconds < 30:
                return render_template('forgot_password.html', error=f"Veuillez attendre {30 - delta.seconds} secondes.")
            devlobdd.delete_magic_link(row[0])


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
            utils.add_a_try(devlobdd, ip)
            return render_template('reset_password.html', error='Code incorrect')

        row = devlobdd.get_magic_link(code=request.form['code'])
        ja = devlobdd.get_ja_byid(row[0])

        if ja[3] != request.form['email']:
            utils.add_a_try(devlobdd, ip)
            return render_template('reset_password.html', error='Email incorrect')

        code_date = datetime.strptime(str(row[2]), "%Y-%m-%d %H:%M:%S.%f")
        delta = datetime.now() - code_date
        if delta.seconds > 1800:
            return render_template('reset_password.html', error='Le code n\'est plus valide')



        if len(request.form['password']) < 9:
            return render_template('reset_password.html', error="Veuillez avoir un mot de passe d'au moins 9 caractères")
        hashed_pass = bcrypt.hashpw(request.form['password'].encode("utf-8"), bcrypt.gensalt())
        devlobdd.change_password(ja[0], hashed_pass)
        devlobdd.delete_magic_link(ja_id=ja[0])

        return render_template('connexion.html', error="Mot de passe mis à jour")



    return render_template("reset_password.html")
