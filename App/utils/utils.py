import json
import os
from re import fullmatch, compile
import random
from datetime import datetime, timedelta
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
        raise ValueError(f"Invalid JA ID: {ja_id}")

def etape_verification(devlobdd, ja_id):
    ja = devlobdd.get_ja_byid(ja_id)
    mail = ja[1]
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

    if devlobdd.code_exists(code):
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
    if code == row[1] and delta.seconds < 1800:
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
def editeur_form_processing(form_dict: dict, json_site: dict, ja_id):

    for key in form_dict.keys():
        try:
            splited = key.split("-")
            if type(splited[0]) is int:
                raise ValueError("Utilisateur essaie de rentrer un integer au lieu d'un str")
            section = splited[0]

            try:
                splited[1] = int(splited[1])
            except ValueError:
                pass
            try:
                splited[2] = int(splited[2])
            except (ValueError, IndexError):
                pass

            if len(splited) >= 3:
                json_site[section][splited[1]][splited[2]] = form_dict[key]
            else:
                json_site[section][splited[1]] = form_dict[key]
        except (IndexError, ValueError, KeyError) as e:
            print("An error occurd in the first try " + str(e))

    with open(f"tmp/{ja_id}/site.json", "w") as f:
        json.dump(json_site, f)