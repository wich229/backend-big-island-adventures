from app import db

class Tour(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String)
    city = db.Column(db.String)
    address = db.Column(db.String)
    date = db.Column(db.DateTime)
    duration_in_min = db.Column(db.Integer)
    price = db.Column(db.Float)
    category = db.Column(db.String)
    is_outdoor = db.Column(db.Boolean)
    capacity = db.Column(db.Integer)
    bookings = db.relationship("Booking", back_populates="tour")
    
    def to_dict(self):
        return {
            "name": self.name,
            "city": self.city,
            "address": self.address,
            "date": self.date,
            "duration_in_min": self.duration_in_min,
            "price": self.price,
            "category": self.category,
            "is_outdoor": self.is_outdoor,
            "capacity": self.capacity
        }
    
    @classmethod
    def from_dict(cls, tour_data):
        new_tour = Tour(name=tour_data["name"], 
                        city=tour_data["city"], 
                        address=tour_data["address"],
                        date=tour_data["date"],
                        duration_in_min=tour_data["duration_in_min"],
                        price=tour_data["price"],
                        category=tour_data["category"],
                        is_outdoor=tour_data["is_outdoor"],
                        capacity=tour_data["capacity"]
                        )
        return new_tour
    
    def available_capacity(id):
        pass