from flask import render_template, Flask

app = Flask(__name__)
app.secret_key = "banane"


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/connexion")
def route_connexion():
    return render_template("connexion.html")

@app.route("/inscription")
def route_inscription():
    return render_template("inscription.html")

@app.route("/verification")
def route_verification():
    return render_template("verification.html")