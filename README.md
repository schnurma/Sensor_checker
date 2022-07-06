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
- als Liste dem User zur Verfügung stellen, erstmal im Terminal.
- Nach Auswahl und verifizierung, laden der vollständigen Lib des Sensors (im LibPackage Bundle sind nur *.mpy Files... )
- Ausgabe der Implemenation Notes mit Link zu Adafruit Sensor Seite
- Example Code in Nano öffnen
- User muss Pin Belegung Protokoll entsprechend Sensor anpassen testen
- Wenn auf IOT2050 funktioniert, Dockerfile wird mit angepassten Example Code erstellt.
- erstellt Docker Image
- startet Docker Image
- Öffnet Docker Container

