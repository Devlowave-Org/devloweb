from re import fullmatch, compile
import random
from datetime import datetime, timedelta


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
    code_date = datetime.strptime(row[2], "%Y-%m-%d %H:%M:%S")
    delta = now - code_date
    print(delta.seconds)
    print(row)
    if code == row[1] and delta.seconds < 1800:
        return True
    else:
        return False


def add_a_try(devlobdd, ip):
    print("On ajoute un try")
    devlobdd.add_try(ip)
    user_security = devlobdd.get_try(ip)
    print(user_security)
    first = datetime.strptime(user_security[2], "%Y-%m-%d %H:%M:%S")
    last = datetime.strptime(user_security[3], "%Y-%m-%d %H:%M:%S")
    delta = last - first
    # On vérifie si le temps entre la première tentative et la derniere < 10 minutes
    if delta.seconds > 600:
        devlobdd.remove_try(ip)
        return True
    # Et maintenant si il a fait 5 try en <10 minutes on le punit pour 30
    if user_security[1] >= 5:
        print("On est sensé le punir")
        # voyons comment cela marche
        devlobdd.punish_try(ip, datetime.now() + timedelta(minutes=30))


def is_punished(devlobdd, ip):
    print("On vérifie si il est punit")
    user_security = devlobdd.get_try(ip)
    print(user_security)
    if not user_security:
        return False
    punition = datetime.strptime(user_security[4], "%Y-%m-%d %H:%M:%S")
    print(f"La punition : {punition}")
    delta = datetime.now() - punition
    print(f"Le delta de la punition : {delta.seconds}")
    if delta.seconds > 0:
        print("Il est punit")
        return True
    else:
        return False