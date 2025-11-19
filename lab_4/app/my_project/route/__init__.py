from ..controller.airline_controller import bp as airlines_bp
from ..controller.pilot_controller import bp as pilots_bp
from ..controller.flight_controller import bp as flights_bp
from ..controller.crew_controller import bp as crew_bp

def register_blueprints(app):
    app.register_blueprint(airlines_bp)
    app.register_blueprint(pilots_bp)
    app.register_blueprint(flights_bp)
    app.register_blueprint(crew_bp)
