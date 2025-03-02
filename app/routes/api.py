from flask_restful import Api
from app.routes.event_routes import EventResource

def register_api(app):
    api = Api(app)
    api.add_resource(EventResource, '/api/events', '/api/events/<int:id_event>')