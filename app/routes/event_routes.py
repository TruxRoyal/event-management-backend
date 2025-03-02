from flask_restful import Resource
from flask import request, jsonify
from app import db 
from app.models.event import Event

class EventResource(Resource):
    def get(self, id_event=None):
        if id_event:
            event = Event.query.get(id_event)
            if event:
                return event.to_dict()
            return {'error': 'Evento no encontrado'}, 404
        
        events = Event.query.all()

        if not events:
            return {'message': 'No hay eventos'}, 200

        return [event.to_dict() for event in events]
    
    def post(self):
        data = request.json
        new_event = Event(
            title_event=data['title_event'],
            date_event=data['date_event'],
            description_event=data['description_event'],
            location_event=data['location_event'],
        )
        db.session.add(new_event)
        db.session.commit()
        return jsonify(new_event.to_dict()), 201
    def put(self, id_event):
        event = Event.query.get(id_event)
        if not event:
            return jsonify({'error': 'Evento no encontrado'}), 404
        else:
            data = request.json
            event.title_event = data['title_event']
            event.date_event = data['date_event']
            event.description_event = data['description_event']
            event.location_event = data['location_event']
            db.session.commit()
            return jsonify(event.to_dict())
    def delete(self, id_event):
        event = Event.query.get(id_event)
        if not event:
            return jsonify({'error': 'Evento no encontrado'}), 404
        else:
            db.session.delete(event)
            db.session.commit()
            return jsonify({'message': 'Evento eliminado'}), 200