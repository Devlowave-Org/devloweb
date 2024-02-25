from re import fullmatch, compile
from flask import render_template

def email_validator(email: str) -> bool:
    regex = compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    if fullmatch(regex, email):
        return True
    else:
        return False


def ja_id_int(ja_id: str) -> int | str:
    try:
        ja_int = int(ja_id.split("-")[1])
        return ja_int
    except ValueError as e:
        return render_template("inscription.html", error=str(e))
