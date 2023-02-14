from app import db

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    name = db.Column(db.String)
    email = db.Column(db.String) 
    phone = db.Column(db.String) 
    password = db.Column(db.String)
    bookings = db.relationship("Booking", back_populates="customer")
    sessions = db.relationship("Session", back_populates="customer")

    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "password": self.password,
            "bookings": [list(booking.to_dict()) for booking in self.bookings],
            "sessions": [list(session.to_dict()) for session in self.sessions]
        }
    
    @classmethod
    def from_dict(cls, customer_data):
        new_customer = Customer(
            name=customer_data["name"],
            email = customer_data["email"],
            phone = customer_data["phone"],
            password = customer_data["password"]
        )
        return new_customer


# drop database touring_api_test;
# drop database touring_api_development;
# create database touring_api_test;
# create database touring_api_development;
# flask db init; flask db migrate -m "init" ; flask db upgrade 