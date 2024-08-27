from flask import request, render_template, session, redirect, flash, url_for
from App.utils import bdd, utils
import re


def load_website_validator():
    param1 = request.args.get("ja_id")
    return render_template('admin_space/website_validator.html', ja_id=param1)