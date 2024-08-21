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

