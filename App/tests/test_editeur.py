import json
import os
import pytest
from test_inscription import devlobdd, req_connection, req_code_verif
from flask import session


def setup_account(client, devlobdd):
    devlobdd.delete_ja("timtonix@icloud.com")
    client.post('/inscription', data={
        "email": "timtonix@icloud.com",
        "ja_id": "JA-8166",
        "password": "jesuisunebananeavecdespouvoirsmagiques"  # +12 caractères
    })
    code = devlobdd.get_code_via_jaid("8166")[1]
    req_code_verif(client, "JA-8166", code)
    req_connection(client, "timtonix@icloud.com", "jesuisunebananeavecdespouvoirsmagiques")


def test_editor_access_without_account(client):
    response = client.get('/home/editeur')
    assert response.status_code == 302


def test_good_editor_access(client, devlobdd):
    setup_account(client, devlobdd)
    response = client.get('/home/editeur')

    assert response.status_code == 200

def test_modify_site(client, devlobdd):
    with client.session_transaction() as c:
        c["ja_id"] = "8166"
        c["email"] = "timtonix@icloud.com"
        c["ip"] = "127.0.0.1"
        c["avatar"] = "https://gravatar.com/avatar/8166.png?d=mp"

    response = client.post('/editeur/pof', data={
        "titre": "test",
        "valeur1": "test",
        "valider": ""
    })


    json_site = json.loads(open(f"tmp/8166/site.json").read())

    assert response.status_code == 200
    assert json_site["titre"] == "test"
    assert json_site["valeur1"] == "test"