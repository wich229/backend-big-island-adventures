from app import db

class Tour(db.Model):
    # NOTE: I dont think we need an end date or due date for registering
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String)
    city = db.Column(db.String)
    address = db.Column(db.String)
    date = db.Column(db.DateTime)
    duration_in_min = db.Column(db.Integer)
    price = db.Column(db.Float) # or decimal?
    category = db.Column(db.String)
    is_outdoor = db.Column(db.Bool) # or string? can tours be indoor and outdoor?
    capacity = db.Column(db.Integer)
    customers = db.relationship("Customer", secondary="booking", back_populates="tour")
    
    def to_dict(self):
        return {
        }
    
    @classmethod
    def from_dict(cls, data):
        pass
    
    def available_capacity(id):
        pass