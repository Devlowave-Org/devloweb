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
from App.utils.rnja_api import get_ja, ja_exists


def is_connected(session, devlobdd):
    if session.get('ja_id') is None:
        return False

    if not devlobdd.ja_exists(session.get('ja_id')):
        session.clear()
        return False

    return True

def is_admin(session, devlobdd):
    print(session.get("admin"))
    if session.get('admin') == 1:
        return True
    return False


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
    print("fait")


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
    print(row)
    mail = devlobdd.get_ja_byid(ja_id=row[1])[3]

    delta = datetime.now() - create_date
    if delta.seconds < 120:
        return False
    else:
        code = create_verification_code(devlobdd)
        devlobdd.update_code(row[0], code)
        devlomail = email_api.DevloMail()
        mailer_thread = Thread(target=devlomail.verification_email, args=(mail, code))
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
        if not os.listdir(folder_path):  # Vérifie que le dossier est vide
            shutil.copytree(base_path, folder_path, dirs_exist_ok=True)
        else:
            print("Le dossier n'est pas vide, donc rien n'a été copié.")
    except RuntimeError:
        print("Une erreur s'est produite")


"""
Gestion de l'éditeur
"""
def set_value_recursively(json_site, keys, value):
    print(f"Voici nos clés {keys}")
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
    # Car oui, on vérifie qu'a ce moment, json_site est une liste.
    if key.isdigit():
        key = int(key)
        if not isinstance(json_site, list) or key >= len(json_site):
            raise ValueError("Index invalide pour une liste.")

    # Si c'est le dernier segment, on met la valeur str
    if len(keys) == 1 and key in json_site:
        json_site[key] = value
        return

    # Ici pour l'entier
    if len(keys) == 1 and isinstance(json_site, list):
        json_site[key] = value
        return

    # Navigue dans la structure imbriquée et appelle récursivement
    if isinstance(json_site, dict) and key in json_site:
        set_value_recursively(json_site[key], keys[1:], value)
    elif isinstance(json_site, list) and isinstance(key, int):
        set_value_recursively(json_site[key], keys[1:], value)
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

    # Gestion des sections
    if "general-sections" in form_dict.keys():
        section_list = form_dict["general-sections"].split("+")
        for i, section in enumerate(section_list):
            form_dict[f"general-sections-{i}"] = section
        form_dict.pop("general-sections")

    for key, value in form_dict.items():
        print(f"Traitement de la clé {key} avec valeur : {value}")
        try:
            splited_keys = key.split("-")

            # Ajout dynamique de membres
            if "members-list" in key and splited_keys[2].isdigit():
                # SI le tableau fait la meme taille que l'index on rajoute une case
                if len(json_site["members"]["list"]) == int(splited_keys[2]) and value is not '':
                    json_site["members"]["list"].append({"image": "", "role": "", "name": ""})

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
        print(f"Traintement de l'image de {key} : {file.filename}.")
        if file.filename == '':
            continue

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filename = nice_filename(filename, key)
            print(filename)
            try:
                splited_keys = key.split("-")
                set_value_recursively(json_site, splited_keys, filename)
                file.save(os.path.join(f"tmp/{ja_id}/", filename))
                print(f"Fichier enregistré {key}")
            except (KeyError, ValueError) as e:
                print(f"Erreur lors de la mise à jour pour {key}: {e}")
        else:
            print("Fichier non autorisé")

    return json_site


def set_default_value_to_json_site(ja_id):
    ja_from_api = get_ja(ja_id)

    json_site = json.loads(open(f"tmp/{ja_id}/site.json").read())
    json_site["general"]["ja_id"] = ja_id
    json_site["general"]["theme"] = "lemonade"
    json_site["general"]["sections"] = ["nav_section", "hero_section", "footer_section", "", ""]
    json_site["general"]["starting_point"] = 0

    json_site["nav"]["ja"] = ja_from_api["name"]
    json_site["hero"]["title"] = ja_from_api["name"]
    json_site["hero"]["description"] = ja_from_api["description"]

    json_site["footer"]["socials"]["twitter"] = ja_from_api["twitter"]
    json_site["footer"]["socials"]["facebook"] = ja_from_api["facebook"]
    json_site["footer"]["socials"]["instagram"] = ja_from_api["instagram"]
    json_site["footer"]["socials"]["youtube"] = ja_from_api["youtube"]
    json_site["footer"]["socials"]["discord"] = ja_from_api["discord"]
    json_site["footer"]["socials"]["tiktok"] = ja_from_api["tiktok"]
    json_site["footer"]["socials"]["website"] = ja_from_api["website"]

    with open(f"tmp/{ja_id}/site.json", "w") as f:
        json.dump(json_site, f)


def create_session(ja_id, ja_name, ip, email, admin):
    from flask import session
    session['email'] = email
    session['ip'] = ip
    session['ja_id'] = ja_id
    session['name'] = ja_name
    session["admin"] = admin
    session['avatar'] = "general-logo-image"