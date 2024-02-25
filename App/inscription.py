from flask import render_template, request
from utils import utils
def inscription():
    """
    Gestion du formulaire d'inscription Flask

    :param ja_id:
    :param email:
    :param password:
    :return:
    """
    if request.method == 'POST':
        ja_id = utils.ja_id_int(ja_id=request.form['ja_id'])

        email = request.form['email']
        password = request.form['password']

        if not utils.email_validator(email):
            return render_template('inscription.html')

        # TODO  Je suis sensé vérifier que ja_id est bien dans la BDD de samuel
        if ja_id == 8166:
            pass

    return render_template("inscription.html")