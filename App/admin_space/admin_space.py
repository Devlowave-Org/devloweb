"""IMPORTS"""
from calendar import error

from flask import request, render_template, session, redirect, flash, url_for

from App.admin_space.search_engine import search
from App.admin_space.website_validator import get_submit_demand
from App.utils import bdd, utils
from App.admin_space import search_engine, website_details_area, connection


"""CODE"""
def load_panel(devlobdd):
    search_result = None
    error = None
    ja_id = request.args.get("ja_id")
    is_connected = connection.connect()

    if is_connected:
        if ja_id:
            website_details_area.load_website_details()
        else:
            search_result, error = search_engine.search(devlobdd)

    return render_template("admin_space/panel.html", search_result=search_result, error=error,  zip=zip, url_for=url_for, len=len)


def load_website_validator():
    return get_submit_demand()