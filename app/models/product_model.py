from app.extensions import db
from app.utils import utc_now


class Student(db.Model):
    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    seller_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    image_url = db.Column(db.String(255), nullable=True)
    is_active = db.Column(db.Boolean, default=True)


    def to_dict(self):
        return {
            "id": self.id,
            "seller_id": self.seller_id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "stock": self.stock,
            "image_url": self.image_url,
            "is_active": self.is_active,
        }
