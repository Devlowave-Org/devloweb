from flask import request, render_template, session, redirect, flash, url_for
from App.admin_space.admin_space_utils import website_status_reader, ADMIN_SPACE_UTILS_FLAGS, WEBSITE_STATUS_FLAGS, \
    post_parameter_getter
import App.home as home
from App.utils import bdd, utils
import re

"""MAIN FUNCTION"""
def load_website_details(devlobdd, ja_id):
    try:
        if ja_id:
            ja_name = devlobdd.get_ja_name_by_id(ja_id)[0]
            website_domain = devlobdd.get_website_domain_based_on_ja_id(ja_id)[0]
            website_status = website_status_reader(devlobdd, ja_id)
            is_demand_active = is_demand_active_checker(website_status)
            print(is_demand_active)

            if is_demand_active:
                apply_process_demand(devlobdd, ja_id)

            website_status = website_status_reader(devlobdd, ja_id)
            is_demand_active = is_demand_active_checker(website_status)
            print(is_demand_active)
            error = None
            url = home.preview(ja_id)

            website_infos = [ja_name, website_domain, website_status, is_demand_active, error, url]
        else:
            website_infos = None
    except TypeError:
        website_infos = ["Cet ID de JA ne correspond à aucun compte"]

    return website_infos

"""UTILS (FOR THE DETAILS)"""
def is_demand_active_checker(website_status):
    if website_status == WEBSITE_STATUS_FLAGS[2]:
        return True
    else:
        return None


def apply_process_demand(devlobdd, ja_id):
    demand = post_parameter_getter('process_demand')
    print(demand)
    if demand == "Rejeter":
        devlobdd.update_website_status_based_on_ja_id(3, ja_id)
    elif demand == "Accepter":
        devlobdd.update_website_status_based_on_ja_id(1, ja_id)
