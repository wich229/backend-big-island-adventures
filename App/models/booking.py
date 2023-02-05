from app import db

class Booking(db.Model):
    __tablename__ = "booking"
    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    customer_id = db.Column(db.Integer, db.ForeignKey("customer.id"))
    customer = db.relationship("Customer", back_populates="bookings")
    tour_id = db.Column(db.Integer, db.ForeignKey("tour.id"))
    tour = db.relationship("Tour", back_populates="bookings")
    booking_date = db.Column(db.DateTime)
    status = db.Column(db.String)
    tickets = db.Column(db.Integer)
    
    
    def to_dict(self):
        return {
            "id": self.id,
            "booking_date": self.booking_date,
            "status": self.status,
            "tickets": self.tickets
        }


    @classmethod
    def from_dict(cls, booking_data):
        new_booking = Booking(
            booking_date = booking_data["booking_date"],
            status = booking_data["status"],
            tickets = booking_data["tickets"]
        )
        return new_booking

    