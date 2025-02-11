from chalice import Chalice, BadRequestError
from datetime import datetime, timezone

app = Chalice(app_name='crowd-link')

# In-memory storage for the latest GPS data.
# In production, you might replace this with a persistent datastore.
latest_gps_data = {}

@app.route('/api/gps', methods=['POST'])
def receive_gps():
    request = app.current_request
    data = request.json_body

    # Validate the incoming JSON data.
    if not data or 'lat' not in data or 'lng' not in data:
        raise BadRequestError("Missing required fields: lat, lng")

    # Add a timestamp if not provided.
    data.setdefault('timestamp', datetime.now(timezone.utc).isoformat())


    # Update the in-memory store with the new GPS data.
    latest_gps_data.update(data)

    return {"message": "GPS data received"}

@app.route('/api/gps', methods=['GET'])
def get_gps():
    if not latest_gps_data:
        return {"error": "No GPS data available"}
    return latest_gps_data
