from flask import render_template, Flask, session, redirect, url_for, g, has_app_context
from App import home, inscription, verification, connexion, resend, pof, onthefly
from App.utils.bdd import DevloBDD

app = Flask(__name__)
app.debug = True
app.secret_key = "banane"
app.which = "devlobdd"


def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = DevloBDD(app.which)
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        print("Je close la bdd")
        db.quit_bdd()

"""devlobdd = None
if __name__ != "__main__":
    os.system("rm devlotest.db")
    devlobdd = DevloBDD("devlotest")
    print("On est sur DevloTest actuellement")
else:
    devlobdd = DevloBDD()
"""

@app.route("/")
def index():
    return render_template("index.html")

"""
ESPACE INSCRIPTION/CONNEXION
"""
@app.route("/inscription", methods=("GET", "POST"))
def route_inscription():
    return inscription.inscription(get_db())


@app.route("/verification", methods=("GET", "POST"))
def route_verification():
    return verification.verify_email(get_db())


@app.route("/connexion", methods=("GET", "POST"))
def route_connexion():
    return connexion.connexion(get_db())


@app.route("/resend", methods=("GET", "POST"))
def route_resend():
    return resend.resend_email(get_db())


"""
ESPACE MODIFICATION DU SITE
"""


@app.route("/home")
def route_home():
    if 'email' not in session:
        return redirect(url_for('route_connexion'))
    return home.index()


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
    return home.parametres_theme(get_db())


@app.route("/pages/add", methods=("GET", "POST"))
def route_add_page():
    if 'email' not in session:
        return redirect(url_for('route_connexion'))
    return home.add_page()


@app.route("/site_verification", methods=("GET", "POST"))
def route_site_verification():
    if 'email' not in session:
        return redirect(url_for('route_connexion'))
    return home.site_verification(get_db())


@app.route("/domaine", methods=("GET", "POST"))
def route_domaine():
    if 'email' not in session:
        return redirect(url_for('route_connexion'))
    return home.domaine(get_db())


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
    return onthefly.gen_on_the_fly(ja_domain, get_db())



if __name__ == "__main__":
    # therms-and-conditions
    app.run(host="0.0.0.0", port=5555)