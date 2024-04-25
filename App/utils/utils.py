from re import fullmatch, compile
import random
from datetime import datetime, timedelta
import App.utils.email_api as email_api


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
    devlomail.send_verification_email(mail, code)

def create_verification_code(devlobdd: object) -> str:
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
        devlomail.send_verification_email(mail, code)
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
