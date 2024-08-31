"""IMPORTS"""
from flask import request, render_template, session, redirect, flash, url_for
from App.utils import bdd, utils
import re



"""UTILS FUNCTIONS"""
def query_parameter_getter():
        query = request.args.get('query')

        if query is not None:
           return query
        else:
            return "No query"


def query_getter_and_checker(devlobdd):
    query_to_check = query_parameter_getter()
    all_ja_with_website = all_ja_with_website_getter(devlobdd)

    try:
        if re.match("^ja-[0-9]{2,5}$", query_to_check):
            query_to_check = int(utils.ja_id_only(query_to_check))
        elif re.match("^[0-9]{2,5}$", query_to_check):
            query_to_check = int(query_to_check)
        elif query_to_check is "" or query_to_check is "No query":
            return "No query"
        else:
            return "Invalid query"

        if query_to_check not in all_ja_with_website:
            return "Ja does not exist nor have a website"
        else:
            return query_to_check

    except ValueError:
        return "Invalid query"


def website_status_reader(devlobdd, ja_id):
    if ja_id:
        website_status = devlobdd.get_website_status_based_on_ja_id(ja_id)[0]

        if website_status is None:
            return "Not available"
        elif website_status == 0:
            return "Not created yet"
        elif website_status == 1:
            return "Up and running"
        elif website_status == 2:
            return "Website submitted but not approved yet"
        elif website_status == 3:
            return "Website disapproved"
        else:
            return "Error"


def checkbox_parameter_setter_based_on_website_status(website_status):
    if website_status is "Website disapproved" or website_status is "Website submitted but not approved yet" or website_status is "Not created yet":
        checkbox_parameters = "disabled"
    elif website_status is "Up and running":
        checkbox_parameters = "checked disabled"

    return checkbox_parameters


def all_ja_with_website_getter(devlobdd):
    all_ja_ids = devlobdd.all_ja_with_website_getter()
    all_ja_ids = [int(t[0]) for t in all_ja_ids]
    return all_ja_ids