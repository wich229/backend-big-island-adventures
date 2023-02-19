from app import db
from datetime import datetime
from time import time
class Tour(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String)
    city = db.Column(db.String)
    address = db.Column(db.String)
    date = db.Column(db.DateTime)
    time = db.Column(db.DateTime)
    duration_in_min = db.Column(db.Integer)
    price = db.Column(db.Float)
    category = db.Column(db.String)
    is_outdoor = db.Column(db.Boolean)
    capacity = db.Column(db.Integer)
    bookings = db.relationship("Booking", back_populates="tour")
    description = db.Column(db.String)
    photo_url = db.Column(db.String)
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "city": self.city,
            "address": self.address,
            "date": self.date.strftime('%-m/%-d/%Y'),
            "duration_in_min": self.duration_in_min,
            "price": self.price,
            "category": self.category,
            "is_outdoor": self.is_outdoor,
            "capacity": self.capacity,
            "description": self.description,
            "photo_url": self.photo_url,
            "time": self.time
        }
    
    @classmethod
    def from_dict(cls, tour_data):
        new_tour = Tour(
            name=tour_data["name"], 
            city=tour_data["city"], 
            address=tour_data["address"],
            date=datetime.strptime(tour_data["date"], ('%m/%d/%Y')),
            duration_in_min=tour_data["duration_in_min"],
            price=tour_data["price"],
            category=tour_data["category"],
            is_outdoor=tour_data["is_outdoor"],
            capacity=tour_data["capacity"],
            description=tour_data["description"],
            photo_url=tour_data["photo_url"],
            time=tour_data["time"]
        )
        return new_tour
    
    # updated -------------------------------------------------------
    def available_capacity(self):
        # looping through the bookings to count the saled tickets
        total_saled = sum([ each_booking.tickets for each_booking in self.bookings])
        
        available_capacity = self.capacity - total_saled
        return available_capacity