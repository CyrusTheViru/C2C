Einleitung
============


``BaseCar`` ist eine pythonbasierte Software mit der das Modellfahrzeug PiCar-S des Herstellers Sunfounder autonom fahrend betrieben werden kann.

Das Fahrzeug ist mit der gelieferten Software in der Lage selbstständig Fahrmanöver auszuführen, Hindernisse zu erkennen, sowie autonom Bahnen zu verfolgen. 



Motivation
**********

Die Herausforderung bei der Programmierung der Software ist zum Einen erste erlernte Schritte in der Pythonprogrammierung zu verstehen und anzuwenden, zum Anderen in einem agilen Team mit 5 Mitgliedern ein einheitliches Verständnis und gemeinsamen Style im programmierten Code zu erzeugen.
Dabei wurde die Software so aufgebaut, dass auch der Anwender durch Aufrufen der verschiedenen Fahrparcours 1-6 die
Entwicklungsschritte von einfachen Fahrbefehlen im Parcours 1 bis hin zum autonom fahrenden Fahrzeug im Parcours 6
nachvollziehen kann

Funktionen
**********
- Vorwärts- und Rückwärtsfahrt
- Lenkung rechts und links
- Hinderniserkennung mittels Ultraschallmodul
- Bahnverfolgung mittels Infrarotsensorik

Hardware
********
- RaspberryPi
- Modelauto : Bausatz Sunfounder PiCar‑S wird nach der beigelegten Anleitung aufgebaut und verdrahtet


Installation der Hardware Spezifischen Bibliotheken
***************************************************
- Console oeffnen
    - cd /home/pi/
    - git clone --recursive https://github.com/sunfounder/SunFounder_PiCar-S.git
    - cd ~/SunFounder_PiCar-S/
    - sudo ./install_dependencies
die Durchfuehrung zur Einstellungen für Lenkeinschlag und ähnlichen sind zum gegeben Punkt der Aufbauanleitung zu Entnehmen

Benötigte installierte Softwaremodule auf dem RaspberryPi:
**********************************************************
- Phyton 3 (Version: 3.7.3)

 erforderliche Pakete für Python3, auszuführen mit den Befehlen:
- pip3 install jupyter-dash
- pip install jupyter-dash
- pip install yupiterlab
- pip3 install --upgrade ipython
- pip3 install --upgrade numpy
- sudo apt-get install libatlas-base-dev
- pip3 install pandas


Voraussetzungen / Einstellungen zum Betrieb des PiCars auf dem RaspberryPi
**************************************************************************
 - Console oeffnen
    sudo raspi-config im Terminal starten, unter Advanced options den Punkt GL Driver aktivieren und dann neu starten
 - Wählen Sie im Menu des Raspberry Pi den Punkt “Einstellungen” und klicken auf den Reiter “Schnittstellen”. Aktivieren die Punkte “Kamera”, “SSH” und “I2C”.


Voraussetzungen zur Kommunikation mit dem RaspberryPi
*****************************************************
Es wird eine Remoteverbindung mit dem RaspberryPi vorausgesetzt.


Voraussetzungen zum Betrieb des PiCars
**************************************
- Softwaremodule BaseCar.py & basisklassen.py
- Akkubetrieb des Fahrzeugs

Betrieb der Software
********************
- Starten Sie die BaseCar.py

- Bei der Ertinbetriebnahme werden Sie dazu aufgefordert das Ultraschallmodul zu kalibrieren.

 1. Hierzu müssen Sie das Fahrzeug auf den Fahrbahnbelag stellen auf dem später gefahren werden soll. Bestätigen Sie die Anforderung mit Enter.
 2. Im Folgeschritt werden Sie dazu aufgefordert das Fahrzeug bzw. die Infrarotsensoren auf die zu verfolgende Linie (z.B. Klebeband) zu kalibrieren. Richten Sie die Sensorik auf die Linie aus und bestätigen Sie diesen Schrit mit         Enter.
 3. Die Software erzeugt nun die Datei Config.py und speichert die Kalibrierdaten in dieser Datei ab. Ist später ein Nachkalibrieren erforderlich werden die Daten in dieser Datei hinterlegt.

- Nun ist das Fahrzeug betriebsbereit und es erscheit folgendes Auswahlmenü.

 - 10 Fahrprofil
 - 20 Settings
 - 90 Exit

``10 Fahrprofil`` dient zu Auswahl des zu fahrenden Parcours:

- Im Fahrparcours 1 fährt das Fahrzeug vor, stopt, und fährt danach zurück (Betrieb / Test des Antriebs vor und zurück)
- Im Fahrparcours 2 fährt das Fahrzeug zunächst vorwärts, wechselt auf vollen Lenkeinschlag vorwärts im Uhrzeigersinn, stopt, und fährt danach mit vollem Lenkeinschlag im Uhrzeigersinn rückwärts (Betrieb mit Antrieb und Lenkung)
- Im Fahrparcours 3 fährt das Fahrzeug so lange geradeaus bis es auf ein Hindernis trifft und (Betrieb mit Ultraschallsensor) 
- Im Fahrparcours 4 fährt das Fahrzeug so lange geradeaus bis es auf ein Hindernis trifft und weicht dem Hindernis aus indem es zurück setzt und eine andere Bahn fährt (Betrieb mit Ultraschallsensor) 
- Im Fahrparcours 5 fährt das Fahrzeug autonom einer Linie folgen (Betrieb mit Infrarotsensorik)
- Im Fahrparcours 6 fährt das Fahrzeug autonom einer Linie folgend und stopt bei der Erkennung von Hindernissen mittels Ultraschallsensorik

``20 Settings`` enthält folgende Funktionen:

- 10 Formatchanger liest die Konfigurationsdateien der mitgelieferten SunFounder Software für die Antriebe und legt eine config.py Datei an sofern diese noch nicht existiert
- 20 Kalibrierung startet die Kalibrierungssequenz der Infrarotsensorik (untergrund und Linienkalibrierung)
- 30 Referenzierung setzen speichert die errechneten Referenzdaten in der config.py ab.

``90 Exit`` bricht die aktuell gewählte Operation ab

