from App.utils.utils import ja_id_only
from flask import request, render_template, session, redirect, flash, url_for
from App.utils import bdd, utils


def panel(devlobdd):
    all_ids = devlobdd.get_all_ja_with_website()
    all_ids = [int(t[0]) for t in all_ids]

    search_query = request.form.get('query')
    search_query = int(ja_id_only(search_query))

    id = None
    for index in range(len(all_ids)):
        if search_query == all_ids[index]:
            id = all_ids[index]
            break
        if id is None:
            continue

    website_status = devlobdd.get_website_status_based_on_ja_id(id)

    return render_template("admin_space/panel.html", id=id, website_status=website_status)
