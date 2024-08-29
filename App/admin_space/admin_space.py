"""IMPORTS"""
from flask import request, render_template, session, redirect, flash, url_for
from App.admin_space.search_engine import search
from App.admin_space.website_details_area import load_website_details
from App.admin_space.website_validator import process_submit_demand
from App.admin_space.admin_space_utils import query_parameter_getter, query_getter_and_checker, website_status_reader
from App.utils import bdd, utils
from App.admin_space import search_engine, website_details_area, connection


"""CODE"""
def load_panel(devlobdd):
    website_details = None
    search_result = None
    error = None
    ja_id = query_getter_and_checker(devlobdd)
    is_connected = connection.connect()

    if is_connected:
        if ja_id == "Invalid query" or ja_id == "Ja does not exist nor have a website":
            error = ja_id
        elif ja_id == "No query":
            search_result, error = search_engine.search(devlobdd)
        else:
            website_details = load_website_details(devlobdd, ja_id)
            search_result, error = search_engine.search(devlobdd)
    else:
        error = "You are not authorized to access this page"

    return render_template("admin_space/panel.html", search_result=search_result, error=error, website_details=website_details, zip=zip, url_for=url_for, len=len)


def load_website_validator(devlobdd):
    is_connected = connection.connect()
    if is_connected:
        return process_submit_demand(devlobdd)
    else:
        return render_template("admin_space/website_validator.html", error="You are not authorized to access this page")