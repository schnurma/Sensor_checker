# Sensor_checker
# Tool for checking Sensortype and decide which ROS2 Messagetype is needed.
#
# 

"resources" ist der lokale Ordner für alle Daten die vom GitHub geladen werden oder erstellt werden.
sensor_info.txt wird beim einlesen der Lib Info erstellt.

Fürs testen:
libs "adafruit_*.py" vom Sensor direkt im Ordner
"lib" und "adafruit_bundle"
code_dump.txt und classes_objects.py 


Meine Idee:

- Liste von der Adafruit GitHub Library erstellen,
- als Liste dem User zur Verfügung stellen, im Terminal.
- Nach Auswahl und Verifizierung, laden der vollständigen Lib des Sensors (im LibPackage Bundle sind nur *.mpy Files... )
- Ausgabe der Implemenation Notes mit Link zu Adafruit Sensor Seite
- Example Code in Nano öffnen
-> User muss Pin Belegung Protokoll entsprechend Sensor anpassen testen
-> kann Example Code starten
- Wenn auf IOT2050 funktioniert, Dockerfile wird mit angepassten Example Code erstellt
- Docker Image Namen festlegen lassen, vorauswahl definieren.
- erstellt Docker Image Strukturen (in Vorbereitung für ROS2)
- erstellt Dockerfile
- startet Docker Image
- Öffnet Docker Container


INFOS für README?

- Sensorname
- Datum
- Infos aus Lib?
- Funktionsweise
- Befehle Docker
- Befehle ROS2

