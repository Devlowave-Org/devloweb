from devloapp import app

def test_mauvais_id():
    response = app.test_client().post('/inscription', data={
        "email": "timtonix@icloud.com",
        "ja_id": "azerty?",
        "password": "aefkdnbùgkfxdgbmfvlkbeshf"
    })

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

def test_simple():
    response = app.test_client().get("/")
    assert b"Hello World" in response.data

