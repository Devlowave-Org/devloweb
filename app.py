from flask import render_template, Flask
from App import inscription

app = Flask(__name__)
app.debug = True
app.secret_key = "banane" 


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/inscription", methods=["GET", "POST"])
def route_inscription():
    return inscription.inscription()



if __name__ == "__main__":
    app.run(port=5555)