from flask import Blueprint, request, jsonify
from app.config import db
from app.models import Event

event_bp = Blueprint('event_bp', __name__)

@event_bp.route('/', methods=['GET'])
def get_events():
    events = Event.query.all()
    return jsonify([event.to_dict() for event in events])

@event_bp.route('/<int:id>', methods=['GET'])
def get_event(id):
    event = Event.query.get(id)
    if event:
        return jsonify(event.to_dict())
    return jsonify({'error': 'Event not found'}), 404

@event_bp.route('/', methods=['POST'])
def create_event():
    data = request.get_json()
    new_event = Event(
        tittle=data['tittle'],
        date=data['date'],
        description=data['description'],
        location=data['location'],
    )
    db.session.add(new_event)
    db.session.commit()
    return jsonify(new_event.to_dict()), 201

@event_bp.route('/<int:id>', methods=['PUT'])
def update_event(id):
    event = Event.query.get(id)

    if not event:
        return jsonify({'error': 'Event not found'}), 404
    else:
        data = request.get_json()
        event.tittle = data['tittle']
        event.date = data['date']
        event.description = data['description']
        event.location = data['location']

        db.session.commit()
        return jsonify(event.to_dict())
    
@event_bp.route('/<int:id>', methods=['DELETE'])
def delete_event(id):
    event = Event.query.get(id)
    if not event:
        return jsonify({'error': 'Event not found'}), 404
    else:
        db.session.delete(event)
        db.session.commit()
        return jsonify({'message': 'Event deleted'})

    