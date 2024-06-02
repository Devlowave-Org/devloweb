import os
import time
from datetime import datetime
from App.utils.bdd import DevloBDD
import pytest
from test_inscription import devlobdd
from devloapp import app

app.which = "devlotest"
os.system("rm -rf ~/PycharmProjects/devloweb/devlotest.db")


def test_pof_access(devlobdd):
    response = app.test_client().get('/pof')
    assert response.status_code == 302