import re
from App.utils.utils import ja_id_only

def generate_no_query_infos_list(db):
    no_query_infos_list = db.fetch_all_ja_name_and_id()
    return no_query_infos_list


def retrieve_infos(db, query):
    search_result = {}

    # format -> '8166'
    if re.match("^\d{2,5}$" , query):
        ja_id = int(query)
        ja_infos = db.get_ja_byid(ja_id)
        if ja_infos:
            website_infos = db.view_data_website(ja_id)
            search_result = generate_info_dict(ja_infos, website_infos)
        else:
            ja_infos = [f"La JA {ja_id} n'existe pas", ja_id]
            website_infos = [f"La JA {ja_id} n'a pas de site web"]
            search_result = generate_info_dict(ja_infos, website_infos)


    # format -> 'ja-8166'
    elif re.match("^ja-\d{2,5}$", query):
        ja_id = int(ja_id_only(query))
        ja_infos = db.get_ja_byid(ja_id)
        if ja_infos:
            website_infos = db.view_data_website(ja_id)
            search_result = generate_info_dict(ja_infos, website_infos)
        else:
            ja_infos = [f"La JA {ja_id} n'existe pas", ja_id]
            website_infos = [f"La JA {ja_id} n'a pas de site web"]
            search_result = generate_info_dict(ja_infos, website_infos)


    # format -> 'devlowave'
    elif re.match("^(?!\s)[\w\s'À-ÖØ-öø-ÿ]+(?<!\s)$", query):
        ja_name = query
        ja_id = db.get_ja_id_by_name(ja_name)
        if ja_id:
            ja_infos = db.get_ja_byid(ja_id)
            website_infos = db.view_data_website(ja_id)
            if website_infos:
                search_result = generate_info_dict(ja_infos, website_infos)
            else:
                website_infos = [f"La JA {ja_name} n'a pas de site web"]
                search_result = generate_info_dict(ja_infos, website_infos)
        else:
            ja_infos = [f"La JA {ja_name} n'existe pas", ja_name]
            website_infos = [f"La JA {ja_name} n'a pas de site web"]
            search_result = generate_info_dict(ja_infos, website_infos)


    else:
        search_result = {"error" : "Merci de rechercher une JA avec un format correct. Exemples : ja-8166, 8166 ou devlowave"}



    return search_result

def generate_info_dict(ja_infos, website_infos):
    if ja_infos[0] == f"La JA {ja_infos[1]} n'existe pas":
        search_result = {
            "account": {
                "Erreur": ja_infos[0],
            },
            "website": {

            }
        }
    else:
        search_result = {
            "account": {
                "Nom": ja_infos[1],
                "Id": ja_infos[0],
                "Email": ja_infos[3],
                "Email verifié": "Oui" if ja_infos[4] == 1 else "Non",
                "Date de la vérification du mail": ja_infos[6] if ja_infos[4] == 1 else "Mail non verifié",
                "Compte crée": ja_infos[7],
                "Dernière connexion": ja_infos[8],
                "Compte activé": "Oui" if ja_infos[9] == 1 else "Non",
                "Permissions administrateur": "Oui" if ja_infos[10] == 1 else "Non",
            },
            "website": {

            }
        }


    if website_infos[0] == f"La JA {ja_infos[1]} n'a pas de site web":
        search_result["website"] = {
            "Erreur" : website_infos[0]
        }
    else :
          search_result["website"] = {
            "Sous domaine": f"{website_infos[1]}.devlowave.fr",
            "theme": website_infos[2],
            "status": "",
            "Hebergé depuis" : None, # Also needs the host demand date or host accept/reject date
            "Demande d'hébergement accepté par" : None,# Also needs the admin that accepted or rejected the host demand
            "Date de la demande d'hébergement" : None, # Also needs the date of the demand
            "Dernier changement de status fait par": None,
            "Date du dernier changement de status": None,
          }
          if website_infos[3] == 0:
              search_result["website"]["status"] = "Aucune demande d'hébergement n'a été effectué"
          elif website_infos[3] == 1:
              search_result["website"]["status"] = f"Site accessible à l'adresse {website_infos[1]}.devlowave.fr"
          elif website_infos[3] == 2:
              search_result["website"]["status"] = "Votre attention est requise, une demande d'hébergement est en cours !"
          elif website_infos[3] == 3:
              search_result["website"]["status"] = "Site inaccessible, la demande d'hébergement à eté refusée ou le site à été desactivé"

    return search_result