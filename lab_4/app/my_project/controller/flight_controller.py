from flask import Blueprint, abort
from marshmallow import fields
from ..utils.db import ma
from ..service.flight_service import FlightService

bp = Blueprint("flights", __name__, url_prefix="/api/flights")
svc = FlightService()

class FlightSchema(ma.Schema):
    flight_id = fields.Int()
    flight_number = fields.Str()
    scheduled_departure = fields.Date()
    scheduled_arrival = fields.Date()
    actual_departure = fields.Date(allow_none=True)
    actual_arrival = fields.Str(allow_none=True)
    airline_airline_id = fields.Int()
    routes_route_id = fields.Int()
    flight_statuses_status_id = fields.Int()
    aircrafts_aircraft_id = fields.Int()

flight_schema = FlightSchema()
flights_schema = FlightSchema(many=True)

@bp.get("/")
def list_flights():
    return flights_schema.jsonify(svc.list())

@bp.get("/<int:flight_id>")
def get_flight(flight_id):
    obj = svc.get(flight_id)
    if not obj: abort(404)
    return flight_schema.jsonify(obj)
