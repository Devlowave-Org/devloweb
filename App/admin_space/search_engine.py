import re
import shutil

import App.utils.utils as utils
from flask import request, redirect, session
from datetime import datetime
from App.utils.utils import ja_id_only
import App.utils.email_api as email_api
from threading import Thread


"""INFOS"""
def generate_no_query_infos_list(db):
    no_query_infos_list = db.fetch_all_ja_name_and_id()
    return no_query_infos_list


def retrieve_infos(db, query):
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
            if website_infos[3] != 0:
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
        }


    if website_infos[0] == f"La JA {ja_infos[1]} n'a pas de site web":
        search_result["website"] = {
            "Erreur" : website_infos[0]
        }
    else :
          search_result["website"] = {
            "Sous domaine": f"{website_infos[1]}.devlowave.fr",
            "theme": website_infos[2],
            "status": "", # Will be set later on
            "Date de la demande d'hébergement" : website_infos[4] if website_infos[4] != None else "Cette JA n'a jamais demandé à avoir un site",
            "Demande validée le": website_infos[5] if website_infos[5] != None else "Pas encore validée" ,
            "Demande d'hébergement accepté par": website_infos[6] if website_infos[6] != None else "Pas encore validée",  # Also needs the admin that accepted or rejected the host demand
            "Dernier changement de status fait par": website_infos[7] if website_infos[7] != None else "Status jamais changé",
            "Date du dernier changement de status": website_infos[8] if website_infos[8] != None else "Status jamais changé",
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



"""HOST MANAGEMENT"""
def generate_no_query_host_demands_list(db):
    no_query_host_demands_list = {}

    for index, host in enumerate(db.fetch_all_host_demands()):
        no_query_host_demands_list[str(index)] = {
            "name": db.get_name_by_id(host[1])[0],
            'id': host[1],
            "subdomain": host[2],
            'demand_date': host[5]
        }

    # Sort the list by parsing the demand_date into datetime objects
    sorted_list = dict(
        sorted(
            no_query_host_demands_list.items(),
            key=lambda item: datetime.strptime(item[1]['demand_date'], '%Y-%m-%d %H:%M:%S.%f')
        )
    )

    return sorted_list



def retrieve_host_demand(db, query):
    # format -> '8166'
    if re.match("^\d{2,5}$", query):
        ja_id = int(query)
        search_result = generate_host_demand_dict(db, ja_id)


    # format -> 'ja-8166'
    elif re.match("^ja-\d{2,5}$", query):
        ja_id = int(ja_id_only(query))
        search_result = generate_host_demand_dict(db, ja_id)


    # format -> 'devlowave'
    elif re.match("^(?!\s)[\w\s'À-ÖØ-öø-ÿ]+(?<!\s)$", query):
        ja_name = query
        ja_id = db.get_ja_id_by_name(ja_name)
        search_result = generate_host_demand_dict(db, ja_id)

    else:
        search_result = {
            "error": "Merci de rechercher une JA avec un format correct. Exemples : ja-8166, 8166 ou devlowave"}

    return search_result



def host_demand_dict_maker(db, website_infos, ja_id):
    if website_infos[0] == f"La JA {ja_id} n'a pas de site web":
        search_result = {
            "Erreur" : website_infos[0]
        }
    elif website_infos[0] == f"La JA {ja_id} n'a pas de demandes en cours":
        search_result = {
            "Erreur" : website_infos[0]
        }
    elif website_infos[0] == "Cette JA n'existe pas et/ou n'a pas de site web":
        search_result = {
            "Erreur" : website_infos[0]
        }
    else :
          search_result = {
            "JA": f"{db.get_name_by_id(ja_id)[0]} - {ja_id}",
            "Sous domaine": f"{website_infos[1]}.devlowave.fr",
            "theme": website_infos[2],
            "Date de la demande d'hébergement" : website_infos[4],
            "Lien de la preview": f"preview/{ja_id}",
            "status_modification": "",
            "JA_name": db.get_name_by_id(ja_id)[0],
          }

    if search_result.get("status_modification"):
        search_result["status_modification"] = manage_website_status_modification(db, ja_id)


    return search_result


def generate_host_demand_dict(db, ja_id):
    if ja_id:
        ja_id = ja_id[0]
        website_infos = db.view_data_website(ja_id)
        if website_infos:
            if website_infos[3] == 2:
                search_result = host_demand_dict_maker(db, website_infos, ja_id)
                # Only call manage_website_status_modification here if needed
                search_result["status_modification"] = manage_website_status_modification(db, ja_id)
            else:
                website_infos = [f"La JA {ja_id} n'a pas de demandes en cours"]
                search_result = host_demand_dict_maker(db, website_infos, ja_id)
        else:
            website_infos = [f"La JA {ja_id} n'a pas de site web"]
            search_result = host_demand_dict_maker(db, website_infos, ja_id)
    else:
        website_infos = ["Cette JA n'existe pas et/ou n'a pas de site web"]
        search_result = host_demand_dict_maker(db, website_infos, ja_id)

    return search_result

"""WEBSITE SECTION"""
def generate_no_query_websites_list(db):
    no_query_websites_list = {}

    print(db.fetch_all_websites())

    for index, host in enumerate(db.fetch_all_websites()):
        no_query_websites_list[str(index)] = {
            "name": db.get_name_by_id(host[1])[0],
            'id': host[1],
            "subdomain": host[2],
            'demand_date': host[5]
        }

    # Sort the list by parsing the demand_date into datetime objects
    sorted_list = dict(
        sorted(
            no_query_host_demands_list.items(),
            key=lambda item: datetime.strptime(item[1]['demand_date'], '%Y-%m-%d %H:%M:%S.%f')
        )
    )

    return sorted_list



def retrieve_host_demand(db, query):
    # format -> '8166'
    if re.match("^\d{2,5}$", query):
        ja_id = int(query)
        search_result = generate_host_demand_dict(db, ja_id)


    # format -> 'ja-8166'
    elif re.match("^ja-\d{2,5}$", query):
        ja_id = int(ja_id_only(query))
        search_result = generate_host_demand_dict(db, ja_id)


    # format -> 'devlowave'
    elif re.match("^(?!\s)[\w\s'À-ÖØ-öø-ÿ]+(?<!\s)$", query):
        ja_name = query
        ja_id = db.get_ja_id_by_name(ja_name)
        search_result = generate_host_demand_dict(db, ja_id)

    else:
        search_result = {
            "error": "Merci de rechercher une JA avec un format correct. Exemples : ja-8166, 8166 ou devlowave"}

    return search_result



def host_demand_dict_maker(db, website_infos, ja_id):
    if website_infos[0] == f"La JA {ja_id} n'a pas de site web":
        search_result = {
            "Erreur" : website_infos[0]
        }
    elif website_infos[0] == f"La JA {ja_id} n'a pas de demandes en cours":
        search_result = {
            "Erreur" : website_infos[0]
        }
    elif website_infos[0] == "Cette JA n'existe pas et/ou n'a pas de site web":
        search_result = {
            "Erreur" : website_infos[0]
        }
    else :
          search_result = {
            "JA": f"{db.get_name_by_id(ja_id)[0]} - {ja_id}",
            "Sous domaine": f"{website_infos[1]}.devlowave.fr",
            "theme": website_infos[2],
            "Date de la demande d'hébergement" : website_infos[4],
            "Lien de la preview": f"preview/{ja_id}",
            "status_modification": "",
            "JA_name": db.get_name_by_id(ja_id)[0],
          }

    if search_result.get("status_modification"):
        search_result["status_modification"] = manage_website_status_modification(db, ja_id)


    return search_result


def generate_host_demand_dict(db, ja_id):
    if ja_id:
        ja_id = ja_id[0]
        website_infos = db.view_data_website(ja_id)
        if website_infos:
            if website_infos[3] == 2:
                search_result = host_demand_dict_maker(db, website_infos, ja_id)
                # Only call manage_website_status_modification here if needed
                search_result["status_modification"] = manage_website_status_modification(db, ja_id)
            else:
                website_infos = [f"La JA {ja_id} n'a pas de demandes en cours"]
                search_result = host_demand_dict_maker(db, website_infos, ja_id)
        else:
            website_infos = [f"La JA {ja_id} n'a pas de site web"]
            search_result = host_demand_dict_maker(db, website_infos, ja_id)
    else:
        website_infos = ["Cette JA n'existe pas et/ou n'a pas de site web"]
        search_result = host_demand_dict_maker(db, website_infos, ja_id)

    return search_result


"""For all"""
def manage_website_status_modification(db, ja_id):
    mail_sender = email_api.DevloMail()
    if request.form.get("accept_button") or request.form.get("activate_button"):
        if request.form.get("accept_confirmation") == "oui" or request.form.get("activate_confirmation") == "oui":
            db.activate_website(ja_id, session.get("name"))
            mail_thread = Thread(target=mail_sender.send_host_demand_accept_mail, args=(db.get_email_by_id(ja_id)[0], f"{db.get_subdomain_by_id(ja_id)[0]}.devlowave.fr"))
            mail_thread.start()
            return 9
        elif request.form.get("activate_confirmation") == "non" or request.form.get("accept_confirmation") == "non":
            return request.form.get("activate_button")
        return 1

    elif request.form.get("reject_button") or request.form.get("deactivate_button"):
        if request.form.get("reject_message"):
            db.disable_website(ja_id, session.get("name"))
            mail_thread = Thread(target=mail_sender.send_host_demand_reject_mail, args=(db.get_email_by_id(ja_id)[0], f"{db.get_subdomain_by_id(ja_id)[0]}.devlowave.fr"))
            mail_thread.start()
            return 9
        else:
            return False

    elif request.form.get("reset_button"):
        if request.form.get("reset_message"):
            db.reset_website(ja_id)
            # Also delete the website and all -> supprimer le tmp et réinvoquer init website
            shutil.rmtree(f"tmp/{ja_id}")
            utils.create_ja_folder(ja_id)
            utils.set_default_value_to_json_site(ja_id)
            db.init_website(ja_id, "", "beta")
            # Also need to send the mail here
            return request.form.get("reset_message")
        return 0

    # Otherwise (it is not supposed to happen)
    else:
        return None
