from flask import render_template, Flask, session, redirect, url_for, g, has_app_context
from App import home, inscription, verification, connexion, resend, pof, onthefly, forgot_password
from App.utils.bdd import DevloBDD
from os import path, getcwd
from json import load

app = Flask(__name__)
app.debug = True
app.secret_key = "banane"
app.which = "devlobdd"


file_path = path.abspath(path.join(getcwd(), "config.json"))  # Trouver le chemin complet du fichier config.json

# Lecture du fichier JSON
with open(file_path, 'r') as file:
    config_data = load(file)  # Ouverture du fichier config.json

db = DevloBDD(config_data['database']['username'], config_data['database']['password'], config_data['database']['addr'], config_data['database']['port'])

db.create_bdd()

@app.route("/")
def index():
    return render_template("index.html")

"""
ESPACE INSCRIPTION/CONNEXION
"""
@app.route("/inscription", methods=("GET", "POST"))
def route_inscription():
    return inscription.inscription(db)


@app.route("/verification", methods=("GET", "POST"))
def route_verification():
    return verification.verify_email(db)


@app.route("/connexion", methods=("GET", "POST"))
def route_connexion():
    return connexion.connexion(db)

@app.route("/forgotpassword", methods=("GET", "POST"))
def route_forgot():
    return forgot_password.forgot_password(db)

@app.route("/reset_password", methods=("GET", "POST"))
def route_reset():
    return forgot_password.reset_password(db)

@app.route("/resend", methods=("GET", "POST"))
def route_resend():
    return resend.resend_email(db)


"""
ESPACE MODIFICATION DU SITE
"""


@app.route("/home")
def route_home():
    if 'email' not in session:
        return redirect(url_for('route_connexion'))
    return home.index()

@app.route("/home/account")
def route_account():
    if 'email' not in session:
        return redirect(url_for('route_connexion'))
    return home.account()


@app.route("/home/editeur", methods=("GET", "POST"))
def route_editeur():
    # C'est le DASHBOARD Éditeur
    print(session)
    if 'email' not in session:
        return redirect(url_for('route_connexion'))
    return render_template("home/editeur.html")


@app.route("/pof", methods=("GET", "POST"))
def route_pof():
    return pof.proof_of_concept()


@app.route("/editeur/v1/editeur", methods=("GET", "POST"))
def route_v1():
    if 'email' not in session:
        return redirect(url_for('route_connexion'))
    return home.editeur()

@app.route("/editeur/beta/editeur", methods=("GET", "POST"))
def route_beta():
    if 'email' not in session:
        return redirect(url_for('route_connexion'))
    return home.editeur()


@app.route("/editeur/pof", methods=("GET", "POST"))
def route_editeur_pof():
    if 'email' not in session:
        return redirect(url_for('route_connexion'))
    return home.editeur()


"""
ESPACE GESTION DU THÈME
"""
@app.route("/parametres/theme", methods=("GET", "POST"))
def route_parametres_theme():
    if 'email' not in session:
        return redirect(url_for('route_connexion'))
    return home.parametres_theme(db)


@app.route("/pages/add", methods=("GET", "POST"))
def route_add_page():
    if 'email' not in session:
        return redirect(url_for('route_connexion'))
    return home.add_page()


@app.route("/site_verification", methods=("GET", "POST"))
def route_site_verification():
    if 'email' not in session:
        return redirect(url_for('route_connexion'))
    return home.site_verification(db)


@app.route("/domaine", methods=("GET", "POST"))
def route_domaine():
    if 'email' not in session:
        return redirect(url_for('route_connexion'))
    return home.domaine(db)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


"""
ESPACE SOUS-DOMAINES
"""
@app.route("/", subdomain="<ja_domain>")
def ja_website(username):
    return username + ".your-domain.tld"
"""
ESPACE ERREURS
"""
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error/404.html'), 404

@app.errorhandler(500)
def internal_error(e):
    return render_template('error/500.html', error=e), 500


"""
GESTION DE GÉNÉRATION A LA VOLÉE
"""
@app.route("/ja/<ja_domain>")
def route_ja(ja_domain):
    return onthefly.gen_on_the_fly(ja_domain, db)



if __name__ == "__main__":
    # therms-and-conditions
    app.run(host="0.0.0.0", port=5555)