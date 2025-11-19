from flask import Blueprint, request, abort
from marshmallow import fields
from ..utils.db import ma
from ..service.pilot_service import PilotService

bp = Blueprint("pilots", __name__, url_prefix="/api/pilots")
svc = PilotService()

class PilotSchema(ma.Schema):
    pilot_id = fields.Int(dump_only=True)
    first_name = fields.Str()
    last_name = fields.Str()
    license_number = fields.Str()
    exp_years = fields.Int()
    airline_airline_id = fields.Int()

pilot_schema = PilotSchema()
pilots_schema = PilotSchema(many=True)

@bp.get("/")
def list_pilots():
    return pilots_schema.jsonify(svc.list())

@bp.post("/")
def create_pilot():
    obj = svc.create(pilot_schema.load(request.json))
    return pilot_schema.jsonify(obj), 201

@bp.get("/<int:pilot_id>")
def get_pilot(pilot_id):
    obj = svc.get(pilot_id)
    if not obj: abort(404)
    return pilot_schema.jsonify(obj)
