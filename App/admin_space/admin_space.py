from select import error

from flask import request, render_template, session, redirect, flash, url_for
from App.utils import bdd, utils
from App.admin_space import search_bar, website_details_area

def load_panel(devlobdd):
    selected_id = request.args.get("ja_id")

    # TODO : Connection thing
    if selected_id:
        search_result = None
        error = None
        website_details = website_details_area.load_website_details()
    else:
        search_result, website_details, error = search_bar.search(devlobdd)

    try:
        if len(search_result[2]) == 1 or request.form.get("ja_selector") == "1":
            website_details = website_details_area.load_website_details()
    except TypeError:
        pass

    return render_template("admin_space/panel.html", search_result=search_result, website_details=website_details, error=error, selected_id=selected_id,  zip=zip, url_for=url_for)

def load_website_validator():
    param1 = request.args.get('param1')
    return render_template("admin_space/website_validator.html", ja_id=param1)
