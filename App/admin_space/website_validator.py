from flask import request, render_template, session, redirect, flash, url_for
from App.admin_space.admin_space_utils import website_status_reader
from App.utils import bdd, utils
import re


def process_submit_demand(devlobdd):
    error = None
    ja_id = request.args.get('ja_id')
    if website_status_reader(devlobdd, ja_id) == "Website submitted but not approved yet":
        action = request.form.get('action')
        if action == "Accept":
            devlobdd.update_website_status_based_on_ja_id(ja_id, 1)
            error= "Your acceptation has been applied, website's now available"
        if action == "Reject":
            devlobdd.update_website_status_based_on_ja_id(ja_id, 3)
            error = "Your reject has been applied"
    else:
        error = "No demand for this JA"

    return render_template('admin_space/website_validator.html', ja_id=ja_id, error=error)