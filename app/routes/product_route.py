# from flask import Blueprint
# from app.middleware import roles_required

# from app.controllers import student_controller as ctrl

# product_bp = Blueprint("products", __name__, url_prefix="/api/products")


# @product_bp.route("", methods=["POST"])
# @roles_required("admin","product")
# def create_product():
#     return ctrl.create_product()


# @product_bp.route("", methods=["GET"])
# @roles_required("admin")
# def get_products():
#     return ctrl.get_products()


# @product_bp.route("/<int:product_id>", methods=["GET"])
# @roles_required("admin", "product"  )
# def get_product(product_id):
#     return ctrl.get_product(product_id)


# @product_bp.route("/<int:product_id>", methods=["PUT"])
# @roles_required("product")
# def update_product(product_id):
#     return ctrl.update_product(product_id)


# @product_bp.route("/<int:product_id>", methods=["DELETE"])
# @roles_required("admin")
# def delete_product(product_id):
#     return ctrl.delete_product(product_id)


from flask import Blueprint
from app.middleware import roles_required, owner_required
from app.controllers import product_controller as ctrl

product_bp = Blueprint("products",__name__, url_prefix="/api/products")


@product_bp.route("", methods=["GET"])
def get_products():
    return ctrl.get_products()



@product_bp.route("/<int:id>", methods=["GET"])
def get_product(id):
    return ctrl.get_product(id)



@product_bp.route("", methods=["POST"])
@roles_required("seller")
def create_product():
    return ctrl.create_product()



@product_bp.route("/<int:id>", methods=["PUT"])
@roles_required("seller")
@owner_required
def update_product(id):
    return ctrl.update_product(id)



@product_bp.route("/<int:id>", methods=["DELETE"])
@roles_required("seller")
@owner_required
def delete_product(id):
    return ctrl.delete_product(id)



