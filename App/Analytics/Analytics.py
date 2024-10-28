from datetime import datetime, timedelta, timezone
from flask import request, jsonify, session
from uuid import uuid4

def get_analytics(db):
    data = request.get_json()
    # Check si les datas sont correctes
    if not data or 'eventType' not in data:
        return jsonify({"status": "error", "message": "Données invalides"}), 400

    # Traitement en fonction du type d'événement
    event_type = data['eventType']
    if event_type != "page":
        return jsonify({"status": "error", "message": "Données invalides"}), 400

    id_session = id_analytics_sessions(db, data)
    db.add_page_viewed(id_session, data['pageInfo']['url'], data['pageInfo']['duration'], 0, data["time"])


    return jsonify({"status": "success", "message": "Données collectées avec succès"}), 200


def id_analytics_sessions(db, data):
    """Initialise ou récupère une session de tracking"""
    if 'visitor_id' not in session or session["visitor_id_expires_at"] < datetime.now(timezone.utc):
        session_id = str(uuid4())

        db.create_session(session_id, data["deviceInfo"]["deviceType"], data["deviceInfo"]["os"], data["deviceInfo"]["browser"], request.remote_addr)

        session['visitor_id'] = session_id
        session['visitor_id_expires_at'] = datetime.now(timezone.utc) + timedelta(minutes=30)

    session['visitor_id_expires_at'] = datetime.now(timezone.utc) + timedelta(minutes=30)
    print(session['visitor_id_expires_at'])
    print(datetime.now(timezone.utc))
    print(session["visitor_id_expires_at"] < datetime.now(timezone.utc))

    return session['visitor_id']