from flask import request

def generate_details_area_dict(db, ja_id):
    ja_details = {
        "id": ja_id,
        "name": db.get_ja_name_by_id(ja_id)[0],
        "subdomain": db.get_ja_domain_by_id(ja_id)[0],
        "status": db.get_website_status_by_id(ja_id)[0],
        "preview_link": None, # Include here the preview or link to the site when i'll have it
        "status_modification" : manage_status_modification(db, ja_id),
        "error": None
    }

    if ja_details["status_modification"] :
        ja_details["status"] = db.get_website_status_by_id(ja_id)[0]


    return ja_details

def manage_status_modification(db, ja_id):
    if request.form.get("accept_button") or request.form.get("activate_button"):
        if request.form.get("accept_confirmation") == "oui" or request.form.get("activate_confirmation") == "oui":
            db.update_website_status_by_id(ja_id, 1)
            # Also need to send the mail here
            return True
        elif request.form.get("activate_confirmation") == "non" or request.form.get("accept_confirmation") == "non":
            return request.form.get("activate_button")
        return 1
    elif request.form.get("reject_button") or request.form.get("deactivate_button"):
        if request.form.get("reject_message"):
            db.update_website_status_by_id(ja_id, 3)
            # Also need to send the mail here
            return request.form.get("reject_message")
        return False

    elif request.form.get("reset_button"):
        if request.form.get("reset_message"):
            db.update_website_status_by_id(ja_id, 0)
            # Also delete the website and all
            # Also need to send the mail here
            return request.form.get("reset_message")
        return 0

    # Otherwise (it is not supposed to happen)
    else:
        return None
