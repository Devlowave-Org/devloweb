from flask import render_template, Flask, session, redirect, url_for, request, jsonify
from App import home, inscription, verification, connexion, resend, onthefly, forgot_password
from App.utils.bdd import DevloBDD
from App.utils.utils import is_connected, is_admin
from werkzeug.middleware.proxy_fix import ProxyFix
from App.admin_space import admin_panel
from App.Analytics.Analytics import get_analytics
from os import path, getcwd, environ
from dotenv import load_dotenv
from datetime import timedelta

env = path.join(getcwd(), '.env')
if path.exists(env):
    load_dotenv(env)

app = Flask(__name__)
app.secret_key = "banane"
app.which = "devlobdd"
app.config["UPLOAD_FOLDER"] = "tmp/"
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_host=1)

if environ.keys().__contains__("SERVER_NAME") and environ["ENV"] == "prod":
    app.config["SERVER_NAME"] = environ["SERVER_NAME"]
    db = DevloBDD(environ["DB_USERNAME"], environ["DB_PASSWORD"], "localhost", 3306)

elif environ["ENV"] == "test":
    app.config["SERVER_NAME"] = "127.0.0.1:5555"
    db = DevloBDD(environ["DB_USERNAME"], environ["DB_PASSWORD"], "localhost", 3306, database="devlotest")
else:
    app.config["SERVER_NAME"] = "127.0.0.1:5555"
    db = DevloBDD(environ["DB_USERNAME"], environ["DB_PASSWORD"], "localhost", 3306)


db.create_bdd()

# Création de la BDD analytics, uniquement si la variable d'environnement est sur True
if environ["ANALYTICS"] == "True":
    db.create_bdd_analytics()

@app.before_request
def before_request():
    # Si l'url est celle de la collecte de l'Analytics et qu'elles sont désactivé, erreur 403
    if request.path == url_for("collect_data") and environ["ANALYTICS"] == "False":
        return jsonify({"status": "error", "message": "Collecte de données désactivée pour cette environnement!"}), 403
    # Sinon on continue


@app.route("/", subdomain="<subdomain>")
def index(subdomain):
    print(f"Acces depuis {subdomain} !")
    if subdomain != "devlowave":
        return onthefly.gen_on_the_fly(subdomain, db)
    return render_template("index.html")

@app.route("/tmp/<ja>/<image>", methods=("GET",))
def route_tmp(ja, image):
    # C'est le DASHBOARD Éditeur
    print(ja, image)
    return onthefly.send_image(ja, image)


@app.route("/")
def accueil():
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
    if is_connected(session, db):
        return home.index(db)
    return redirect(url_for('route_connexion'))


@app.route("/home/account", methods=("GET", "POST"))
def route_account():
    if is_connected(session, db):
        return home.account(db)
    return redirect(url_for('route_connexion'))


@app.route("/home/editeur/starting_point", methods=("GET", "POST"))
def route_starting_point():
    # C'est le starting point t'as capté
    if is_connected(session, db):
        return home.starting_point()
    return redirect(url_for('route_connexion'))

@app.route("/home/editeur", methods=("GET", "POST"))
def route_editeur():
    # C'est l'éditeur dans le panel
    if is_connected(session, db):
        return render_template("home/editeur.html")
    return redirect(url_for('route_connexion'))

@app.route("/home/preview", methods=("GET", "POST"))
def route_preview():
    # C'est le DASHBOARD Éditeur
    if is_connected(session, db):
        return home.preview(session["ja_id"])
    return redirect(url_for('route_connexion'))


@app.route("/editeur/beta/editeur", methods=("GET", "POST"))
def route_beta():
    if is_connected(session, db):
        return home.editeur()
    return redirect(url_for('route_connexion'))

@app.route("/home/hebergement", methods=("GET", "POST"))
def route_hebergement():
    if is_connected(session, db):
        return home.hebergement(db)
    return redirect(url_for('route_connexion'))


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('accueil'))


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
ESPACE ADMIN
"""
@app.route("/admin_space/", methods=("GET", "POST"))
@app.route("/admin_space", methods=("GET", "POST"))
def route_admin_space():
    return redirect("/admin_space/panel")

@app.route("/admin_space/panel", methods=("GET", "POST"))
def route_admin_space_website_validator():
    return admin_panel.load(db)


@app.route("/admin_space/preview/<ja_id>", methods=("GET", "POST"))
def route_admin_preview(ja_id):
    # C'est le DASHBOARD Éditeur
    if is_admin(session, db):
        return home.preview(ja_id)
    return redirect(url_for('route_connexion'))

"""
Espace Analytics
"""
@app.route("/collect", methods=["POST"])
def collect_data():
    return get_analytics(db)


if __name__ == "__main__":
    # therms-and-conditions
    app.run(host="127.0.0.1", port=5555, debug=True)
