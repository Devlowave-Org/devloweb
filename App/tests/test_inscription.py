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


def test_mauvais_code_verif():
    response = app.test_client().post('/verification', data={
        "ja_id": "JA-8166",
        "verif": 1234
    })
    assert response.status_code == 200
    assert devlobdd.get_ja_by_mail("timtonix@icloud.com")[4] == 0


def test_code_verification():
    code = devlobdd.get_code_via_jaid("8166")
    response = app.test_client().post('/verification', data={
        "ja_id": "JA-8166",
        "verif": code[1]
    })
    assert response.status_code == 302
    # Le compte existe et il est activé
    assert devlobdd.get_ja_by_mail("timtonix@icloud.com")[4] == 1

