from flask import request, render_template, session, redirect, flash
from App.utils import bdd, utils, cloudflare
import bcrypt


def index():
    return render_template('home/index.html')

def parametres_generaux():
    devlobdd = bdd.DevloBDD()
    if request.method == 'POST':
        form_data = request.form.to_dict(flat=False)  # Convert ImmutableMultiDict to regular dict
        print(form_data)
        devlobdd.boom_boom(form_data, session['ja'])
    return render_template('home/parametres_generaux.html', data=devlobdd.get_site_by_ja(session['ja']))

def parametres_theme():
    devlobdd = bdd.DevloBDD()
    if request.method == 'POST':
        devlobdd.change_theme(session['ja'], request.form.get('theme'))
    return render_template('home/parametres_theme.html', data=devlobdd.get_site_by_ja(session['ja']))
                                                                                         
def site_verification():
    devlobdd = bdd.DevloBDD()
    return render_template('home/verification.html', data=devlobdd.get_site_by_ja(session['ja']))

def domaine():
    devlobdd = bdd.DevloBDD()
    if request.method == 'POST':
        name = request.form.get('name')
        domain = request.form.get('domain')
        data=devlobdd.get_site_by_ja(session['ja'])
        if data[1] == f"{name.lower()}.{domain.lower()}":
            flash("Rien n'as changé !")
            data=devlobdd.get_site_by_ja(session['ja'])
            return render_template('home/domaine.html', data=data)
        
        if cloudflare.subdomain_exist(name, domain) == False:
            # Fonction magique
            test = cloudflare.create_subdomain(name, "1.2.3.4", domain)
            if test == True:
                cloudflare.delete_subdomain({data[1]}, {data[2]})
                devlobdd.change_domain(session['ja'], name.lower(), domain.lower())
                flash("Votre domaine a été enregistré ! ")
                data=devlobdd.get_site_by_ja(session['ja'])
                return render_template('home/domaine.html', data=data)
            else:
                flash("Erreur : " + str(test))
        else:
            flash("Erreur : ce nom de domaine existe de déjà !")
    data=devlobdd.get_site_by_ja(session['ja'])
    return render_template('home/domaine.html', data=data)

def add_page():
    return render_template('home/add_page.html')

def list_page():
    return render_template('home/list_page.html')