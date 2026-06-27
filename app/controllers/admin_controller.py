from datetime import datetime

from flask import jsonify, request

from app.extensions import db
from app.models.order_model import admin





def _validate_admin_payload(data, admin_id=None):
    errors = []
    if not data:
        return ["Request body is required."]

    name = data.get("name")
    if name is None or str(name).strip() == "":
        errors.append("name is required.")

    price = data.get("price")
    if price is None:
        errors.append("price is required.")
    else:
        try:
            price_val = float(price)
            if price_val <= 0:
                errors.append("price must be a positive number.")
        except (TypeError, ValueError):
            errors.append("price must be a positive number.")

    stock = data.get("stock")
    if stock is None:
        errors.append("stock is required.")
    else:
        try:
            stock_val = int(stock)
            if stock_val < 0:
                errors.append("stock must be a non-negative integer.")
        except (TypeError, ValueError):
            errors.append("stock must be a non-negative integer.")



    return errors


def create_admin():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Request body is required."}), 400

    errors = _validate_admin_payload(data)
    if errors:
        return jsonify({"errors": errors}), 400

   
    try:
        admin = admin(
            name=data.get("name").strip(),
            description=data.get("description"),
            price=float(data.get("price")),
            stock=int(data.get("stock")),
            image_url=data.get("image_url"),
            is_active=data.get("is_active", True),
        )
        db.session.add(admin)
        db.session.commit()
        return jsonify({"message": "admin created successfully.", "admin": admin.to_dict()}), 201
    except Exception:
        db.session.rollback()
        return jsonify({"error": "An internal server error occurred."}), 500


def get_admins():
    admins = admin.query.all()
    return jsonify({"admins": [s.to_dict() for s in admins]}), 200


def get_admin(admin_id):
    admin = admin.query.get(admin_id)
    if not admin:
        return jsonify({"error": "admin not found."}), 404
    return jsonify({"admin": admin.to_dict()}), 200


def update_admin(admin_id):
    admin = admin.query.get(admin_id)
    if not admin:
        return jsonify({"error": "admin not found."}), 404

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "No data provided to update."}), 400

    errors = _validate_admin_payload(data, admin_id=admin_id)
    if errors:
        return jsonify({"errors": errors}), 400



    try:
        admin.name = data.get("name").strip()
        admin.description = data.get("description")
        admin.price = float(data.get("price"))
        admin.stock = int(data.get("stock"))
        admin.image_url = data.get("image_url")
        if "is_active" in data:
            admin.is_active = bool(data.get("is_active"))
       
        db.session.commit()
        return jsonify({"message": "admin updated successfully.", "admin": admin.to_dict()}), 200
    except Exception:
        db.session.rollback()
        return jsonify({"error": "An internal server error occurred."}), 500


def delete_admin(admin_id):
    admin = admin.query.get(admin_id)
    if not admin:
        return jsonify({"error": "admin not found."}), 404
    try:
        db.session.delete(admin)
        db.session.commit()
        return jsonify({"message": "admin deleted successfully."}), 200
    except Exception:
        db.session.rollback()
        return jsonify({"error": "An internal server error occurred."}), 500
