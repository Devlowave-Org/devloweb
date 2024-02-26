"""IMPORTS"""
import os


"""CODE"""
# Create folder ja in www if it doesn't exist
ja_websites_folder_path = "/var/www/ja"
if not os.path.exists(ja_websites_folder_path):
    os.system(f"sudo mkdir {ja_websites_folder_path}")
    #Give permissions to this folder
    os.system(f"sudo chown $USER:www-data /var/www/ja")
    os.system("sudo chmod g+s /var/www/ja")
    os.system("sudo chmod o-rwx /var/www/ja")
