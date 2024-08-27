from flask import request, render_template, session, redirect, flash, url_for
from App.utils import bdd, utils
import re

def load_website_details():
    website_details = ["a", ["Standing for validation", "b", "c", "d", "e", "f", "g", "h", "i", "j"]]
    return website_details