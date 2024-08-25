from requests import request


def get_ja(ja_id) -> dict:
    return request("GET", f"https://api.devloweb.site/row/{ja_id}").json()


def ja_exists(ja_id):
    ja = get_ja(ja_id)
    try:
        if ja["message"] == "Internal Server Error":
            return False

    except KeyError:
        pass

    try:
        if ja["id"] == int(ja_id):
            return ja
    except KeyError:
        return False

