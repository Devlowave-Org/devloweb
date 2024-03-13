from flask import render_template, Flask
from App import inscription, verification, connexion
from utils.bdd import DevloBDD


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


if __name__ == "__main__":
    app.run(port=5555)