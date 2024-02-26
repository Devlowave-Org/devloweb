from re import fullmatch, compile
from flask import render_template


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