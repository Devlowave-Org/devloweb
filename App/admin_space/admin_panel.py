import re

from flask import render_template, Flask, request, session, redirect, url_for
from App.admin_space import search_engine, details_area
from App.admin_space.details_area import manage_hosting_demand


def load(db):
    search_results = load_search_area(db)

    # If there is a selected ja, show its details
    if search_results["results"]["result_1"]["error"] == None:
        for key, value in search_results["results"].items():
            if value["is_selected"] == True:
               website_details = load_website_details(db, value["id"])
               if website_details["status"] != search_results["results"]["result_1"]["status"]:
                   search_results["results"]["result_1"]["status"] = website_details["status"]
               break
            else:
                website_details = None
    else:
        website_details = None

    return render_template("admin_space/panel.html", search_results=search_results, website_details=website_details, type_result=type(search_results["results"]["result_1"]))


def load_search_area(db):
    # Define search_result["result"] field -> refer to search_engine to see what it becomes
    search_results = {
        "query" : None,
        "results" : {},
        "status" : None,
        "is_selected" : None,
        "error" : None
    }

    query_from_searchbar = request.args.get('searchbar')
    if query_from_searchbar:
        # If it is the ja name because it can contain whitespaces and all.
        if re.match("^(?!\s)[\w\s'À-ÖØ-öø-ÿ]+(?<!\s)$", query_from_searchbar):
            query_from_searchbar = query_from_searchbar
        else:
            query_from_searchbar = query_from_searchbar.replace(" ", "").lower()
    else:
        if request.args.get('ja_selector_id'):
            query_from_ja_selector = request.args.get('ja_selector_id')
        else:
            query_from_ja_selector = None

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

def load_website_details(db, ja_id):
    website_details = details_area.generate_details_area_dict(db, ja_id)
    return website_details