from ..dao.airline_dao import AirlineDAO

class AirlineService:
    def __init__(self):
        self.dao = AirlineDAO()

    def list(self):
        return self.dao.get_all()

    def get(self, airline_id: int):
        return self.dao.get(airline_id)

    def create(self, data: dict):
        return self.dao.create(**data)

    def update(self, airline_id: int, data: dict):
        obj = self.dao.get(airline_id)
        return None if not obj else self.dao.update(obj, **data)

    def delete(self, airline_id: int):
        obj = self.dao.get(airline_id)
        if not obj: return False
        self.dao.delete(obj)
        return True
