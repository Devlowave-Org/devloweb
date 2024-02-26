from flask import render_template, request
from utils import utils
from utils import bdd
from utils import email_api
from utils import verification
import bcrypt


def inscription():
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
            return render_template('inscription.html')

        # On vérifie le mot de passe
        password = request.form['password']
        if len(password) < 12:
            return render_template('inscription.html', error="Veuillez avoir un mot de passe d'au moins 12 caractères")

        hashed_pass = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

        """
        On va maintenant utiliser la base de donnée pour :
        - Vérifier que la JA n'a pas déjà un compte
        - Enregistre le compte
        """
        devlobdd = bdd.DevloBDD()
        if devlobdd.ja_exists(ja_id):
            return render_template("inscription.html", error="Vous avez déjà un compte.")

        devlobdd.inscire_ja(ja_id, email, hashed_pass)

        # TODO je dois vérifier que la JA n'a pas déja un compte
        # TODO  Je suis sensé vérifier que ja_id est bien dans la BDD de samuel
        if ja_id == 8166:
            pass
        etape_verification(devlobdd, ja_id, email)

    return render_template("inscription.html")

def etape_verification(devlobdd, ja_id, mail):
    code = verification.create_verification_code(devlobdd)
    verification.store_code(devlobdd, ja_id, code)
    devlomail = email_api.DevloMail()
    devlomail.send_verification_email(mail, code)



    return render_template("inscription.html", error="AUCUNE ERREUR")