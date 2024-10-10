"""IMPORTS"""
from flask import request, render_template, session, redirect, flash, url_for
from App.utils import bdd, utils
from App.admin_space.admin_space_utils import *
import re



"""MAIN FUNCTION"""
def search(devlobdd):
    ja_id = query_getter_and_checker(devlobdd)
    search_result, error = search_result_list_generator_and_checker(devlobdd, ja_id)
    return search_result, error



"""UTILS FUNCTIONS (specific to the search_engine"""




def search_result_list_generator_and_checker(devlobdd, ja_id):
    search_result = None
    error = None
    all_ja_ids = all_ja_with_website_getter(devlobdd)

    if ja_id == "Invalid query" or ja_id == "Ja does not exist nor have a website":
        error = ja_id
    elif ja_id == "No query":
        list_template = ["List of ja who created a website :", [], []]
        search_result = search_result_list_maker(list_template, devlobdd, all_ja_ids)
    else:
        website_status = website_status_reader(devlobdd, ja_id)
        if website_status is "Not available" or website_status is "Error":
            error = website_status
        else:
            list_template = ["Results :", [], []]
            search_result = search_result_list_maker(list_template, devlobdd, ja_id)

    return search_result, error


def search_result_list_maker(received_list, devlobdd, all_ja_ids):
    website_status = None
    list_to_return = received_list

    if type(all_ja_ids) is list:
        for index in range(len(all_ja_ids)):
            website_status = website_status_reader(devlobdd, all_ja_ids[index])
            checkbox_parameters = checkbox_parameter_setter_based_on_website_status(website_status)
            list_to_return[1] = list_to_return[1] + [f"{all_ja_ids[index]}"]
            list_to_return[2] = list_to_return[2] + [f"{checkbox_parameters}"]

    elif type(all_ja_ids) is int:
            website_status = website_status_reader(devlobdd, all_ja_ids)
            checkbox_parameters = checkbox_parameter_setter_based_on_website_status(website_status)
            list_to_return[1] = list_to_return[1] + [f"{all_ja_ids}"]
            list_to_return[2] = list_to_return[2] + [f"{checkbox_parameters}"]

    return list_to_return

