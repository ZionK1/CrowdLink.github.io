from chalice import Chalice, BadRequestError, Response, CORSConfig
from datetime import datetime, timezone

app = Chalice(app_name='crowd-link')

# Create a CORS configuration object
cors_config = CORSConfig(
    allow_origin='*'
)

# In-memory store for GPS data keyed by busId.
latest_gps_data = {}

@app.route('/api/gps', methods=['POST'], cors=cors_config)
def receive_gps():
    request = app.current_request
    data = request.json_body

    if not data or 'busId' not in data or 'lat' not in data or 'lng' not in data:
        raise BadRequestError("Missing required fields: busId, lat, lng")
    
    bus_id = data.pop('busId')
    data.setdefault('timestamp', datetime.now(timezone.utc).isoformat())
    latest_gps_data[bus_id] = data

    return {"message": "GPS data received"}

@app.route('/api/gps', methods=['GET'], cors=cors_config)
def get_gps():
    if not latest_gps_data:
        return {"error": "No GPS data available"}
    return latest_gps_data
