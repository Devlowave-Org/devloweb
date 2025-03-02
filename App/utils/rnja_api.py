from requests import request


def get_ja(ja_id) -> dict:
    return {
            "name": "Nom de l'entreprise",
            "description": "Description de l'entreprise",
            "twitter": "https://twitter.com/entreprise",
            "facebook": "https://facebook.com/entreprise",
            "instagram": "https://instagram.com/entreprise",
            "linkedin": "https://linkedin.com/entreprise",
            "website": "https://entreprise.com",
            "tiktok": "https://tiktok.com/entreprise",
            "youtube": "https://youtube.com/entreprise",
            "discord": "https://discord.gg/entreprise",
        }
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

