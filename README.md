# GPS_WDIC
WDIC Projekt GPS


## Ziel des Projektes
In unserem Projekt geht es darum, mit dem MN5010HS GPS Empfäner den Aktuellen Standort zu ermitteln und auf einer Karte, welche auf einem Webserver zu sehen ist, auszugeben. Es soll so wie bei einer Sporttracking App der gelaufene Pfad auf der Karte angezeigt werden.

## Arbeitsteilung
In unserem Projekt wurde zwischen Empfangen der GPS Daten und dem Dartstellen der Daten getrennt. Stefan übernimmt den Teil des Datenempfangens und Wendelin übernimmt die Darstellung.

## Darstellung
Da wir zwischen Datenempfang und Darstellung trennten, wurde erstmal eine Datei erstellt, in welcher NMEA-Daten eines Standorts sind (nmea_data.txt). Mithilfe von diesen Daten wurde im Programm gps_pin.py ein Programm erstellt, welches diesen Standort auf einer Karte auf einem Webserver Pinnt. 

Für die Karte wird die OpenStreetMap API genutzt und mithilfe von leaflet verwendet, Was man an folgendem Codeabschnitt erkennen kann:

~~~ html
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
~~~

Die Longitude und die Latitude sind daten, welche aus dem nmea_data.txt file gelesen werden. Diese werden in dieser Anwendung als Pin auf der Karte ausgegeben. Um Longitude und Latitude zu erhalten müssen die NMEA Ausgaben umgewandelt werden. Um dies zu machen wurde die pynema2 library verwendet. su kann mit folgenden Codzeilen die Längen- und Breitengrad ermittlet werden:

~~~ py
if line.startswith("$GPGGA") or line.startswith("$GNGGA"):
  msg = pynmea2.parse(line)
  latitude = msg.latitude
  longitude = msg.longitude
  return latitude, longitude
~~~

Es wird ein Flask-Server verwendet. Dieser kann mit folgenden Codzeilen gestartet werden:

~~~ py
if __name__ == "__main__":
    # Flask-Server starten
    app.run(host="0.0.0.0", port=5000, debug=True)
~~~



