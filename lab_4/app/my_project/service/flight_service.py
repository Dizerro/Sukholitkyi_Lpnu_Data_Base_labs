from ..dao.flight_dao import FlightDAO

class FlightService:
    def __init__(self):
        self.dao = FlightDAO()

    def list(self):
        return self.dao.get_all()

    def get(self, flight_id: int):
        return self.dao.get(flight_id)
