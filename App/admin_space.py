from flask import request, render_template, session, redirect, flash, url_for
from App.utils import bdd, utils
import re

def panel(devlobdd):
    website_status = None
    ja_id = None
    error = None
    id = query_checker(devlobdd)

    if id is "Invalid query" or id is "No query" or id is "Ja does not exist nor have a website":
        error = id
    else:
        website_status = website_status_reader(devlobdd, id)
        print(website_status)

        if website_status is "Not available" or website_status is "Error":
            error = website_status

        ja_id = id


    return render_template("admin_space/panel.html", website_status=website_status, ja_id=ja_id, error=error)


def query_checker(devlobdd):
    search_query = request.form.get('query')
    all_ja_with_website = get_all_ja_with_website(devlobdd)

    if search_query is not None:
        try:
            if re.match("^ja-[0-9]{4}$", search_query):
                search_query = int(utils.ja_id_only(search_query))
                print("a")
            elif re.match("^[0-9]{4}$", search_query):
                search_query = int(search_query)
                print("b")
            else:
                return "Invalid query"

            if search_query not in all_ja_with_website:
                return "Ja does not exist nor have a website"

            return search_query


        except ValueError:
            return "Invalid query"
    else:
        return "No query"


def website_status_reader(devlobdd, ja_id):
    website_status = devlobdd.get_website_status_based_on_ja_id(ja_id)[0]

    if website_status == "Not available":
        return "Not available"
    elif website_status == 0:
        return ""
    elif website_status == 1:
        return "checked"
    else:
        return "Error"

def get_all_ja_with_website(devlobdd):
    all_ids = devlobdd.get_all_ja_with_website()
    all_ids = [int(t[0]) for t in all_ids]
    return all_ids