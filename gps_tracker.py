from flask import Flask, render_template_string, jsonify
import serial
import pynmea2
import threading

# Flask App
app = Flask(__name__)

# HTML Template für dynamische Weganzeige
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>GPS Weganzeige</title>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/axios/1.3.4/axios.min.js"></script>
</head>
<body>
    <div id="map" style="width: 100%; height: 600px;"></div>
    <script>
        var map = L.map('map').setView([0, 0], 15); // Startansicht der Karte
        var marker = L.marker([0, 0]).addTo(map);   // Marker für die aktuelle Position
        var path = L.polyline([], {color: 'blue'}).addTo(map); // Linie für den zurückgelegten Weg
        
        async function updatePosition() {
            try {
                const response = await axios.get('/position');
                const data = response.data;
                if (data.latitude !== null && data.longitude !== null) {
                    // Karte, Marker und Linie aktualisieren
                    map.setView([data.latitude, data.longitude], 15);
                    marker.setLatLng([data.latitude, data.longitude]);
                    path.addLatLng([data.latitude, data.longitude]);
                }
            } catch (error) {
                console.error("Fehler beim Abrufen der Position:", error);
            }
        }
        
        // Alle 2 Sekunden Position aktualisieren
        setInterval(updatePosition, 2000);
    </script>
</body>
</html>
"""

# Globale Variablen für Position und Weg
position_data = {"latitude": None, "longitude": None}
path_data = []

# Funktion, um die aktuelle Position über die serielle Schnittstelle zu lesen
def read_serial_data(serial_port):
    global position_data, path_data
    with serial.Serial(serial_port, baudrate=4800, timeout=1) as ser:
        while True:
            try:
                line = ser.readline().decode('ascii', errors='ignore').strip()
                if line.startswith("$GPGGA") or line.startswith("$GNGGA"):
                    msg = pynmea2.parse(line)
                    latitude = msg.latitude
                    longitude = msg.longitude
                    if latitude and longitude:
                        # Position aktualisieren
                        position_data["latitude"] = latitude
                        position_data["longitude"] = longitude
                        # Zum Weg hinzufügen
                        path_data.append((latitude, longitude))
            except (pynmea2.ParseError, UnicodeDecodeError):
                continue

@app.route("/")
def index():
    # HTML-Seite zurückgeben
    return render_template_string(HTML_TEMPLATE)

@app.route("/position")
def get_position():
    # Aktuelle Position als JSON zurückgeben
    return jsonify(position_data)

if __name__ == "__main__":
    # Serielle Schnittstelle und Thread starten
    serial_port = "/dev/ttyS0"  # Anpassen an die korrekte serielle Schnittstelle
    serial_thread = threading.Thread(target=read_serial_data, args=(serial_port,), daemon=True)
    serial_thread.start()
    
    # Flask-Server starten
    app.run(host="0.0.0.0", port=5000, debug=True)
