from app.extensions import db
from app.utils import utc_now


class Student(db.Model):
    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, nullable=False)
    product_id = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Float, nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), nullable=False, default="pending")
    shipping_address = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=utc_now)
   


    def to_dict(self):
        return {
            "id": self.id,
            "customer_id": self.customer_id,
            "product_id": self.product_id,
            "quantity": self.quantity,
            "unit_price": self.unit_price,
            "total_amount": self.total_amount,
            "status": self.status,
            "shipping_address": self.shipping_address,
            "created_at": self.created_at
        }
