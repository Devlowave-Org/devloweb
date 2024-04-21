from devloapp import app



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
    assert devlobdd.get_ja_by_mail("timtonix@icloud.com") == ('8166', 'timtonix@icloud.com', b'$2b$12$40xDYE0d0naHJaHWcrCtYOKg4Z.ej2tqah4G2qco7NUXW6m6N.1Oq', '2024-04-21 16:29:28', 0)

def test_code_verification():
    code = devlobdd.get_code_via_jaid("8166")
    response = app.test_client().post('/verification', data={
        "ja_id": "JA-8166",
        "verif": code[1]
    })

    assert devlobdd.get_ja_by_mail("timtonix@icloud.com") == (
    '8166', 'timtonix@icloud.com', b'$2b$12$40xDYE0d0naHJaHWcrCtYOKg4Z.ej2tqah4G2qco7NUXW6m6N.1Oq',
    '2024-04-21 16:29:28', 1)
