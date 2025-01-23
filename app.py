from flask import Flask, render_template_string
import pynmea2

# Flask App
app = Flask(__name__)

# HTML Template für die Karte
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>GPS Position</title>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
</head>
<body>
    <div id="map" style="width: 100%; height: 600px;"></div>
    <script>
        var map = L.map('map').setView([{{ latitude }}, {{ longitude }}], 15);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 19
        }).addTo(map);
        L.marker([{{ latitude }}, {{ longitude }}]).addTo(map)
            .bindPopup("Aktuelle Position: {{ latitude }}, {{ longitude }}")
            .openPopup();
    </script>
</body>
</html>
"""

# Funktion zum Lesen und Verarbeiten der NMEA-Daten aus einer Datei
def get_position_from_file(file_path):
    with open(file_path, "r") as file:
        for line in file:
            try:
                # Nur GGA-NMEA-Sätze verwenden
                if line.startswith("$GPGGA") or line.startswith("$GNGGA"):
                    msg = pynmea2.parse(line)
                    latitude = msg.latitude
                    longitude = msg.longitude
                    return latitude, longitude
            except pynmea2.ParseError:
                continue
    return None, None

@app.route("/")
def index():
    # Datei mit den NMEA-Daten (Pfad anpassen)
    nmea_file_path = "nmea_data.txt"
    
    # GPS-Daten aus Datei extrahieren
    latitude, longitude = get_position_from_file(nmea_file_path)
    
    # Fallback, wenn keine gültigen Daten gefunden wurden
    if latitude is None or longitude is None:
        latitude, longitude = 0.0, 0.0

    # HTML mit den aktuellen Koordinaten rendern
    return render_template_string(HTML_TEMPLATE, latitude=latitude, longitude=longitude)

if __name__ == "__main__":
    # Flask-Server starten
    app.run(host="0.0.0.0", port=5000, debug=True)
