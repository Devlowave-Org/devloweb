import os

gmail_app = os.environ.get("GMAIL_APP")
server_name = os.environ.get("SERVER_NAME")
env = os.environ.get("ENV")

print("GMAIL_APP:", gmail_app)
print("SERVER_NAME:", server_name)
print("ENV:", env)
