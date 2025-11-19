from flask import Blueprint, request, jsonify, abort
from marshmallow import fields
from ..utils.db import ma
from ..service.airline_service import AirlineService
from ..service.pilot_service import PilotService

bp = Blueprint("airlines", __name__, url_prefix="/api/airlines")
airline_svc = AirlineService()
pilot_svc = PilotService()

class AirlineSchema(ma.Schema):
    airline_id = fields.Int(dump_only=True)
    name = fields.Str()
    icao_code = fields.Str()
    iata_code = fields.Str()
    country = fields.Str()

airline_schema = AirlineSchema()
airlines_schema = AirlineSchema(many=True)

@bp.get("/")
def list_airlines():
    return airlines_schema.jsonify(airline_svc.list())

@bp.post("/")
def create_airline():
    data = airline_schema.load(request.json)
    obj = airline_svc.create(data)
    return airline_schema.jsonify(obj), 201

@bp.get("/<int:airline_id>")
def get_airline(airline_id):
    obj = airline_svc.get(airline_id)
    if not obj: abort(404)
    return airline_schema.jsonify(obj)

@bp.put("/<int:airline_id>")
def update_airline(airline_id):
    data = airline_schema.load(request.json, partial=True)
    obj = airline_svc.update(airline_id, data)
    if not obj: abort(404)
    return airline_schema.jsonify(obj)

@bp.delete("/<int:airline_id>")
def delete_airline(airline_id):
    ok = airline_svc.delete(airline_id)
    if not ok: abort(404)
    return "", 204

# M:1 — усі пілоти конкретної авіалінії
@bp.get("/<int:airline_id>/pilots")
def pilots_for_airline(airline_id):
    pilots = pilot_svc.by_airline(airline_id)
    class PilotSchema(ma.Schema):
        pilot_id = fields.Int()
        first_name = fields.Str()
        last_name = fields.Str()
        license_number = fields.Str()
        exp_years = fields.Int()
        airline_airline_id = fields.Int()
    return PilotSchema(many=True).jsonify(pilots)
