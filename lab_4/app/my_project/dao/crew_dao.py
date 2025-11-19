from ..utils.db import db
from ..domain.models import FlightCrew

class CrewDAO:
    def add_member(self, flight_id: int, pilot_id: int, role: str):
        member = FlightCrew(flight_id=flight_id, pilot_id=pilot_id, role=role)
        db.session.add(member)
        db.session.commit()
        return member

    def list_for_flight(self, flight_id: int):
        return FlightCrew.query.filter_by(flight_id=flight_id).all()

    def list_for_pilot(self, pilot_id: int):
        return FlightCrew.query.filter_by(pilot_id=pilot_id).all()

    def delete_member(self, flight_id: int, pilot_id: int, role: str):
        FlightCrew.query.filter_by(flight_id=flight_id, pilot_id=pilot_id, role=role).delete()
        db.session.commit()
