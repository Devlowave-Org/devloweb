"""IMPORTS"""
import os
import RNJAPI_caller


"""GLOBAL VARS"""
ja_name = RNJAPI_caller.get_ja_name()
ja_website_files_path = """/var/www/ja/""" + ja_name + "_website_files"


"""CODE"""
def create_website_folder():
    if not os.path.exists(ja_website_files_path):
        os.system(f"mkdir {ja_website_files_path}")
        print("Website folder created")
    else:
        print("JA website folder cannot be created, possibly already existing")

def create_config_file():
    # Copy/Paste /var/www/devloweb/template/nginx_config.conf
    # Modify expected lines


"""CALL USED IN THE FUCKING SCRIPT TO RUN THE NGINX SETUPER"""
def setup_website():
    create_website_folder()

