"""IMPORTS"""
import os


"""CODE"""

# These lines are here to make the ja folder existing and give perms to it

# Create folder ja in www if it doesn't exist
ja_websites_folder_path = "/var/www/ja"
if not os.path.exists(ja_websites_folder_path):
    os.system(f"sudo mkdir {ja_websites_folder_path}")
    #Give permissions to this folder
    os.system(f"sudo chown $USER:www-data /var/www/ja")
    os.system("sudo chmod g+s /var/www/ja")
    os.system("sudo chmod o-rwx /var/www/ja")


# Theses lines are here to make the setuper able to create symbolic links without sudo 

#give perms to sites-available
os.system(f"sudo chown $USER:www-data /etc/nginx/sites-available")
os.system("sudo chmod g+s /etc/nginx/sites-available")
os.system("sudo chmod o-rwx /etc/nginx/sites-available")

# give perms to sites-enabled
os.system(f"sudo chown $USER:www-data /etc/nginx/sites-enabled")
os.system("sudo chmod g+s /etc/nginx/sites-enabled")
os.system("sudo chmod o-rwx /etc/nginx/sites-enabled")

# Create a file to give permissions to restart nginx via the fucking_script
if not os.path.exists(ja_websites_folder_path):
    with open("sudo nano /etc/sudoers.d/devloweb", "w") as perms_file:
    	perms_file.write("%grisz ALL=(ALL) NOPASSWD:/bin/systemctl restart nginx
