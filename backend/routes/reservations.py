from flask import Blueprint, request, jsonify
from models import Reservation, db

# define blueprint
reservations_bp = Blueprint('reservations', __name__, url_prefix='/reservations')

# read all reservations
@reservations_bp.route("/", methods=["GET"], strict_slashes=False)
def get_reservations():
    reservations = Reservation.query.all()
    json_reservations = list(map(lambda x: x.reservation_to_json(), reservations))
    return jsonify({"reservations": json_reservations})