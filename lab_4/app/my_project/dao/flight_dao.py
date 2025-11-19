from .base import BaseDAO
from ..domain.models import Flight

class FlightDAO(BaseDAO):
    def __init__(self):
        super().__init__(Flight)

    def crew_for_flight(self, flight_id: int):
        f = self.get(flight_id)
        return [] if not f else f.crew
