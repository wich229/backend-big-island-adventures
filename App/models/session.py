from app import db
import datetime

class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    customer_id = db.Column(db.Integer, db.ForeignKey("customer.id"))
    customer = db.relationship("Customer", back_populates="sessions")
    is_active = db.Column(db.Boolean)
    # create_timestamp = db.Column(db.DateTime, default = (datetime.date.today()))
    create_timestamp = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    

    
    def to_dict(self):
        return {
            "id": self.id,
            "customer_id": self.customer_id,
            "is_active": self.is_active,
            "create_timestamp": self.create_timestamp

        }
    
    @classmethod
    def from_dict(cls, session_data):
        session = Session(
            id=session_data["id"],
            customer_id = session_data["customer_id"],
            is_active = session_data["is_active"],
            create_timestamp = session_data["create_timestamp"]
        )
        return session
    
