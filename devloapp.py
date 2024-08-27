from flask import render_template, Flask, session, redirect, url_for, g
from App import home, inscription, verification, connexion, resend, onthefly, forgot_password
from App.utils.bdd import DevloBDD
from App.utils.utils import is_connected
from werkzeug.middleware.proxy_fix import ProxyFix
import os

app = Flask(__name__)
app.secret_key = "banane"
app.which = "devlobdd"
app.wsgi_app = ProxyFix(
    app.wsgi_app, x_for=1, x_proto=0, x_host=1, x_prefix=1
)

if os.environ.keys().__contains__("SERVER_NAME") and os.environ["ENV"] == "prod":
    app.config["SERVER_NAME"] = os.environ["SERVER_NAME"]
else:
    app.config["SERVER_NAME"] = "127.0.0.1:5555"


def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = DevloBDD(app.which)
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        print(f"Je close la bdd : {exception}")
        db.quit_bdd()


"""devlobdd = None
if __name__ != "__main__":
    os.system("rm devlotest.db")
    devlobdd = DevloBDD("devlotest")
    print("On est sur DevloTest actuellement")
else:
    devlobdd = DevloBDD()
"""
@app.before_request
def before_request():
    print(os.environ.keys())

@app.route("/", subdomain="<subdomain>")
def index(subdomain):
    print(f"Acces depuis {subdomain} !")
    if subdomain != "devlowave":
        return onthefly.gen_on_the_fly(subdomain, get_db())
    return render_template("index.html")

@app.route("/")
def accueil():
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


@app.route("/forgotpassword", methods=("GET", "POST"))
def route_forgot():
    return forgot_password.forgot_password(get_db())


@app.route("/reset_password", methods=("GET", "POST"))
def route_reset():
    return forgot_password.reset_password(get_db())


@app.route("/resend", methods=("GET", "POST"))
def route_resend():
    return resend.resend_email(get_db())


"""
ESPACE MODIFICATION DU SITE
"""


@app.route("/home")
def route_home():
    if is_connected(session, get_db()):
        return home.index(get_db())
    return redirect(url_for('route_connexion'))


@app.route("/home/account")
def route_account():
    if is_connected(session, get_db()):
        return home.account()
    return redirect(url_for('route_connexion'))


@app.route("/home/editeur", methods=("GET", "POST"))
def route_editeur():
    # C'est le DASHBOARD Éditeur
    if is_connected(session, get_db()):
        return render_template("home/editeur.html")
    return redirect(url_for('route_connexion'))




@app.route("/editeur/beta/editeur", methods=("GET", "POST"))
def route_beta():
    if is_connected(session, get_db()):
        return home.editeur()
    return redirect(url_for('route_connexion'))

@app.route("/home/hebergement", methods=("GET", "POST"))
def route_hebergement():
    if is_connected(session, get_db()):
        return home.hebergement(get_db())
    return redirect(url_for('route_connexion'))


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


"""
ESPACE ERREURS
"""


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error/404.html'), 404


@app.errorhandler(500)
def internal_error(e):
    return render_template('error/500.html', error=e), 500



if __name__ == "__main__":
    # therms-and-conditions
    app.run(host="127.0.0.1", port=5555, debug=True)
