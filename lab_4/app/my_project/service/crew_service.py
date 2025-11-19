from ..dao.crew_dao import CrewDAO

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
