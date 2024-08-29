from flask import request, render_template, session, redirect, flash, url_for
from App.admin_space.admin_space_utils import website_status_reader
from App.utils import bdd, utils
import re

def load_website_details(devlobdd, ja_id):
    website_infos = []
    website_infos.append(get_website_status(devlobdd, ja_id))
    website_infos.append(make_link_to_ja_validation_page(ja_id))
    return website_infos

def get_website_status(devlobdd, ja_id):
    website_status = (website_status_reader(devlobdd, ja_id))
    return website_status

def make_link_to_ja_validation_page(ja_id):
    if ja_id :
        return f"admin_space/website_validator?ja_id={ja_id}"
    else:
        return None