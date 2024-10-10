from flask import render_template, Flask, request, session, redirect, url_for
from App.admin_space import search_engine

def load(db):
    search_results = load_search_area(db)
    website_details = load_website_details(db)

    return render_template("admin_space/panel.html", search_results=search_results, website_details=website_details)


def load_search_area(db):
    query_from_searchbar = request.args.get('searchbar')
    if query_from_searchbar:
        query_from_searchbar = query_from_searchbar.replace(" ", "").lower()
    else:
        if request.form.get('ja_selector_id'):
            query_from_ja_selector = request.form.get('ja_selector_id')
        else:
            query_from_ja_selector = None

    # Define search_result["result"] field -> refer to search_engine to see what it becomes
    search_results = {
        "query" : None,
        "results" : {},
        "status" : None,
        "is_selected" : None
    }

    # Set the query
    if query_from_searchbar is not None:
        search_results['query'] = query_from_searchbar
    elif query_from_ja_selector is not None:
        search_results['query'] = query_from_ja_selector
    else:
        search_results['query'] = None

    # Search
    if search_results["query"]:
        search_results = search_engine.search_perfect_matching(db, search_results)
    else:
        search_results = search_engine.no_query(db, search_results)

    return search_results

def load_website_details(db):
    return "a"