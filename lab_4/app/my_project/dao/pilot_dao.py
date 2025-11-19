from .base import BaseDAO
from ..domain.models import Pilot

class PilotDAO(BaseDAO):
    def __init__(self):
        super().__init__(Pilot)

    def by_airline(self, airline_id: int):
        return self.model.query.filter_by(airline_airline_id=airline_id).all()
