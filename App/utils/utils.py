import json
import os
from re import fullmatch, compile
import random
from datetime import datetime, timedelta

import flask
from werkzeug.utils import secure_filename

import App.utils.email_api as email_api
from threading import Thread
import shutil


def is_connected(session, devlobdd):
    if session.get('ja_id') is None:
        return False
    if not devlobdd.ja_exists(session.get('ja_id')):
        print(f"ON DÉCONNECTE {session['ja_id']} !")
        session.clear()
        return False
    return True


def email_validator(email: str) -> bool:
    regex = compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    if fullmatch(regex, email):
        return True
    else:
        return False


def ja_id_only(ja_id: str) -> str:
    try:
        ja_id = ja_id.split("-")[1]
        return ja_id
    except (ValueError, IndexError) as e:
        raise ValueError(f"Identifiant de JA invalide : {ja_id}")

def etape_verification(devlobdd, ja_id):
    ja = devlobdd.get_ja_byid(ja_id)
    mail = ja[3]
    code = create_verification_code(devlobdd)
    store_code(devlobdd, ja_id, code)
    devlomail = email_api.DevloMail()
    mailer_thread = Thread(target=devlomail.verification_email, args=(mail, code))
    mailer_thread.start()


def create_verification_code(devlobdd) -> str:
    length = 4
    code = ""
    for i in range(length):
        code += str(random.randint(0, 9))

    if devlobdd.back_code_exists(code):
        create_verification_code(devlobdd)
    return code


def store_code(devlobdd, ja_id, code):
    devlobdd.store_code(ja_id, code)


def verif_code(devlobdd, ja_id, code):
    row = devlobdd.get_code_via_jaid(ja_id)

    if not row:
        return False

    now = datetime.now()
    code_date = datetime.strptime(row[2], "%Y-%m-%d %H:%M:%S.%f")
    delta = now - code_date
    print(delta.seconds)
    print(row)
    # Le code est valable 30 minutes
    if code == row[0] and delta.seconds < 1800:
        return True
    else:
        return False


def update_verif_code(devlobdd, row):
    create_date = datetime.strptime(row[2], "%Y-%m-%d %H:%M:%S.%f")
    mail = devlobdd.get_ja_byid(ja_id=row[0])[0]

    delta = datetime.now() - create_date
    if delta.seconds < 120:
        return False
    else:
        code = create_verification_code(devlobdd)
        devlobdd.update_code(row[0], code)
        devlomail = email_api.DevloMail()
        mailer_thread = Thread(target=devlomail.send_verification_email, args=(mail, code))
        mailer_thread.start()
        return True


def add_a_try(devlobdd, ip):
    print("On lui ajoute un try")
    devlobdd.add_try(ip)

    user_security = devlobdd.get_try(ip)
    first = datetime.strptime(user_security[2], "%Y-%m-%d %H:%M:%S.%f")
    last = datetime.strptime(user_security[3], "%Y-%m-%d %H:%M:%S.%f")
    delta = last - first
    # On vérifie si le temps entre la première tentative et la derniere > 10 minutes
    if delta.seconds > 600:
        devlobdd.reset_try(ip)
        return True
    # Et maintenant si il a fait 5 try en <10 minutes on le punit pour 30
    if user_security[1] >= 5:
        print(f"Il sera punit de {datetime.now() + timedelta(minutes=30)}")
        # voyons comment cela marche

        devlobdd.punish_try(ip, datetime.now() + timedelta(minutes=30))


def is_punished(devlobdd, ip):
    print("On vérifie si il est punit")
    user_security = devlobdd.get_try(ip)
    print(user_security)
    if not user_security:
        return False
    punition = datetime.strptime(user_security[4], "%Y-%m-%d %H:%M:%S.%f")
    """
    La date de la punition doit être plus grande que la date actuelle pour prouver qu'il est punit.
    """
    print(f"Voilà ce qu'on test : {punition} > {datetime.now()} = {punition > datetime.now()}")
    if punition > datetime.now():
        print("Il est punit")
        return True
    return False


