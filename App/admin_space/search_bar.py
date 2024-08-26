"""IMPORTS"""
from array import array

from flask import request, render_template, session, redirect, flash, url_for
from App.utils import bdd, utils
import re

"""MAIN FUNCTION"""
def search(devlobdd):
    error = None
    search_result = None
    all_ids = get_all_ja_with_website(devlobdd)
    id = query_checker(devlobdd)
    print(id)

    if id is "Invalid query" or id is "Ja does not exist xor have a website":
        error = id
    elif id is "No query":
        list_template = ["List of ja who created a website :", [], []]
        search_result = list_generator(list_template, devlobdd, all_ids)
    else:
        website_status = website_status_reader(devlobdd, id)
        if website_status is "Not available" or website_status is "Error":
            error = website_status
        else:
            list_template = ["Results :", [], []]
            search_result = list_generator(list_template, devlobdd, id)


    return search_result, error

"""UTILS FUNCTIONS"""
def list_generator(received_list, devlobdd, all_ids):
    list_to_return = received_list

    if type(all_ids) is list:
        for index in range(len(all_ids)):
            website_status = website_status_reader(devlobdd, all_ids[index])
            checkbox_parameters = checkbox_parameter_manager(website_status)
            list_to_return[1] = list_to_return[1] + [f"{all_ids[index]}"]
            list_to_return[2] = list_to_return[2] + [f"{checkbox_parameters}"]

    elif type(all_ids) is int:
            print(f"1{all_ids}")
            website_status = website_status_reader(devlobdd, all_ids)
            print(f"2{all_ids}")
            checkbox_parameters = checkbox_parameter_manager(website_status)
            list_to_return[1] = list_to_return[1] + [f"{all_ids}"]
            list_to_return[2] = list_to_return[2] + [f"{checkbox_parameters}"]
    return list_to_return


def checkbox_parameter_manager(website_status):
    if website_status is "Website disapproved" or website_status is "Website submitted but not approved yet":
        checkbox_parameters = "disabled"
    else:
        checkbox_parameters = website_status

    return checkbox_parameters


def query_checker(devlobdd):
    search_query = request.form.get('query')
    all_ja_with_website = get_all_ja_with_website(devlobdd)

    if search_query is not None:
        try:
            if re.match("^ja-[0-9]{4}$", search_query):
                search_query = int(utils.ja_id_only(search_query))
            elif re.match("^[0-9]{4}$", search_query):
                search_query = int(search_query)
            else:
                if search_query is "":
                    return "No query"
                return "Invalid query"
            if search_query not in all_ja_with_website:
                return "Ja does not exist xor have a website"
            else:
                return search_query

        except ValueError:
            return "Invalid query"
    else:
        return "No query"


def website_status_reader(devlobdd, ja_id):
    website_status = devlobdd.get_website_status_based_on_ja_id(ja_id)[0]

    if website_status is None:
        return "Not available"
    elif website_status == 0:
        return ""
    elif website_status == 1:
        return "checked"
    elif website_status == 2:
        return "Website submitted but not approved yet"
    elif website_status == 3:
        return "Website disapproved"
    else:
        return "Error"


def get_all_ja_with_website(devlobdd):
    all_ids = devlobdd.get_all_ja_with_website()
    all_ids = [int(t[0]) for t in all_ids]
    return all_ids