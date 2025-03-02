from app import db

class Event(db.Model):
    id_event = db.Column(db.Integer, primary_key=True)
    title_event = db.Column(db.String(150), nullable=False)
    date_event = db.Column(db.Date, nullable=False)
    description_event = db.Column(db.Text, nullable=False)
    location_event = db.Column(db.String(150), nullable=False)

    def to_dict(self):
        return {
            'id_event': self.id_event,
            'title_event': self.title_event,
            'date_event': self.date_event,
            'description_event': self.description_event,
            'location_event': self.location_event
        }