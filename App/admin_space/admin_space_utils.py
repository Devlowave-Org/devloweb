"""IMPORTS"""
from flask import request, render_template, session, redirect, flash, url_for
from netaddr.ip.iana import query

from App.utils import bdd, utils
import re

"""FLAGS"""
ADMIN_SPACE_UTILS_FLAGS = [
    "Pas de requête",
    "Requête invalide",
    "Cette JA n'a pas de compte",
    "Erreur",
    "Vous n'êtes pas autorisé à accéder à cette page"
]

WEBSITE_STATUS_FLAGS=[
    "Ce site n'a pas encore été crée",
    "Ce site a été approuvé",
    "Ce site requiert une approbation",
    "Ce site a été désapprouvé",
    "Erreur"
]


"""UTILS FUNCTIONS"""
def get_parameter_getter(name):
        parameter = request.args.get(name)

        if parameter is None or parameter == '':
            return ADMIN_SPACE_UTILS_FLAGS[0]
        else:
            return parameter

def post_parameter_getter(name):
    parameter = request.form[name]
    if parameter is None or parameter == '':
        return None
    else:
        return parameter

def website_status_reader(devlobdd, ja_id):
    if ja_id:
        status = devlobdd.get_website_status_based_on_ja_id(ja_id)[0]
        print(status)

        if status is None:
            return WEBSITE_STATUS_FLAGS[0]
        else:
            return WEBSITE_STATUS_FLAGS[status]


def status_svg_selector(website_status):
    path_to_svg = "static/admin_space/images/website_status_icons/"
    if website_status == WEBSITE_STATUS_FLAGS[0]:
        return path_to_svg + "not_existing.svg"
    elif website_status == WEBSITE_STATUS_FLAGS[1]:
        return path_to_svg + "approved.svg"
    elif website_status == WEBSITE_STATUS_FLAGS[2]:
        return path_to_svg + "submitted.svg"
    elif website_status == WEBSITE_STATUS_FLAGS[3]:
        return path_to_svg + "disapproved.svg"
    elif website_status == WEBSITE_STATUS_FLAGS[4]:
        return ADMIN_SPACE_UTILS_FLAGS[4]
    else:
        return ADMIN_SPACE_UTILS_FLAGS[4]



def all_ja_with_website_getter(devlobdd):
    all_ja_ids = devlobdd.all_ja_with_website_getter()
    all_ja_ids = [int(t[0]) for t in all_ja_ids]
    return all_ja_ids