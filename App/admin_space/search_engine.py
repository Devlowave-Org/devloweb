import re
from App.utils import utils

"""CODE"""
def search_perfect_matching(db, search_results):
    query = search_results["query"]

    if re.match("^\d{2,5}$" , query):# -> 8166
        ja_id = int(query)
        ja_name = db.get_ja_name_by_id(ja_id)
        if ja_name:
            ja_domain = db.get_ja_domain_by_id(ja_id)
            if ja_domain:
                search_results['results']["result_1"] = generate_ja_info_dict(db, ja_id)
            else:
                search_results['results']["result_1"] = f"La JA '{ja_name[0]}', id : '{ja_id}' à un compte devloweb mais pas de site."
        else:
            search_results['results']["result_1"] = "Merci d'entrer un identifiant de JA existante."

    elif re.match("^ja-\d{2,5}$", query): # -> ja-8166
        ja_id = int(utils.ja_id_only(query))
        ja_name = db.get_ja_name_by_id(ja_id)[0]
        ja_domain = db.get_ja_domain_by_id(ja_id)[0]
        search_results['results']["result_1"] = generate_ja_info_dict(db, ja_id)

    elif re.match("^[A-Za-z]+$", query): # -> devlowave
        search_results["results"][f"result_1"] = f"format 3 - {query}"

    elif re.match("^[A-Za-z]+\.devlowave\.fr$", query): # -> devlowave.devlowave.fr
        search_results["results"][f"result_1"] = f"format 4 - {query}"

    # If no results were added, add a default "no results" message
    if not search_results["results"]:
        search_results["results"][f"result_1"] = "Please enter a valid query."

    return search_results


def no_query(db, search_results):
    all_ja_ids_with_website = db.fetch_all_ja_ids_with_website()
    for index, ja_id in enumerate(all_ja_ids_with_website):
        # Create a new dictionary for each result
        ja_info = {
            "id": ja_id[0],
            "name": db.get_ja_name_by_id(ja_id[0])[0],
            "subdomain": db.get_ja_domain_by_id(ja_id[0])[0]
        }
        search_results["results"][f"result_{index + 1}"] = ja_info

    return search_results


def generate_ja_info_dict(db, ja_id):
    # Create a new dictionary for the result
    ja_info = {
        "id": ja_id,
        "name": db.get_ja_name_by_id(ja_id)[0],
        "subdomain": db.get_ja_domain_by_id(ja_id)[0]
    }
    return ja_info
