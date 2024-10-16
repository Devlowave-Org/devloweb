import re
from pprint import pprint

from flask import request
from App.utils import utils


"""CODE"""
def search_perfect_matching(db, search_results):
    query = search_results["query"]

    # format -> '8166'
    if re.match("^\d{2,5}$" , query):
        ja_id = int(query)
        ja_name = db.get_ja_name_by_id(ja_id)
        if ja_name:
            ja_name = ja_name[0]
            ja_domain = db.get_ja_domain_by_id(ja_id)
            if ja_domain:
                search_results['results']["result_1"] = generate_ja_info_dict(db, search_results,  ja_id)
            else:
                search_results['results']["result_1"] = f"La JA '{ja_name}', ja-{ja_id} à un compte devloweb mais pas de site."
        else:
            search_results['results']["result_1"] = "Merci d'entrer un identifiant de JA existante."

    # format -> 'ja-8166'
    elif re.match("^ja-\d{2,5}$", query):
        ja_id = int(utils.ja_id_only(query))
        ja_name = db.get_ja_name_by_id(ja_id)
        if ja_name:
            ja_name = ja_name[0]
            ja_domain = db.get_ja_domain_by_id(ja_id)
            if ja_domain:
                search_results['results']["result_1"] = generate_ja_info_dict(db, search_results, ja_id)
            else:
                search_results['results']["result_1"] = f"La JA '{ja_name[0]}', id : '{ja_id}' à un compte devloweb mais pas de site."
        else:
            search_results['results']["result_1"] = "Merci d'entrer un identifiant de JA existante."

    # format -> 'devlowave'
    elif re.match("^(?!\s)[\w\s'À-ÖØ-öø-ÿ]+(?<!\s)$", query):
        ja_name = query
        print(db.get_ja_id_by_name(ja_name))
        ja_id = db.get_ja_id_by_name(ja_name)
        if ja_id:
            ja_id=ja_id[0]
            ja_domain = db.get_ja_domain_by_id(ja_id)
            if ja_domain:
                search_results['results']["result_1"] = generate_ja_info_dict(db, search_results, ja_id)
            else:
                search_results['results'][
                    "result_1"] = f"La JA '{ja_name}', id : '{ja_id}' à un compte devloweb mais pas de site."
        else:
            search_results['results']["result_1"] = "Merci d'entrer un nom de JA existante ou de revérifier votre entrée."

    elif re.match("^[A-Za-z]+\.devlowave\.fr$", query) or re.match("^[A-Za-z]+\.fr$", query): # -> devlowave.devlowave.fr or devlowave.fr
        ja_domain = query
        ja_id = db.get_ja_id_by_domain(ja_domain)
        if ja_id:
            ja_name = db.get_ja_name_by_id(ja_id)
            if ja_name:
                search_results['results']["result_1"] = generate_ja_info_dict(db, search_results, ja_id)
        else:
             search_results['results']["result_1"] = "Merci d'entrer un sous-domaine existant ou de revérifier votre entrée."

    else:
        search_results["results"][f"result_1"] = f"Votre entrée ne correspond à aucun format attendu, veuillez vérifier que votre requête est valide."


    # If no results were added, add a default "no results" message
    if type(search_results["results"]["result_1"]) is str:
        search_results["results"][f"result_1"] = {"error" : "error", "content" : f"{search_results['results']['result_1']}"}


    if search_results["results"]["result_1"]["error"] == None:
        for key, value in search_results.items():
            if key == "results":
                value["result_1"]["is_selected"] = True


    return search_results


def no_query(db, search_results):
    all_ja_ids_with_website = db.fetch_all_ja_ids_with_website()
    for index, ja_id in enumerate(all_ja_ids_with_website):
        # Create a new dictionary for each result
        ja_info = {
            "id": ja_id[0],
            "name": db.get_ja_name_by_id(ja_id[0])[0],
            "subdomain": db.get_ja_domain_by_id(ja_id[0])[0],
            "status": str(db.get_website_status_by_id(ja_id[0])[0]),
            "is_selected": search_results["is_selected"],
            "error": None
        }
        search_results["results"][f"result_{index + 1}"] = ja_info
    return search_results


def generate_ja_info_dict(db, search_results, ja_id):
    # Create a new dictionary for the result
    ja_info = {
        "id": ja_id,
        "name": db.get_ja_name_by_id(ja_id)[0],
        "subdomain": db.get_ja_domain_by_id(ja_id)[0],
        "status": str(db.get_website_status_by_id(ja_id)[0]),
        "is_selected": search_results["is_selected"],
        "error": None
    }
    return ja_info
