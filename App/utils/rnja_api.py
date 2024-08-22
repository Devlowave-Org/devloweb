from requests import request


def get_ja(ja_id) -> dict:
    return request("GET", f"https://api.devloweb.site/row/{ja_id}").json()


def ja_exists(ja_id):
    ja = get_ja(ja_id)
    try:
        if ja["message"] == "Internal Server Error":
            return False

        if ja["id"] == ja_id:
            return True
    except KeyError:
        return False


print(ja_exists("8166"))