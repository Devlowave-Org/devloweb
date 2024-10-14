from flask import request

def generate_details_area_dict(db, ja_id):
    ja_details = {
        "id": ja_id,
        "name": db.get_ja_name_by_id(ja_id)[0],
        "subdomain": db.get_ja_domain_by_id(ja_id)[0],
        "status": db.get_website_status_by_id(ja_id)[0],
        "preview_link": None, # Include here the preview or link to the site when i'll have it
        "host_demand" : manage_hosting_demand(db, ja_id),
        "error": None
    }

    if ja_details["host_demand"] :
        ja_details["status"] = db.get_website_status_by_id(ja_id)[0]


    return ja_details

def manage_hosting_demand(db, ja_id):
    ja_id = int(ja_id)
    if request.form.get("accept_button"):
        db.update_website_status_by_id(ja_id, 1)
        # Also need to send the mail here
        return True
    elif request.form.get("reject_button"):
        if request.form.get("reject_message"):
            db.update_website_status_by_id(ja_id, 3)
            # Also need to send the mail here
            return request.form.get("reject_message")
        return False
    else:
        return None
