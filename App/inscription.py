from flask import render_template, request

def inscription():
    """
    Gestion du formulaire d'inscription Flask

    :param ja_id:
    :param email:
    :param password:
    :return:
    """
    if request.method == 'POST':
        ja_id = request.form['ja_id']
        email = request.form['email']
        password = request.form['password']

        #TODO  Je suis sensé vérifier que ja_id est bien dans la BDD de samuel

        

    return render_template("inscription.html")