import os


ja_name = "azerty" #input("Please enter the name of the JA > ")
ja_website_files_path = """/var/www/""" "./" + ja_name + "_website_files"

# create the folder that will contain website files

print(f"Creating folder: '{ja_website_files_path}'")
os.system(f"sudo mkdir {ja_website_files_path}")

print(f"Folder created\nGiving permissions to 'www-data:www-data'")
os.system(f"sudo chown -R www-data:www-data {ja_website_files_path}")

print("Permission given, adjusting them")
os.system(f"sudo chmod 755 {ja_website_files_path}")

print("Creating index.html")

with open(f"{ja_website_files_path}/index.html", "w") as html_index:
    html_index.write("Hello World !")

# create the conf file
print("Index created, creating conf file")

with open(f"/etc/nginx/sites-available/{ja_name}_website.conf", "w") as website_conf:
    website_conf.write(f"server {{\n\n    listen 80;\n\n    listen [::]:80;\n\n    root /var/www/{ja_website_files_path};\n\n    index index.html;\n    server_name {ja_name}.devlowave.fr;\n\n    location / {{\n        try_files $uri $uri/ =404;\n    }}\n}}")

print("Config file created, checking syntax")
os.system(f"sudo ln -s /etc/nginx/sites-available/{ja_name}_website.conf /etc/nginx/sites-enabled/")



