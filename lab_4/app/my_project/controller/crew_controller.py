from flask import Blueprint, request
from marshmallow import fields, validate
from ..utils.db import ma
from ..service.crew_service import CrewService

bp = Blueprint("crew", __name__, url_prefix="/api/crew")
svc = CrewService()

class CrewSchema(ma.Schema):
    flight_id = fields.Int()
    pilot_id  = fields.Int()
    role = fields.Str(validate=validate.OneOf(["Captain","First Officer","Flight Engineer"]))

crew_schema = CrewSchema()
crew_many = CrewSchema(many=True)

# Додати пілота до екіпажу рейсу
@bp.post("/")
def add_member():
    data = crew_schema.load(request.json)
    member = svc.add(**data)
    return crew_schema.jsonify(member), 201

# Увесь екіпаж рейсу
@bp.get("/flight/<int:flight_id>")
def list_for_flight(flight_id):
    return crew_many.jsonify(svc.for_flight(flight_id))

# Усі рейси, де працює пілот
@bp.get("/pilot/<int:pilot_id>")
def list_for_pilot(pilot_id):
    return crew_many.jsonify(svc.for_pilot(pilot_id))

# Видалити члена екіпажу
@bp.delete("/")
def delete_member():
    data = crew_schema.load(request.json)
    svc.delete(**data)
    return "", 204
