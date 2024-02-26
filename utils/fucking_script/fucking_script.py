"""IMPORTS"""
import os
import RNJAPI_caller
import nginx_website_setuper


"""FUCKING SCRIPT 🔥🔥"""
# Preparing the website environment
ja_name = RNJAPI_caller.get_ja_name()
nginx_website_setuper.setup_website()
