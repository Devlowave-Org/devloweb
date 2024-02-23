from flask import render_template, Flask

app = Flask(__name__)
app.debug = True
app.secret_key = "banane"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/inscription")
def inscription():
    return render_template("inscription.html")



if __name__ == "__main__":
    app.run(port=5555)