from app.config import db

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tittle = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    # capacity = db.Column(db.Integer, nullable=False)
    # attendees = db.relationship('Attendee', backref='event', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'tittle': self.tittle,
            'date': self.date,
            'description': self.description,
            'location': self.location
        }