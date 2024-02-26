"""IMPORTS"""
import os
import RNJAPI_caller
import nginx_website_setuper


"""FUCKING SCRIPT 🔥🔥"""
# Preparing the website environment
ja_id = RNJAPI_caller.get_ja_id()
nginx_website_setuper.setup_website()
