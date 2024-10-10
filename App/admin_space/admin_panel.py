from flask import render_template, Flask, request, session, redirect, url_for
import App.admin_space.search_engine
import re

from App.admin_space import search_engine


def load(db):
    query = request.args.get('searchbar')
    if query:
        query = query.replace(" ", "").lower()
    else:
        query = request.form.get('ja_selector_id')

    search_results = {
        "query" : query,
        "query_type" : None, # Can be ja_selector or searchbar
        "results" : {}
    }

    if query:
        search_results = search_engine.search_perfect_matching(db, search_results)
    else:
        search_results = search_engine.no_query(db, search_results)

    ja_selector_id = request.form.get('ja_selector_id')
    if ja_selector_id:
        print(ja_selector_id)

    return render_template("admin_space/panel.html", search_results=search_results, enumerate=enumerate)


