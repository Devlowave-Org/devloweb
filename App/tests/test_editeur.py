import os
import pytest
from test_inscription import devlobdd, req_connection, req_code_verif
from devloapp import app, session

app.which = "devlotest"
os.system("rm -rf ~/PycharmProjects/devloweb/devlotest.db")


def setup_account(devlobdd):
    devlobdd.delete_ja("timtonix@icloud.com")
    app.test_client().post('/inscription', data={
        "email": "timtonix@icloud.com",
        "ja_id": "JA-8166",
        "password": "jesuisunebananeavecdespouvoirsmagiques"  # +12 caractères
    })
    code = devlobdd.get_code_via_jaid("8166")[1]
    req_code_verif("JA-8166", code)
    req_connection("timtonix@icloud.com", "jesuisunebananeavecdespouvoirsmagiques")


def test_editor_access_without_account():
    response = app.test_client().get('/home/editeur')
    assert response.status_code == 302

def test_good_editor_access(devlobdd):
    setup_account(devlobdd)
    response = app.test_client().get('/home/editeur')

    assert response.status_code == 200
