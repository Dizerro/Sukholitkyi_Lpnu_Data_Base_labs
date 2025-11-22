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

# Літак + весь екіпаж на ньому
@bp.get("/aircraft/<int:aircraft_id>")
def crew_for_aircraft(aircraft_id):
    result = svc.crew_for_aircraft(aircraft_id)
    if not result:
        return {"error": "Aircraft not found"}, 404

    aircraft = result["aircraft"]
    crew = result["crew"]

    return {
        "aircraft": {
            "aircraft_id": aircraft.aircraft_id,
            "registration_number": aircraft.registration_number,
            "serial_number": aircraft.serial_number,
            "airline_id": aircraft.airline_airline_id,
            "model_id": aircraft.aircraft_models_model_id
        },
        "crew": [
            {
                "role": c.role,
                "pilot_id": c.pilot_id,
                "flight_id": c.flight_id
            }
            for c in crew
        ]
    }

# ВСІ літаки + весь екіпаж
@bp.get("/aircraft")
def all_aircraft_with_crew():
    items = svc.crew_for_all_aircraft()

    return [
        {
            "aircraft": {
                "aircraft_id": i["aircraft"].aircraft_id,
                "registration_number": i["aircraft"].registration_number,
                "serial_number": i["aircraft"].serial_number,
                "airline_id": i["aircraft"].airline_airline_id,
                "model_id": i["aircraft"].aircraft_models_model_id
            },
            "crew": [
                {
                    "role": c.role,
                    "pilot_id": c.pilot_id,
                    "flight_id": c.flight_id
                }
                for c in i["crew"]
            ]
        }
        for i in items
    ]

