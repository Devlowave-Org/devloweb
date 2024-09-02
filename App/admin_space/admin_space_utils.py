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
    "Ce site requiert",
    "Ce site a été désapprouvé",
    "Erreur"
]


"""UTILS FUNCTIONS"""
def query_parameter_getter():
        query = request.args.get('query')

        if query is None or query == '':
            return ADMIN_SPACE_UTILS_FLAGS[0]
        else:
            return query


def query_getter_and_checker(devlobdd):
    query_to_check = query_parameter_getter()
    all_ja_with_website = all_ja_with_website_getter(devlobdd)

    try:
        if re.match("^ja-[0-9]{2,5}$", query_to_check):
            query_to_check = int(utils.ja_id_only(query_to_check))
        elif re.match("^[0-9]{2,5}$", query_to_check):
            query_to_check = int(query_to_check)
        elif query_to_check is ADMIN_SPACE_UTILS_FLAGS[0]:
            return ADMIN_SPACE_UTILS_FLAGS[0]
        else:
            return ADMIN_SPACE_UTILS_FLAGS[1]

        if query_to_check not in all_ja_with_website:
            return ADMIN_SPACE_UTILS_FLAGS[3]
        else:
            return query_to_check

    except ValueError:
        return 1 # Flag number


def website_status_reader(devlobdd, ja_id):
    if ja_id:
        status = devlobdd.get_website_status_based_on_ja_id(ja_id)[0]

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