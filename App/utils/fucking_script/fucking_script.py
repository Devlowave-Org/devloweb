"""IMPORTS"""
import RNJAPI_caller
import nginx_website_setuper
import cloudflare

"""FUCKING SCRIPT 🔥🔥"""
# Getting ja's name and id
ja_id = RNJAPI_caller.get_ja_id()
ja_name = RNJAPI_caller.get_ja_name()

# Preparing the website environment of the new website
nginx_website_setuper.setup_website()
nginx_website_setuper.restart_nginx()

# Calling cloudflare API to create a new subdomain
cloudflare.create_subdomain(ja_name, "82.64.89.33")
