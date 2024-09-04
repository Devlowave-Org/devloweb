import re

from flask import request, render_template, session, redirect, flash, url_for
from App.utils import utils, cloudflare
import json


def index(devlobdd):
    return render_template('home/index.html')


def editeur():
    json_site = json.loads(open(f"tmp/{session['ja_id']}/site.json").read())
    print(json_site)

    if request.method == "POST":
        utils.gestion_editeur(request, json_site, session['ja_id'])

    return render_template("editor/beta/editeur.html", data=json_site)

def hebergement(devlobdd):
    status_dict = {0: "Désactivé", 1: "Hébergé", 2: "En attente", 3: "Refusé"}
    site = devlobdd.get_site_by_ja(session['ja_id'])
    if request.method == "POST" and request.form["heberger"] == "heberger":
        if not re.fullmatch(r"[a-z0-9]{1,15}", request.form["domain"]):
            return render_template("home/hebergement.html", error="Le nom de domaine doit contenir des lettres minuscules et ne doit avoir plus de 15 caractères")
        devlobdd.ask_hebergement(session['ja_id'])
        devlobdd.set_domain_name(session['ja_id'], request.form["domain"])

    return render_template("home/hebergement.html", status=status_dict[site[3]], domain=site[1])


def preview(ja_id):
    json_site = json.loads(open(f"tmp/{ja_id}/site.json").read())
    return render_template("sites/beta.html", data=json_site)


def account():
    return render_template('home/account.html')
