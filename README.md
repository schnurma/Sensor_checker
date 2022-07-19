#Sensor_checker#
Tool for checking Sensortype and decide which ROS2 Messagetype is needed.

# DEV NOTES TEMP #

"resources" ist der lokale Ordner für alle Daten die vom GitHub geladen werden oder erstellt werden.
sensor_info.txt wird beim einlesen der Lib Info erstellt.

Fürs testen:
libs "adafruit_*.py" vom Sensor direkt im Ordner
"lib" und "adafruit_bundle"
code_dump.txt und classes_objects.py



User should input Sensor ID to search in Adafruit Sensor Library
Searching in Lib for Sensor ID, downloads the file
Prints out Implementation Notes and Connection Type (I2C, SPI, etc...)
Develops Core for ROS2 and Dockercontainer with Comments what is needed to implement?
implement GUI?

ERROR HANDLING !!!???!!!


Meine Idee:

x Liste von der Adafruit GitHub Library erstellen,
x als Liste dem User zur Verfügung stellen, im Terminal.
x Nach Auswahl und Verifizierung, laden der vollständigen Lib des Sensors (im LibPackage Bundle sind nur *.mpy Files... )
nö Ausgabe der Implemenation Notes mit Link zu Adafruit Sensor Seite
x Example Code in Nano öffnen
-> User muss Pin Belegung Protokoll entsprechend Sensor anpassen testen
-> kann Example Code starten
x Wenn auf IOT2050 funktioniert, Dockerfile wird mit angepassten Example Code erstellt
x Docker Image Namen festlegen lassen, vorauswahl definieren.
x zwei Varianten ohne und mit ROS2 Funktion für besseres testen und einbinden

x erstellt Docker Image Strukturen (in Vorbereitung für ROS2)
x erstellt Dockerfile

- startet Docker Image
- Öffnet Docker Container


INFOS für README?

- Sensorname
- Datum
- Infos aus Lib?
- Funktionsweise
- Befehle Docker
- Befehle ROS2

INFOS für package.xml?
