from flask_restful import Resource
from flask import request, jsonify
from app import db 
from app.models.event import Event
from datetime import datetime
from app.utils import constants

class EventResource(Resource):

    def get(self, id_event=None):
        if id_event:
            event = db.session.get(Event, id_event)
            if event:
                return event.to_dict()
            return {'error': constants.EVENT_NOT_FOUND }, 404
        
        events = Event.query.all()

        if not events:
            return {'message': constants.NO_EVENTS }, 200

        return [event.to_dict() for event in events]
    
    def post(self):
        try:
            # Validar si la solicitud contiene JSON
            if not request.is_json:
                return {"error": constants.INVALID_JSON}, 400

            data = request.get_json()

            # Validar que todos los campos requeridos estén presentes
            required_fields = ["title_event", "date_event", "description_event", "location_event"]
            missing_fields = [field for field in required_fields if field not in data]

            if missing_fields:
                return {"error": constants.MISSING_FIELDS, "fields": missing_fields}, 400  # ✅ Se arregló "fields:"

            # Diccionario con reglas de validación
            validations = {
                "title_event": (str, constants.INVALID_TITLE),
                "description_event": (str, constants.INVALID_DESCRIPTION),
                "location_event": (str, constants.INVALID_LOCATION),
            }

            # Validar campos de tipo string automáticamente
            validated_data = {}
            for field, (expected_type, error_message) in validations.items():
                if not isinstance(data[field], expected_type) or len(data[field].strip()) == 0:
                    return {"error": error_message}, 400
                validated_data[field] = data[field]

            # Validar `date_event` por separado porque requiere conversión
            try:
                validated_data["date_event"] = datetime.strptime(data["date_event"], "%Y-%m-%d").date()
            except ValueError:
                return {"error": constants.DATE_FORMAT_ERROR}, 400

            # Crear el nuevo evento
            new_event = Event(**validated_data)
            db.session.add(new_event)
            db.session.commit()

            return new_event.to_dict(), 201  # ✅ Se elimina `jsonify()`, Flask-RESTful maneja JSON

        except Exception as e:
            return {"error": constants.ERROR_PROCESSING_REQUEST, "details": str(e)}, 500

    def put(self, id_event):
        try:
            # Buscar el evento en la base de datos
            event = db.session.get(Event, id_event)
            if not event:
                return {"error": constants.EVENT_NOT_FOUND}, 404

            # Validar si la solicitud contiene JSON
            if not request.is_json:
                return {"error": constants.INVALID_JSON}, 400

            data = request.get_json()

            # Validar que al menos un campo esté presente
            allowed_fields = ["title_event", "date_event", "description_event", "location_event"]
            if not any(field in data for field in allowed_fields):
                return {"error": constants.EMPTY_UPDATE}, 400

            # Diccionario con reglas de validación
            validations = {
                "title_event": (str, constants.INVALID_TITLE),
                "description_event": (str, constants.INVALID_DESCRIPTION),
                "location_event": (str, constants.INVALID_LOCATION),
            }

            # Validar campos de tipo string automáticamente
            for field, (expected_type, error_message) in validations.items():
                if field in data:
                    if not isinstance(data[field], expected_type) or len(data[field].strip()) == 0:
                        return {"error": error_message}, 400
                    setattr(event, field, data[field])  # ✅ Asignación dinámica

            # Validar `date_event` por separado porque requiere conversión
            if "date_event" in data:
                try:
                    event.date_event = datetime.strptime(data["date_event"], "%Y-%m-%d").date()
                except ValueError:
                    return {"error": constants.DATE_FORMAT_ERROR}, 400

            # Guardar cambios en la base de datos
            db.session.commit()

            return event.to_dict(), 200  # ✅ Respuesta optimizada

        except Exception as e:
            return {"error": constants.ERROR_PROCESSING_REQUEST, "details": str(e)}, 500

        
    def delete(self, id_event):
        try:
            #Busca el evento en la base de datos
            event = db.session.get(Event, id_event)
            if not event:
                return {'error': constants.EVENT_NOT_FOUND }, 404

            #Eliminar el evento
            db.session.delete(event)
            db.session.commit()
            return {'message': constants.EVENT_DELETED, "id_event":id_event }, 200
        except Exception as e:
            return {"error": constants.ERROR_PROCESSING_REQUEST , "details": str(e)}, 500