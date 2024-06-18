from flask import request, render_template, session, redirect, flash
from App.utils import bdd, utils, cloudflare
import os
import json


def index():
    return render_template('home/index.html')

def parametres_generaux(devlobdd):
    if request.method == 'POST':
        form_data = request.form.to_dict(flat=True)  # Convert ImmutableMultiDict to regular dict
        
        # Ancienne ligine qui boom boom la bdd
        #devlobdd.boom_boom(form_data, session['ja_id'])
        
        # Mais maintenant, on fait du JSON 😏
        form_data['ja_id'] = session['ja_id']
        form_data['ip'] = session['ip']
        
        print(form_data)
        
        with open(f'data/{session["ja_id"]}.json', 'w', encoding='utf-8') as f:
            json.dump(form_data, f, ensure_ascii=False, indent=4)
            
    
    json_data = {}
    
    if os.path.isfile(f'data/{session["ja_id"]}.json') and os.path.getsize(f'data/{session["ja_id"]}.json') > 0:
        with open(f'data/{session["ja_id"]}.json', 'r', encoding='utf-8') as f:
            json_data = json.loads(f.read())
            
    return render_template('home/parametres_generaux.html', json_data=json_data, data=devlobdd.get_site_by_ja(session['ja_id']))

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
    data=devlobdd.get_site_by_ja(session['ja_id'])
    return render_template('home/domaine.html', data=data)

def add_page():
    return render_template('home/add_page.html')

def list_page():
    return render_template('home/list_page.html')