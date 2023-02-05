from app import db

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    name = db.Column(db.String)
    email = db.Column(db.String) 
    phone = db.Column(db.String) 
    password = db.Column(db.String)
    tours = db.relationship("Tour", secondary="booking", back_populates="customers")


    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone
        }
    
    @classmethod
    def from_dict(cls, data):
        pass
    
    