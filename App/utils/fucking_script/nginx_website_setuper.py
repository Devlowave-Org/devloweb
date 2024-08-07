"""IMPORTS"""
import os
import RNJAPI_caller


"""GLOBAL VARS"""
ja_id = RNJAPI_caller.get_ja_id()
ja_name = RNJAPI_caller.get_ja_name()
ja_website_files_path = """/var/www/ja/""" + ja_id + "_website_files"


"""CODE"""
def create_website_folder():
    if not os.path.exists(ja_website_files_path):
        os.system(f"mkdir {ja_website_files_path}")
        return "Website folder created"
    else:
        return "JA website folder cannot be created, possibly already existing"

def create_config_file():
    with open("/var/www/devloweb/template/nginx_config.conf", "r") as conf_template:
        conf_template = conf_template.read()

    # modify necessitated lines
    conf_template_modified = conf_template[:67] + f"{ja_id}" + conf_template[67:]
    conf_template_modified = conf_template_modified[:122 + len(ja_id)] + f"{ja_name}" + conf_template_modified[123 + len(ja_id):]

    with open(f"/etc/nginx/sites-available/{ja_id}.conf", "w") as conf_file:
        conf_file.write(conf_template_modified)

    return "config file created"

def create_symbolic_link():
    os.system(f"ln -s /etc/nginx/sites-available/{ja_id}.conf /etc/nginx/sites-enabled/{ja_id}.conf")


"""CALL USED IN THE FUCKING SCRIPT TO RUN THE NGINX SETUPER"""
def setup_website():
    success = create_website_folder()
    print(success)

    success = create_config_file()
    print(success)

    create_symbolic_link()

def restart_nginx():
    os.system("sudo systemctl restart nginx") # Perms need to be given by the deployer for sudo this command with no password
