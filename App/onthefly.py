import os

from flask import render_template, send_file, abort
from werkzeug.utils import secure_filename
import json



def gen_on_the_fly(domain_name, devlobdd):
    ja_site = devlobdd.get_ja_by_domain(domain_name)
    if not ja_site:
        return abort(404)

    if ja_site[3] != 1:
        return abort(404)

    json_site = json.loads(open(f"tmp/{ja_site[0]}/site.json").read())
    return render_template(f"sites/{ja_site[2]}.html", data=json_site)

def send_image(ja_id, image_name):
    image_path = f"tmp/{ja_id}/{image_name}"
    if os.path.exists(image_path):
        return send_file(image_path, mimetype='image/gif')
    else: return abort(404)