def magic_link(devlobdd, ja_id, mail):
    """
    Crée un code
    Le stock
    Demande l'envoie d'un mail
    """
    length = 8
    code = ""
    for i in range(length):
        code += str(random.randint(0, 9))

    if devlobdd.magic_link_exists(code):
        magic_link(devlobdd, ja_id, mail)

    devlobdd.store_magic_link(code, ja_id)
    devlomail = email_api.DevloMail()
    mailer_thread = Thread(target=devlomail.magic_link_mail, args=(mail, code))
    mailer_thread.start()


"""
Création du dossier JA
"""
def create_ja_folder(jaid):
    folder_path = os.path.join(os.getcwd(), "tmp/" + str(jaid))
    base_path = os.path.join(os.getcwd(), "ressources/base/")
    print("création du dossier JA : ", folder_path)
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)

    try:
        shutil.copytree(base_path, folder_path, dirs_exist_ok=True)
    except RuntimeError:
        print("Une erreur s'est produite")


"""
Gestion de l'éditeur
"""
def set_value_recursively(dictionary, keys, value):
    """
    Fonction récursive pour définir une valeur dans un dictionnaire imbriqué.

    dictionary : dictionnaire de base
    keys : liste de segments de clé
    value : valeur à insérer

    from : https://chatgpt.com/share/5fc613c9-8e62-46c8-998c-1892688deec2
    doc : key[1:] donne la prochaine clé
    """
    # Premier segment de la clé
    key = keys[0]

    # Si le segment est un index numérique (pour une liste)
    if key.isdigit():
        key = int(key)
        if not isinstance(dictionary, list) or key >= len(dictionary):
            raise ValueError("Index invalide pour une liste.")

    # Si c'est le dernier segment, on met la valeur
    if len(keys) == 1:
        dictionary[key] = value
        return

    # Navigue dans la structure imbriquée et appelle récursivement
    if isinstance(dictionary, dict) and key in dictionary:
        set_value_recursively(dictionary[key], keys[1:], value)
    elif isinstance(dictionary, list) and isinstance(key, int):
        set_value_recursively(dictionary[key], keys[1:], value)
    else:
        raise KeyError(f"Clé introuvable : {key}")


def gestion_editeur(request: flask.Request, json_site: dict, ja_id):
    json_site = gestion_texte(request, json_site)
    json_site = gestion_fichiers(request, json_site, ja_id)

    # Enregistrement du dictionnaire dans le fichier JSON
    print(f"SITE À JOUR{json_site}")
    with open(f"tmp/{ja_id}/site.json", "w") as f:
        json.dump(json_site, f)


def gestion_texte(request: flask.Request, json_site: dict):
    form_dict = request.form.to_dict()

    # Gestion des sections (car le script JS c'est pas hyper abouti quoi...
    if "general-section" in form_dict.keys():
        section_list = form_dict["general-sections"].split("+")
        for i, section in enumerate(section_list):
            form_dict[f"general-sections-{i}"] = section
        form_dict.pop("general-sections")

    for key, value in form_dict.items():
        print(f"Traitement de la clé {key} avec valeur : {value}")
        try:
            splited_keys = key.split("-")
            set_value_recursively(json_site, splited_keys, value)
        except (KeyError, ValueError) as e:
            print(f"Erreur lors de la mise à jour pour {key}: {e}")

    return json_site

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'mov'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def nice_filename(filename, key):
    filename = filename.rsplit('.', 1)
    print(filename)
    filename[0] = key
    return filename[0] + '.' + filename[1]


def gestion_fichiers(request: flask.Request, json_site: dict, ja_id):
    for key in request.files.keys():
        # On oblige à ce que la clée soit une image sinon on peut mettre des images partout
        if "image" not in key:
            continue
        file = request.files[key]
        if file.filename == '':
            continue

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filename = nice_filename(filename, key)
            print(filename)
            try:
                splited_keys = key.split("-")
                set_value_recursively(json_site, splited_keys, filename)
            except (KeyError, ValueError) as e:
                print(f"Erreur lors de la mise à jour pour {key}: {e}")
            file.save(os.path.join(f"tmp/{ja_id}/", filename))
        else:
            print("Fichier non autorisé")
        print(f"Fichier enregistré {key}")

    return json_site