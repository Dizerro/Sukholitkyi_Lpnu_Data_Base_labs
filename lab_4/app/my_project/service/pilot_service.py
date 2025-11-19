from ..dao.pilot_dao import PilotDAO

class PilotService:
    def __init__(self):
        self.dao = PilotDAO()

    def list(self):
        return self.dao.get_all()

    def get(self, pilot_id: int):
        return self.dao.get(pilot_id)

    def create(self, data: dict):
        return self.dao.create(**data)

    def by_airline(self, airline_id: int):
        return self.dao.by_airline(airline_id)
