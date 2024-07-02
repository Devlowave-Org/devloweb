from App import onthefly
from test_inscription import devlobdd

def test_valid_domain(devlobdd, client):
    # Inscription terminée et domaine sélectionné
    ja_site = devlobdd.get_ja_by_domain('devlowave')
    assert ja_site[0] == "8166"
    assert client.get('ja/invalid').status_code == 200

def test_invalid_domain(devlobdd, client):
    ja_site = devlobdd.get_ja_by_domain('invalid')
    assert ja_site is None
    assert client.get('ja/invalid').status_code == 404
