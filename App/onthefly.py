from flask import render_template, session, abort
import json



def gen_on_the_fly(domain_name, devlobdd):
    ja_site = devlobdd.get_ja_by_domain(domain_name)
    if not devlobdd.get_ja_by_domain(domain_name):
        return abort(404)
    json_site = json.loads(open(f"tmp/{ja_site[0]}/site.json").read())
    return render_template(f"sites/{ja_site[2]}.html", data=json_site)