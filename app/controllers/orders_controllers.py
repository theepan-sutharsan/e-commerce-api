from datetime import datetime

from flask import jsonify, request

from app.extensions import db
from app.models.order_model import order





def _validate_order_payload(data, order_id=None):
    errors = []
    if not data:
        return ["Request body is required."]

    quantity = data.get("quantity")
    if quantity is None:
        errors.append("quantity is required.")
    else:
        try:
            quantity_val = int(quantity)
            if quantity_val <= 0:
                errors.append("quantity must be a positive integer.")
        except (TypeError, ValueError):
            errors.append("quantity must be a positive integer.")

    unit_price = data.get("unit_price")
    if unit_price is None:
        errors.append("unit_price is required.")
    else:
        try:
            unit_price_val = float(unit_price)
            if unit_price_val <= 0:
                errors.append("unit_price must be a positive number.")
        except (TypeError, ValueError):
            errors.append("unit_price must be a positive number.")

    total_amount = data.get("total_amount")
    if total_amount is None:
        errors.append("total_amount is required.")
    else:
        try:
            total_amount_val = int(total_amount)
            if total_amount_val < 0:
                errors.append("total_amount must be a non-negative integer.")
        except (TypeError, ValueError):
            errors.append("total_amount must be a non-negative integer.")


    status = data.get("status")
    if status is None or str(status).strip() == "":
        errors.append("status is required.")


    shipping_address = data.get("shipping_address")
    if shipping_address is None or str(shipping_address).strip() == "":
        errors.append("shipping_address is required.")

    created_at = data.get("created_at")
    if created_at is None or str(created_at).strip() == "": 
        errors.append("created_at is required.")                



    return errors


def create_order():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Request body is required."}), 400

    errors = _validate_order_payload(data)
    if errors:
        return jsonify({"errors": errors}), 400

   
    try:
        order = order(
            name=data.get("name").strip(),
            description=data.get("description"),
            price=float(data.get("price")),
            stock=int(data.get("stock")),
            image_url=data.get("image_url"),
            is_active=data.get("is_active", True),
        )
        db.session.add(order)
        db.session.commit()
        return jsonify({"message": "order created successfully.", "order": order.to_dict()}), 201
    except Exception:
        db.session.rollback()
        return jsonify({"error": "An internal server error occurred."}), 500


def get_orders():
    orders = order.query.all()
    return jsonify({"orders": [s.to_dict() for s in orders]}), 200


def get_order(order_id):
    order = order.query.get(order_id)
    if not order:
        return jsonify({"error": "order not found."}), 404
    return jsonify({"order": order.to_dict()}), 200


def update_order(order_id):
    order = order.query.get(order_id)
    if not order:
        return jsonify({"error": "order not found."}), 404

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "No data provided to update."}), 400

    errors = _validate_order_payload(data, order_id=order_id)
    if errors:
        return jsonify({"errors": errors}), 400



    try:
        order.name = data.get("name").strip()
        order.description = data.get("description")
        order.price = float(data.get("price"))
        order.stock = int(data.get("stock"))
        order.image_url = data.get("image_url")
        if "is_active" in data:
            order.is_active = bool(data.get("is_active"))
       
        db.session.commit()
        return jsonify({"message": "order updated successfully.", "order": order.to_dict()}), 200
    except Exception:
        db.session.rollback()
        return jsonify({"error": "An internal server error occurred."}), 500


def delete_order(order_id):
    order = order.query.get(order_id)
    if not order:
        return jsonify({"error": "order not found."}), 404
    try:
        db.session.delete(order)
        db.session.commit()
        return jsonify({"message": "order deleted successfully."}), 200
    except Exception:
        db.session.rollback()
        return jsonify({"error": "An internal server error occurred."}), 500
