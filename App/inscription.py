import time
from flask import render_template, request, redirect, url_for, session
from App.utils import utils, rnja_api
import bcrypt


def inscription(devlobdd):
    if 'email' in session:
        return redirect(url_for('route_home'))
    
    start = time.time()
    """
    Gestion du formulaire d'inscription Flask

    :param ja_id:
    :param email:
    :param password:
    :return:
    """
    if request.method == 'POST':
        if not request.form['email'] or not request.form['password'] or not request.form['ja_id']:
            return render_template("inscription.html", error="Veuillez remplir tous les champs")

        # Nous ne gardons que l'entier de JA-0000
        try:
            ja_id = utils.ja_id_only(ja_id=request.form['ja_id'])
        except ValueError as e:
            return render_template('inscription.html', error=str(e))

        # On vérifie l'email
        email = request.form['email']
        if not utils.email_validator(email):
            return render_template('inscription.html', error="Veuillez remplir un email valide")

        ja_api = rnja_api.ja_exists(ja_id)
        if not ja_api:
            return render_template("inscription.html", error="Désolé mais cette JA n'existe pas (encore).")

        # On vérifie le mot de passe
        password = request.form['password']
        if len(password) < 9:
            return render_template('inscription.html', error="Veuillez avoir un mot de passe d'au moins 9 caractères")

        hashed_pass = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

        """
        On va maintenant utiliser la base de donnée pour :
        - Vérifier que la JA n'a pas déjà un compte
        - Enregistre le compte
        """
        if devlobdd.ja_exists(ja_id):
            return render_template("inscription.html", error="Vous avez déjà un compte.")

        devlobdd.inscire_ja(ja_id, ja_api["name"], hashed_pass, email)

        # On lui envoie un mail avec le code.
        utils.etape_verification(devlobdd, ja_id)
        end = time.time()
        print(f"Temps d'execution {end - start}")
        return redirect(url_for('route_verification'))

    return render_template("inscription.html")





