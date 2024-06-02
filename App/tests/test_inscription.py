import os
import time
from datetime import datetime
from App.utils.bdd import DevloBDD
import pytest
from devloapp import app

app.which = "devlotest"
os.system("rm -rf ~/PycharmProjects/devloweb/devlotest.db")
@pytest.fixture()
def devlobdd():
    return DevloBDD("devlotest")

def test_mauvais_id(devlobdd):
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


def test_good_inscription(devlobdd):
    devlobdd.delete_ja("timtonix@icloud.com")
    response = app.test_client().post('/inscription', data={
        "email": "timtonix@icloud.com",
        "ja_id": "JA-8166",
        "password": "jesuisunebananeavecdespouvoirsmagiques"  # +12 caractères
    })
    assert response.status_code == 302
    assert devlobdd.get_ja_by_mail("timtonix@icloud.com") is not None
    # Le compte existe et il est pas activé
    assert devlobdd.get_ja_by_mail("timtonix@icloud.com")[4] == 0


def test_account_already_exists():
    response = app.test_client().post('/inscription', data={
        "email": "timtonix@icloud.com",
        "ja_id": "JA-8166",
        "password": "jesuisuneAUTREbananeavecdespouvoirsmagiques"  # -12 caractères
    })
    assert response.status_code == 200
    assert 'Vous avez déjà un compte' in response.data.decode('utf-8')


def req_code_verif(ja_id, code):
    resp = app.test_client().post('/verification', data={
        "ja_id": ja_id,
        "verif": code
    })
    return resp


def test_mauvais_code_verif(devlobdd):
    response = req_code_verif("JA-8166", 1234)

    assert response.status_code == 200
    assert devlobdd.get_ja_by_mail("timtonix@icloud.com")[4] == 0
    assert devlobdd.get_try("127.0.0.1")[1] == 1


def test_punition_verif_code(devlobdd):
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


def test_code_verif_after_punished(devlobdd):
    # Bon en gros on reset pas la BDD après la punition ci-dessus. Et donc meme si on à le bon code ça marche pas
    code = devlobdd.get_code_via_jaid("8166")[1]
    response = req_code_verif("JA-8166", code)
    assert devlobdd.get_try("127.0.0.1")[1] == 5
    assert devlobdd.get_ja_by_mail("timtonix@icloud.com")[4] == 0
    assert response.status_code == 200



def test_good_code_verification(devlobdd):
    devlobdd.delete_try("127.0.0.1")
    code = devlobdd.get_code_via_jaid("8166")[1]
    response = req_code_verif("JA-8166", code)
    assert response.status_code == 302
    # Le compte existe et il est activé
    assert devlobdd.get_ja_by_mail("timtonix@icloud.com")[4] == 1
    # On vérifie que le code a bien été supprimé
    code = devlobdd.get_code_via_jaid("8166")
    assert code is None


def test_already_activated_ja(devlobdd):
    devlobdd.delete_try("127.0.0.1")
    code = devlobdd.get_code_via_jaid("8166")
    assert code is None


@pytest.mark.slow
def test_wait_punition_time(devlobdd):
    # On l'inscrit
    test_good_inscription(devlobdd)
    # On attend 30 minutes après la punition et on peut ensuite activer le compte
    test_punition_verif_code(devlobdd)
    # On désactive la JA manuellement au cas ou elle  était déjà ativé à cause du test du dessus
    devlobdd.desactiver_ja("JA-8166")
    time.sleep(1810)
    code = devlobdd.get_code_via_jaid("8166")[1]
    response = req_code_verif("JA-8166", 1234)
    assert devlobdd.get_try("127.0.0.1")[1] == 1
    response = req_code_verif("JA-8166", code)
    # Il ne s'active pas car le code a plus de 30 minutes
    assert response.status_code == 200
    # Le compte existe et il n'est pas activé
    assert devlobdd.get_ja_by_mail("timtonix@icloud.com")[4] == 0


@pytest.mark.slow
def test_reset_try(devlobdd):
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


def req_connection(mail, password):
    resp = app.test_client().post('/connexion', data={
        "email": mail,
        "password": password
    })
    return resp


def test_bad_mail_connexion(devlobdd):
    devlobdd.delete_try("127.0.0.1")
    resp = req_connection("jambon@.com", "azertyuiopqsdfghjklm")
    assert resp.status_code == 200
    assert devlobdd.get_try("127.0.0.1") is None
    assert "Veuillez rentrer un vrai email" in resp.data.decode("utf-8")

    # Ici le mail est bon dans sa forme mais n'a pas de compte
    resp = req_connection("timtonix@gmail.com", "azertyuiopqsdfghjklm")
    assert resp.status_code == 200
    assert devlobdd.get_try("127.0.0.1")[1] == 1
    assert "Mail ou mot de passe incorrect" in resp.data.decode("utf-8")



def test_wrong_password_connection(devlobdd):
    devlobdd.delete_try("127.0.0.1")
    resp = req_connection("timtonix@icloud.com", "azertyuiopqsdfghjklm")
    assert resp.status_code == 200
    assert "Mail ou mot de passe incorrect" in resp.data.decode("utf-8")
    assert devlobdd.get_try("127.0.0.1")[1] == 1


def test_good_connection(devlobdd):
    devlobdd.delete_try("127.0.0.1")
    resp = req_connection("timtonix@icloud.com", "jesuisunebananeavecdespouvoirsmagiques")
    assert resp.status_code == 302
    assert devlobdd.get_try("127.0.0.1") is None


@pytest.mark.slow
def test_ask_new_code(devlobdd):
    devlobdd.reset_bdd()
    devlobdd.__init__("devlotest")
    # On simule une inscritpion
    test_good_inscription(devlobdd)
    assert devlobdd.get_code_via_jaid("JA-8166") is not None
    code = devlobdd.get_code_via_jaid("JA-8166")[1]
    resp = app.test_client().post('/resend', data={
        "ja_id": "JA-8166"
    })
    assert resp.status_code == 200
    # On vérifie que le code n'a pas changé
    assert devlobdd.get_code_via_jaid("JA-8166")[1] == code
    time.sleep(120)
    resp = app.test_client().post('/resend', data={
        "ja_id": "JA-8166"
    })
    # Le code a bien été mis à jour
    assert devlobdd.get_code_via_jaid("JA-8166")[1] != code
    assert devlobdd.get_ja_by_mail("timtonix@icloud.com")[4] == 0
    # Et on vérifie qu'elle s'active bien avec le nouveau code
    test_good_code_verification()


def test_ask_new_code_already_active(devlobdd):
    devlobdd.reset_bdd()
    devlobdd.__init__("devlotest")
    # On simule une inscritpion
    test_good_inscription(devlobdd)
    test_good_code_verification(devlobdd)
    resp = app.test_client().post('/resend', data={
        "ja_id": "JA-8166"
    })
    # On ne lui a pas crée de nouveau code
    assert devlobdd.get_code_via_jaid("JA-8166") is None
    assert resp.status_code == 200
    assert 'Votre JA est déjà activée' in resp.data.decode('utf-8')





