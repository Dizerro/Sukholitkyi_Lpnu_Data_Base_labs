from . import models  # not required, but keeps style
from ..utils.db import db

# Табл. aircraft_models
class AircraftModel(db.Model):
    __tablename__ = "aircraft_models"
    model_id = db.Column(db.Integer, primary_key=True)
    manufacturer = db.Column(db.String(45))
    model_name = db.Column(db.String(45))
    range_km = db.Column(db.Integer)
    max_speed_kmh = db.Column(db.Integer)
    capacity = db.Column(db.String(45))

    aircrafts = db.relationship("Aircraft", back_populates="model")

# Табл. airline
class Airline(db.Model):
    __tablename__ = "airline"
    airline_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45))
    icao_code = db.Column(db.String(3), unique=True)
    iata_code = db.Column(db.String(2), unique=True)
    country = db.Column(db.String(45))

    aircrafts = db.relationship("Aircraft", back_populates="airline")
    pilots = db.relationship("Pilot", back_populates="airline")
    flights = db.relationship("Flight", back_populates="airline")

# Табл. aircrafts
class Aircraft(db.Model):
    __tablename__ = "aircrafts"
    aircraft_id = db.Column(db.Integer, primary_key=True)
    registration_number = db.Column(db.String(45), unique=True)
    serial_number = db.Column(db.String(45), unique=True)
    year_of_production = db.Column(db.String(45))
    total_flight_hours = db.Column(db.String(45))

    airline_airline_id = db.Column(db.Integer, db.ForeignKey("airline.airline_id"), nullable=False)
    aircraft_models_model_id = db.Column(db.Integer, db.ForeignKey("aircraft_models.model_id"), nullable=False)

    airline = db.relationship("Airline", back_populates="aircrafts")
    model = db.relationship("AircraftModel", back_populates="aircrafts")
    flights = db.relationship("Flight", back_populates="aircraft")

# Табл. airports
class Airport(db.Model):
    __tablename__ = "airports"
    airport_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45))
    iata_code = db.Column(db.String(3), unique=True)
    icao_code = db.Column(db.String(4), unique=True)
    city = db.Column(db.String(45))

    statuses = db.relationship("FlightStatus", back_populates="airport")
    routes = db.relationship("Route", back_populates="airport")

# Табл. flight_statuses
class FlightStatus(db.Model):
    __tablename__ = "flight_statuses"
    status_id = db.Column(db.Integer, primary_key=True)
    status_name = db.Column(db.Enum("Scheduled","En Route","Landed","Cancelled"))
    airports_airport_id = db.Column(db.Integer, db.ForeignKey("airports.airport_id"), nullable=False)

    airport = db.relationship("Airport", back_populates="statuses")
    flights = db.relationship("Flight", back_populates="status")

# Табл. routes
class Route(db.Model):
    __tablename__ = "routes"
    route_id = db.Column(db.Integer, primary_key=True)
    distance_km = db.Column(db.String(45))
    airports_airport_id = db.Column(db.Integer, db.ForeignKey("airports.airport_id"), nullable=False)

    airport = db.relationship("Airport", back_populates="routes")
    flights = db.relationship("Flight", back_populates="route")

# Табл. flights
class Flight(db.Model):
    __tablename__ = "flights"
    flight_id = db.Column(db.Integer, primary_key=True)
    flight_number = db.Column(db.String(45), unique=True)
    scheduled_departure = db.Column(db.Date)
    scheduled_arrival = db.Column(db.Date)
    actual_departure = db.Column(db.Date)
    actual_arrival = db.Column(db.String(45))

    airline_airline_id = db.Column(db.Integer, db.ForeignKey("airline.airline_id"), nullable=False)
    routes_route_id = db.Column(db.Integer, db.ForeignKey("routes.route_id"), nullable=False)
    flight_statuses_status_id = db.Column(db.Integer, db.ForeignKey("flight_statuses.status_id"), nullable=False)
    aircrafts_aircraft_id = db.Column(db.Integer, db.ForeignKey("aircrafts.aircraft_id"), nullable=False)

    airline = db.relationship("Airline", back_populates="flights")
    route = db.relationship("Route", back_populates="flights")
    status = db.relationship("FlightStatus", back_populates="flights")
    aircraft = db.relationship("Aircraft", back_populates="flights")

    crew = db.relationship("FlightCrew", back_populates="flight", cascade="all, delete-orphan")
    positions = db.relationship("FlightPosition", back_populates="flight", cascade="all, delete-orphan")

# Табл. pilots
class Pilot(db.Model):
    __tablename__ = "pilots"
    pilot_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(45))
    last_name = db.Column(db.String(45))
    license_number = db.Column(db.String(45), unique=True)
    exp_years = db.Column(db.Integer)

    airline_airline_id = db.Column(db.Integer, db.ForeignKey("airline.airline_id"), nullable=False)
    airline = db.relationship("Airline", back_populates="pilots")

    crew = db.relationship("FlightCrew", back_populates="pilot", cascade="all, delete-orphan")

# M:M через стикувальну flight_crew
class FlightCrew(db.Model):
    __tablename__ = "flight_crew"
    role = db.Column(db.Enum("Captain","First Officer","Flight Engineer"), primary_key=True)
    flight_id = db.Column(db.Integer, db.ForeignKey("flights.flight_id"), primary_key=True)
    pilot_id = db.Column(db.Integer, db.ForeignKey("pilots.pilot_id"), primary_key=True)

    flight = db.relationship("Flight", back_populates="crew")
    pilot = db.relationship("Pilot", back_populates="crew")

# Табл. flight_position (M:1 до flights)
class FlightPosition(db.Model):
    __tablename__ = "flight_position"
    position_id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.Date)
    latitude = db.Column(db.Numeric(9,6))
    longitude = db.Column(db.Numeric(9,6))
    altitude_m = db.Column(db.Integer)
    speed_kmh = db.Column(db.Integer)
    heading_deg = db.Column(db.Integer)
    flights_flight_id = db.Column(db.Integer, db.ForeignKey("flights.flight_id"), nullable=False)

    flight = db.relationship("Flight", back_populates="positions")
