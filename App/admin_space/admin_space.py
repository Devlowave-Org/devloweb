from flask import request, render_template, session, redirect, flash, url_for
from App.utils import bdd, utils
from App.admin_space import search_bar

def load_panel(devlobdd):
    search_result, website_details, error = search_bar.search(devlobdd)

    return render_template("admin_space/panel.html", search_result=search_result, website_details=website_details, error=error, zip=zip)

