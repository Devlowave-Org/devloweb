"""IMPORTS"""
from flask import request, render_template, session, redirect, flash, url_for
from App.utils import bdd, utils
import re



"""UTILS FUNCTIONS"""
def website_status_reader(devlobdd, ja_id):
    print(ja_id)
    if ja_id:
        website_status = devlobdd.get_website_status_based_on_ja_id(ja_id)[0]

        if website_status is None:
            return "Not available"
        elif website_status == 0:
            return "disabled"
        elif website_status == 1:
            return "checked disabled"
        elif website_status == 2:
            return "Website submitted but not approved yet"
        elif website_status == 3:
            return "Website disapproved"
        else:
            return "Error"


def checkbox_parameter_setter_based_on_website_status(website_status):
    if website_status is "Website disapproved" or website_status is "Website submitted but not approved yet":
        checkbox_parameters = "disabled"
    else:
        checkbox_parameters = website_status

    return checkbox_parameters


def all_ja_with_website_getter(devlobdd):
    all_ja_ids = devlobdd.all_ja_with_website_getter()
    all_ja_ids = [int(t[0]) for t in all_ja_ids]
    return all_ja_ids