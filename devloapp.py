from flask import render_template, Flask, session, redirect, url_for
from App import inscription, verification, connexion, admin
from App.utils.bdd import DevloBDD

app = Flask(__name__)
app.debug = True
app.secret_key = "banane" 

devlobdd = DevloBDD

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/inscription", methods=("GET", "POST"))
def route_inscription():
    return inscription.inscription()


@app.route("/verification", methods=("GET", "POST"))
def route_verification():
    return verification.verify_email()


@app.route("/connexion", methods=("GET", "POST"))
def route_connexion():
    return connexion.connexion()

@app.route("/admin")
def route_admin():
    if 'email' not in session:
        return redirect(url_for('route_connexion'))
    return admin.index()

@app.route("/admin/parametres/generaux", methods=("GET", "POST"))
def route_parametres_generaux():
    if 'email' not in session:
        return redirect(url_for('route_connexion'))
    return admin.parametres_generaux()

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error/404.html'), 404

if __name__ == "__main__":
    session.clear()
    app.run(debug=True, port=5555)