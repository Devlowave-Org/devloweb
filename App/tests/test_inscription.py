import time
from datetime import datetime

import pytest

from devloapp import app, devlobdd


def test_mauvais_id():
    response = app.test_client().post('/inscription', data={
        "email": "timtonix@icloud.com",
        "ja_id": "azerty?",
        "password": "aefkdnbùgkfxdgbmfvlkbeshf"
    })
    assert devlobdd.get_ja_by_mail("timtonix@icloud.com") is None
    assert response.status_code == 200
    assert b"Invalid JA ID" in response.data

def test_mauvais_mail():
    response = app.test_client().post('/inscription', data={
        "email": "timtoniicloud.com",
        "ja_id": "JA-8166",
        "password": "eqfliuherlughdslfher"
    })

    assert response.status_code == 200
    assert b"Veuillez remplir un email valide" in response.data


def test_mauvais_password():
    response = app.test_client().post('/inscription', data={
        "email": "timtonix@icloud.com",
        "ja_id": "JA-8166",
        "password": "azerty..."  # -12 caractères
    })

    assert response.status_code == 200
    assert 'Veuillez avoir un mot de passe d&#39;au moins 12 caractères'.encode("utf-8") in response.data

def test_champ_manquant():
    response = app.test_client().post('/inscription', data={
        "email": "timtonix@icloud.com",
        "ja_id": "JA-8166",
        "password": ""  # -12 caractères
    })

    assert response.status_code == 200
    assert 'Veuillez remplir tous les champs'.encode("utf-8") in response.data


def test_inscription():
    devlobdd.delete_ja("timtonix@icloud.com")
    response = app.test_client().post('/inscription', data={
        "email": "timtonix@icloud.com",
        "ja_id": "JA-8166",
        "password": "jesuisunebananeavecdespouvoirsmagiques"  # -12 caractères
    })
    assert response.status_code== 302
    assert devlobdd.get_ja_by_mail("timtonix@icloud.com") is not None
    # Le compte existe et il est pas activé
    assert devlobdd.get_ja_by_mail("timtonix@icloud.com")[4] == 0

def req_code_verif(ja_id, code):
    resp = app.test_client().post('/verification', data={
        "ja_id": ja_id,
        "verif": code
    })
    return resp

def test_mauvais_code_verif():
    response = req_code_verif("JA-8166", 1234)

    assert response.status_code == 200
    assert devlobdd.get_ja_by_mail("timtonix@icloud.com")[4] == 0
    assert devlobdd.get_try("127.0.0.1") is not None

def test_punition_verif_code():
    devlobdd.delete_try("127.0.0.1")
    response = req_code_verif("JA-8166", 1234)
    assert response.status_code == 200
    assert devlobdd.get_try("127.0.0.1")[1] == 1
    response = req_code_verif("JA-8166", 1234)
    response = req_code_verif("JA-8166", 1234)
    response = req_code_verif("JA-8166", 1234)
    assert devlobdd.get_try("127.0.0.1")[1] == 4
    response = req_code_verif("JA-8166", 1234)
    assert devlobdd.get_try("127.0.0.1")[1] == 5
    punish_date = datetime.strptime(devlobdd.get_try("127.0.0.1")[4], "%Y-%m-%d %H:%M:%S.%f")
    delta = punish_date - datetime.now()
    assert punish_date > datetime.now()
    assert 1700 < delta.seconds < 1900
    response = req_code_verif("JA-8166", 1234)
    response = req_code_verif("JA-8166", 1234)
    assert devlobdd.get_try("127.0.0.1")[1] == 5


def test_code_verif_after_punished():
    # Bon en gros on reset pas la BDD après la punition ci-dessus. Et donc meme si on à le bon code ça marche pas
    code = devlobdd.get_code_via_jaid("8166")[1]
    response = req_code_verif("JA-8166", code)
    assert devlobdd.get_ja_by_mail("timtonix@icloud.com")[4] == 0
    assert response.status_code == 200


def test_code_verification():
    devlobdd.delete_try("127.0.0.1")
    code = devlobdd.get_code_via_jaid("8166")[1]
    response = req_code_verif("JA-8166", code)
    assert response.status_code == 302
    # Le compte existe et il est activé
    assert devlobdd.get_ja_by_mail("timtonix@icloud.com")[4] == 1


@pytest.mark.long
def test_wait_punition_time():
    test_punition_verif_code()
    time.sleep(1810)
    code = devlobdd.get_code_via_jaid("8166")[1]
    response = req_code_verif("JA-8166", 1234)
    assert devlobdd.get_try("127.0.0.1")[1] == 1
    response = req_code_verif("JA-8166", code)
    assert response.status_code == 302
    # Le compte existe et il est activé
    assert devlobdd.get_ja_by_mail("timtonix@icloud.com")[4] == 1

@pytest.mark.long
def test_reset_try():
    devlobdd.delete_try("127.0.0.1")
    response = req_code_verif("JA-8166", 1234)
    assert response.status_code == 200
    assert devlobdd.get_try("127.0.0.1")[1] == 1
    response = req_code_verif("JA-8166", 1234)
    response = req_code_verif("JA-8166", 1234)
    assert devlobdd.get_try("127.0.0.1")[1] == 3
    time.sleep(610)
    response = req_code_verif("JA-8166", 1234)
    assert devlobdd.get_try("127.0.0.1")[1] == 1
