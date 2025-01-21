from flask import Blueprint, request, jsonify
from models import Checkout, db

# define blueprint
checkouts_bp = Blueprint('checkouts', __name__, url_prefix='/checkouts')

# read all checkouts
@checkouts_bp.route("/", methods=["GET"], strict_slashes=False)
def get_checkouts():
    checkouts = Checkout.query.all()
    json_checkouts = list(map(lambda x: x.checkout_to_json(), checkouts))
    return jsonify({"checkouts": json_checkouts})