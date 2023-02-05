from app import db

class Booking(db.Model):
    __tablename__ = "booking"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    tour_id = db.Column(db.Integer, db.ForeignKey('tour.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    booking_date = db.Column(db.DateTime)
    status = db.Column(db.String)
    tickets = db.Column(db.Number)
    
    
    
    def to_dict(self):
        return {
        }


    @classmethod
    def from_dict(cls, data):
        pass
    

    