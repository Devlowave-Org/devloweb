from flask import request, render_template, session, redirect, flash, url_for
from App.utils import bdd, utils, cloudflare
import json


def index():
    return render_template('home/index.html')


def editeur():
    json_site = json.loads(open(f"tmp/{session['ja_id']}/site.json").read())
    print(json_site)

    if request.method == "POST":
        print(request.form.keys())
        form = request.form.to_dict()
        utils.editeur_form_processing(form, json_site)

    return render_template("editor/v1/editeur.html", data=json_site)


def parametres_theme(devlobdd):
    if request.method == 'POST':
        devlobdd.change_theme(session['ja_id'], request.form.get('theme'))
    return render_template('home/parametres_theme.html', data=devlobdd.get_site_by_ja(session['ja_id']))
                                                                                         
def site_verification(devlobdd):
    return render_template('home/verification.html', data=devlobdd.get_site_by_ja(session['ja_id']))

def domaine(devlobdd):
    if request.method == 'POST':
        name = request.form.get('name')
        domain = request.form.get('domain')
        data=devlobdd.get_site_by_ja(session['ja_id'])
        if data[1] == f"{name.lower()}.{domain.lower()}":
            flash("Rien n'as changé !")
            data=devlobdd.get_site_by_ja(session['ja_id'])
            return render_template('home/domaine.html', data=data)
        
        if cloudflare.subdomain_exist(name, domain) == False:
            # Fonction magique
            test = cloudflare.create_subdomain(name, "1.2.3.4", domain)
            if test == True:
                cloudflare.delete_subdomain({data[1]}, {data[2]})
                devlobdd.change_domain(session['ja_id'], name.lower(), domain.lower())
                flash("Votre domaine a été enregistré ! ")
                data=devlobdd.get_site_by_ja(session['ja_id'])
                return render_template('home/domaine.html', data=data)
            else:
                flash("Erreur : " + str(test))
        else:
            flash("Erreur : ce nom de domaine existe de déjà !")
    data = devlobdd.get_site_by_ja(session['ja_id'])
    return render_template('home/domaine.html', data=data)

def add_page():
    return render_template('home/add_page.html')

def list_page():
    return render_template('home/list_page.html')