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
        if not request.form['email'] or not request.form['password'] or not request.form['ja_id']:
            return render_template("inscription.html", error="Veuillez remplir tous les champs")

        try:
            ja_id = utils.ja_id_int(ja_id=request.form['ja_id'])
        except ValueError as e:
            return render_template('inscription.html', error=str(e))

        email = request.form['email']
        password = request.form['password']

        if not utils.email_validator(email):
            return render_template('inscription.html')

        # TODO  Je suis sensé vérifier que ja_id est bien dans la BDD de samuel
        if ja_id == 8166:
            pass

    return render_template("inscription.html")