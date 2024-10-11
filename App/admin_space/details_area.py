def generate_details_area_dict(db, ja_id):
    ja_details = {
        "id": ja_id,
        "name": db.get_ja_name_by_id(ja_id)[0],
        "subdomain": db.get_ja_domain_by_id(ja_id)[0],
        "status": str(db.get_website_status_by_id(ja_id)[0]),
        "requires_review": None,
        "error": None
    }
    if ja_details["status"] == 2:
        ja_details["requires_review"] = True

    return ja_details