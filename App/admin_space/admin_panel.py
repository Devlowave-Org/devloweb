from flask import render_template, Flask, request, session, redirect, url_for
import re

def load(db):
    query = request.args.get('searchbar')
    if query:
        query = query.replace(" ", "").lower()

    search_results = {
        "query" : query,
        "results" : {}
    }

    search_results = search_engine(db, search_results)

    return render_template("admin_space/panel.html", search_results=search_results, enumerate=enumerate)

def search_engine(db, search_results):
    if search_results['query']:
        results_count = 0

        query = search_results["query"]
        if re.match("^\d{2,5}$" , query):# -> 8166
            ja_id = int(query)
            ja_name = db.get_ja_name_by_id(ja_id)[0]
            ja_domain = db.get_ja_domain_by_id(ja_id)[0]
            results_count += 1
            search_results["results"][f"result_{results_count}"] = f"format 1 - {query}, ja name : {ja_name}, subdomain : {ja_domain}"

        elif re.match("^ja-\d{2,5}$", query): # -> ja-8166
            results_count += 1
            search_results["results"][f"result_{results_count}"] = f"format 2 - {query}"

        elif re.match("^[A-Za-z]+$", query): # -> devlowave
            results_count += 1
            search_results["results"][f"result_{results_count}"] = f"format 3 - {query}"

        elif re.match("^[A-Za-z]+\.devlowave\.fr$", query): # -> devlowave.devlowave.fr
            search_results["results"][f"result_{results_count}"] = f"format 4 - {query}"

        # If no results were added, add a default "no results" message
        if not search_results["results"]:
            results_count += 1
            search_results["results"][f"result_{results_count}"] = "Please enter a valid query."
    else:
        all_ja_ids_with_website = db.fetch_all_ja_ids_with_website()
        for index, ja_id in enumerate(all_ja_ids_with_website):
            # Create a new dictionary for each result
            ja_info = {
                "id" : ja_id[0],
                "name": db.get_ja_name_by_id(ja_id[0])[0],
                "subdomain": db.get_ja_domain_by_id(ja_id[0])[0]
            }
            search_results["results"][f"result_{index + 1}"] = ja_info

        print(search_results)


        for key, value in search_results["results"].items():
            print(value)

    return search_results
