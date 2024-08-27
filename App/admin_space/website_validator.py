from flask import request, render_template, session, redirect, flash, url_for
from App.utils import bdd, utils
import re


def get_submit_demand():
    ja_id = request.args.get('ja_id')
    print(ja_id)
    return render_template('admin_space/website_validator.html', ja_id=ja_id)