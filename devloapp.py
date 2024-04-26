from flask import render_template, Flask, session, redirect, url_for, g, has_app_context
from App import home, inscription, verification, connexion, resend
from App.utils.bdd import DevloBDD

app = Flask(__name__)
app.debug = True
app.secret_key = "banane"
app.which = "devlobdd"


def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = DevloBDD(app.which)
        print(db.get_ja_byid("JA-8166"))
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

@app.route("/home")
def route_home():
    if 'email' not in session:
        return redirect(url_for('route_connexion'))
    return home.index()


@app.route("/parametres/generaux", methods=("GET", "POST"))
def route_parametres_generaux():
    if 'email' not in session:
        return redirect(url_for('route_connexion'))
    return home.parametres_generaux()


@app.route("/parametres/theme", methods=("GET", "POST"))
def route_parametres_theme():
    if 'email' not in session:
        return redirect(url_for('route_connexion'))
    return home.parametres_theme()

@app.route("/pages/add", methods=("GET", "POST"))
def route_add_page():
    if 'email' not in session:
        return redirect(url_for('route_connexion'))
    return home.add_page()

@app.route("/site_verification", methods=("GET", "POST"))
def route_site_verification():
    if 'email' not in session:
        return redirect(url_for('route_connexion'))
    return home.site_verification()

@app.route("/domaine", methods=("GET", "POST"))
def route_domaine():
    if 'email' not in session:
        return redirect(url_for('route_connexion'))
    return home.domaine()


@app.route("/preview/<string:slug>")
def route_preview(slug):
    return render_template(f'preview/{slug}.html', slug=slug)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error/404.html'), 404

@app.errorhandler(500)
def internal_error(e):
    return render_template('error/500.html', error=e), 500

@app.route("/blog/<string:slug>")
def route_blog_post(slug):
    if DevloBDD.post_exists(slug) == True:
        return render_template('blog/post.html', post=DevloBDD.post_data(slug))
    return render_template('error/404.html'), 404


if __name__ == "__main__":
    # therms-and-conditions
    app.run(port=5555)