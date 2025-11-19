from .base import BaseDAO
from ..domain.models import Airline

class AirlineDAO(BaseDAO):
    def __init__(self):
        super().__init__(Airline)
