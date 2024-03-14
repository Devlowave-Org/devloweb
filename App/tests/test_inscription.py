from devloapp import app

def test_mauvais_id():
    response = app.test_client().post('/inscription', data={
        "email": "timtonix@icloud.com",
        "ja_id": "azerty?",
        "password": "aefkdnbùgkfxdgbmfvlkbeshf"
    })
    print(response.status_code)

    assert response.status_code == 200
    assert b"Invalid JA ID" in response.data


def test_simple():
    response = app.test_client().get("/")
    assert b"Hello World" in response.data

