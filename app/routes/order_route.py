from flask import Blueprint
from app.middleware import roles_required, owner_required
from app.controllers import order_controller as ctrl

order_bp = Blueprint("orders",__name__, url_prefix="/api/orders")


@order_bp.route("", methods=["GET"])
def get_orders():
    return ctrl.get_orders()



@order_bp.route("/<int:id>", methods=["GET"])
def get_order(id):
    return ctrl.get_order(id)



@order_bp.route("", methods=["POST"])
@roles_required("seller")
def create_order():
    return ctrl.create_order()



@order_bp.route("/<int:id>", methods=["PUT"])
@roles_required("seller")
@owner_required
def update_order(id):
    return ctrl.update_order(id)



@order_bp.route("/<int:id>", methods=["DELETE"])
@roles_required("seller")
@owner_required
def delete_order(id):
    return ctrl.delete_order(id)