from app import db
import datetime

class Booking(db.Model):
    __tablename__ = "booking"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("customer.id"))
    customer = db.relationship("Customer", back_populates="bookings")
    tour_id = db.Column(db.Integer, db.ForeignKey("tour.id"))
    tour = db.relationship("Tour", back_populates="bookings")
    booking_date = db.Column(db.DateTime, default = (datetime.date.today()))
    status = db.Column(db.String, default = "confirmed")
    tickets = db.Column(db.Integer)
    
    
    def to_dict(self):
        return {
            "id": self.id,
            "customer_id": self.customer_id,
            "tour_id": self.tour_id,
            "booking_date": self.booking_date.strftime("%Y-%m-%d"),
            "status": self.status,
            "tickets": self.tickets,
            "tour": self.tour.to_dict()
        }


    @classmethod
    def from_dict(cls, booking_data):
        new_booking = Booking(
            # no need because they are default
            # booking_date = booking_data["booking_date"],
            # status = booking_data["status"],
            # customer_id = booking_data["customer_id"],
            # tour_id = booking_data["tour_id"],
            tickets = booking_data["tickets"]
        )
        return new_booking

    