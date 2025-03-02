import re
from bcrypt import hashpw, gensalt
from flask import request, render_template, session, redirect, flash, url_for
from App.tests.test_inscription import devlobdd
from App.utils import utils
import json
import os

def index(devlobdd):
    example_sites = devlobdd.get_random_domain()
    print(example_sites)
    return render_template('home/index.html', example_sites=example_sites)


def editeur():
    json_site = json.loads(open(f"tmp/{session['ja_id']}/site.json").read())
    sections = os.listdir("templates/editeur/sections/")
    # On vérifie qu'il a déjà fait un tour au starting_point
    if json_site["general"]["starting_point"] == 0:
        return redirect(url_for('route_starting_point'))

    if request.method == "POST":
        utils.gestion_editeur(request, json_site, session['ja_id'])

    return render_template("editeur/full.html", data=json_site, sections=sections)

def starting_point():
    json_site = json.loads(open(f"tmp/{session['ja_id']}/site.json").read())

    if request.method == "POST":
        utils.gestion_editeur(request, json_site, session['ja_id'])
        return redirect(url_for('route_beta'))

    return render_template("editeur/setup.html", data=json_site)

def hebergement(devlobdd):
    status_dict = {0: "Désactivé", 1: "Hébergé", 2: "En attente", 3: "Refusé"}
    if request.method == "POST" and request.form["heberger"] == "heberger":
        if not re.fullmatch(r"[a-z0-9]{1,15}", request.form["domain"]):
            return render_template("home/hebergement.html", error="Le nom de domaine doit contenir des lettres minuscules et ne doit avoir plus de 15 caractères")
        devlobdd.ask_hebergement(session['ja_id'])
        devlobdd.set_domain_name(session['ja_id'], request.form["domain"])

    site = json.loads(open(f"tmp/{session['ja_id']}/site.json").read())
    print(site, "JSON")
    return render_template("home/hebergement.html", status=status_dict[site["general"]["statut"]], domain=site["general"]["domain"])


def preview(ja_id):
    json_site = json.loads(open(f"tmp/{ja_id}/site.json").read())
    return render_template("layouts/preview.html", data=json_site)


def account(db):
    if request.method == 'GET':
        account_infos = db.get_ja_byid(session['ja_id'])
        return render_template('home/account.html', account_infos=account_infos)
    elif request.method == 'POST':
        account_infos_old = db.get_ja_byid(session['ja_id'])
        if request.form["password-2"] != "" and request.form["password-1"] != "" \
            and request.form["password-2"] == request.form["password-2"]:
            hashed_password = hashpw(request.form["password-2"].encode("utf-8"), gensalt())
            db.change_password(ja_id=session['ja_id'], password=hashed_password)
            print('password_change')

        if request.form["email"] != "" and request.form["email"] != account_infos_old[3]:
            db.change_email(session['ja_id'], request.form["email"])
            utils.etape_verification(db, session['ja_id'])

        account_infos = db.get_ja_byid(session['ja_id'])
        return render_template('home/account.html', account_infos=account_infos)
