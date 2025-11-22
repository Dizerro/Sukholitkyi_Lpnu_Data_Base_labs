from ..dao.crew_dao import CrewDAO
from my_project.utils.db import db
from my_project.domain.models import Flight
from my_project.domain.models import Aircraft
from my_project.domain.models import FlightCrew

class CrewService:
    def __init__(self):
        self.dao = CrewDAO()

    def add(self, flight_id: int, pilot_id: int, role: str):
        return self.dao.add_member(flight_id, pilot_id, role)

    def for_flight(self, flight_id: int):
        return self.dao.list_for_flight(flight_id)

    def for_pilot(self, pilot_id: int):
        return self.dao.list_for_pilot(pilot_id)

    def delete(self, flight_id: int, pilot_id: int, role: str):
        self.dao.delete_member(flight_id, pilot_id, role)
    
    def crew_for_aircraft(self, aircraft_id):
        # Знайти літаки
        aircraft = Aircraft.query.get(aircraft_id)
        if not aircraft:
            return None

        # Усі рейси цього літака
        flights = Flight.query.filter_by(aircrafts_aircraft_id=aircraft_id).all()
        flight_ids = [f.flight_id for f in flights]

        if len(flight_ids) == 0:
            return {
                "aircraft": aircraft,
                "crew": []
            }

        # Екіпаж по всіх рейсах
        crew = FlightCrew.query.filter(FlightCrew.flight_id.in_(flight_ids)).all()

        return {
            "aircraft": aircraft,
            "crew": crew
        }
    def crew_for_all_aircraft(self):
        from my_project.domain.models import Aircraft, Flight, FlightCrew

        result = []

        # Всі літаки
        aircrafts = Aircraft.query.all()

        for aircraft in aircrafts:
            flights = Flight.query.filter_by(aircrafts_aircraft_id=aircraft.aircraft_id).all()
            flight_ids = [f.flight_id for f in flights]

            if flight_ids:
                crew = FlightCrew.query.filter(FlightCrew.flight_id.in_(flight_ids)).all()
            else:
                crew = []

            result.append({
                "aircraft": aircraft,
                "crew": crew
            })

        return result

