from flask import request, render_template, session, redirect, flash, url_for
from App.admin_space.admin_space_utils import website_status_reader
from App.utils import bdd, utils
import re

def load_website_details(devlobdd, ja_id):
    website_infos = []
    website_infos.append(get_website_status(devlobdd, ja_id))
    return website_infos

def get_website_status(devlobdd, ja_id):
    infos = []
    infos.append(website_status_reader(devlobdd, ja_id))
    return infos[0]