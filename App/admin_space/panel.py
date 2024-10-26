from flask import render_template, request, redirect, render_template_string, session
import App.admin_space.search_engine as search_engine
import re

def load(db):
    print(request.form)
    search_result = None
    page_has_changed = None

    if request.form.get('sidebar_selector'):
        if request.form.get('sidebar_selector') != session.get('sidebar_selector'):
            page_has_changed = True
        else:
            page_has_changed = False

        session['sidebar_selector'] = request.form.get('sidebar_selector')



    # Check and format input
    query_from_searchbar = request.form.get('searchbar')
    query_from_ja_selector = request.form.get('ja_selector')
    if query_from_searchbar:
        # If it is the ja name because it can contain whitespaces and all.
        if re.match("^(?!\s)[\w\s'À-ÖØ-öø-ÿ]+(?<!\s)$", query_from_searchbar):
            query = query_from_searchbar
        else:
            query = query_from_searchbar.replace(" ", "").lower()
    elif query_from_ja_selector:
            query = query_from_ja_selector.split(" - ")[0]
    else:
        query = None

    # Set the query cookie correctly
    if query is not None:
        session['searchbar_query'] = query
    elif query_from_ja_selector is not None:
        session['searchbar_query'] = query_from_ja_selector
    else:
        # So the user can type his query once and then he can change page
        if page_has_changed is False or page_has_changed is None:
            session['searchbar_query'] = None
        else:
            pass

    if session.get('sidebar_selector') == "Infos" or None:
        search_result = load_infos(db)
    elif session.get('sidebar_selector') == "Demandes d\'hébergement":
        search_result = load_hosting(db)
    else:
        search_result = load_infos(db)

    return render_template("admin_space/panel.html", search_result=search_result)


def load_infos(db):
    if session.get('searchbar_query') is None:
        search_result = search_engine.generate_no_query_infos_list(db)
    else:
        search_result = search_engine.retrieve_infos(db, session['searchbar_query'])

    return search_result


def load_hosting(db):
    if session.get('searchbar_query') is None:
        search_result = search_engine.generate_no_query_host_demands_list(db)
    else:
        search_result = search_engine.retrieve_host_demand(db, session['searchbar_query'])

    return search_result
