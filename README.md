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

Man kann folgendes Ergebniss auf dem Webserver sehen:
![grafik](https://github.com/user-attachments/assets/cf8bc4d3-df5a-4471-b4a4-2403d5cd6e30)

In der Date gps_tracker.py wurde versucht, immer der aktuelle Standort aus der Seriellen Schnittstelle auszulesen und als "Weg" auf der Karte auszugeben, was aber noch nicht funktioniert und noch ausgebaut wird.


## GPS-Empfänger

**Wichtig:** Das Modul kann aufgrund seiner Sensitivität nur unter **freiem Himmel** betrieben werden** 

Parameter:  
+ 5 V Versorgung
+ 36 mA Stromaufnahme
+ 1 Hz Refresh Rate
+ <3 m Genauigkeit
+ NMEA & SiRF Support

### Verwendung

Mit einer Terimalsoftware wie beispielsweise [HTerm](https://www.der-hammer.info/pages/terminal.html) können die rohen NMEA Sätze (im Default Mode) ausgelesen werden. Die Baudrate beträgt im Default Mode 4800 BPS. 

*Hinweis: Bis das Modul echte Daten empfängt kann es etwas dauern, bis zu 5 Minuten. Achte auf die Onboard-LED, diese blinkt wenn Daten empfangen werden.*

**Rohdaten:**
~~~
$GPGGA,084901.881,4716.1628,N,00938.0646,E,1,03,6.8,-48.0,M,48.0,M,,0000*46
$GPGSA,A,2,15,23,24,,,,,,,,,,6.9,6.8,1.0*30
$GPRMC,084901.881,A,4716.1628,N,00938.0646,E,0.18,264.02,160125,,,A*6E
$GPVTG,264.02,T,,M,0.18,N,0.3,K,N*0A
$GPGGA,084902.881,4716.1627,N,00938.0645,E,1,03,6.8,-48.0,M,48.0,M,,0000*49
$GPGSA,A,2,15,23,24,,,,,,,,,,6.9,6.8,1.0*30
$GPRMC,084902.881,A,4716.1627,N,00938.0645,E,0.17,278.45,160125,,,A*60
$GPVTG,278.45,T,,M,0.17,N,0.3,K,N*0B
$GPGGA,084903.881,4716.1627,N,00938.0644,E,1,03,6.8,-48.0,M,48.0,M,,0000*49
$GPGSA,A,2,15,23,24,,,,,,,,,,6.9,6.8,1.0*30
$GPRMC,084903.881,A,4716.1627,N,00938.0644,E,0.10,233.25,160125,,,A*6E
$GPVTG,233.25,T,,M,0.10,N,0.2,K,N*04
$GPGGA,084904.885,4716.1628,N,00938.0671,E,1,03,6.8,-48.0,M,48.0,M,,0000*43
$GPGSA,A,2,15,23,24,,,,,,,,,,6.9,6.8,1.0*30
$GPRMC,084904.885,A,4716.1628,N,00938.0671,E,0.26,18.10,160125,,,A*5C
$GPVTG,18.10,T,,M,0.26,N,0.5,K,N*3B
$GPGGA,084905.881,4716.1629,N,00938.0715,E,1,03,6.8,-48.0,M,48.0,M,,0000*44
$GPGSA,A,2,15,23,24,,,,,,,,,,6.9,6.8,1.0*30
$GPGSV,3,1,12,15,72,250,34,24,41,280,35,23,28,300,41,13,61,135,19*71
$GPGSV,3,2,12,14,40,055,16,28,36,211,,27,35,275,,30,33,225,*75
$GPGSV,3,3,12,05,31,056,23,09,30,277,,17,29,096,,19,20,129,*75
$GPRMC,084905.881,A,4716.1629,N,00938.0715,E,0.61,94.81,160125,,,A*54
$GPVTG,94.81,T,,M,0.61,N,1.1,K,N*31
$GPGGA,084906.881,4716.1626,N,00938.0635,E,1,03,6.8,-48.0,M,48.0,M,,0000*4B
$GPGSA,A,2,15,23,24,,,,,,,,,,6.9,6.8,1.0*30
$GPRMC,084906.881,A,4716.1626,N,00938.0635,E,0.49,87.02,160125,,,A*58
$GPVTG,87.02,T,,M,0.49,N,0.9,K,N*3B
~~~

## Requirements
Um unser Projekt auf dem Raspberry verwenden zu können müssen folgende Librarys auf dem Raspberry intstalliert werden:
- Flask
- Pynmea2
- serial
- flask-cors

