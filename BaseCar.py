from os import abort
import basisklassen as bk
import time
import numpy as np
import csv
import os.path
import datetime

### Hauptklasse
class BaseCar:
    """
    Diese Klasse ruft die Klassen und Methoden der Datei basisklassen.py aufund behinhaltet folgende Methoden :
    - set_steering_angle(int): Setzt Lenkwinkel
    - get_steering_angle(): Rückgabe des aktuellen Lenkwinkels
    - drive_forward(int): Vorwärtsfahren mit übergebener Geschwindigkeit
    - drive_backward(int): Rückwärtsfahren mit übergebener Geschwindigkeit
    - drive_stop(): Anhalten
    - get_speed(): Rückgabe der aktuellen Geschwindigkeit
    - get_direction(): Rückgabe der aktuellen Fahrtrichtung (1: vorwärts, 0: Stillstand, ‑1 Rückwärts)
    """
    
    def __init__(self):
        import config as conf
        self._turning_offset = conf.turning_offset
        self._forward_A = conf.forward_A
        self._forward_B = conf.forward_B
        self._direction = 0
        self._speed = 0
        self._steering_angle = 0
        self.drive_stop()
        self.set_steering_angle(90)
   
    def set_steering_angle(self, turn_angle = 0):
        fw = bk.Front_Wheels(turning_offset=self._turning_offset)
        self._steering_angle = fw.turn(turn_angle)
        time.sleep(.1)

    def get_steering_angle(self):
        return self._steering_angle
        
    def drive_forward(self, speed = 0):
        bw = bk.Back_Wheels(forward_A=self._forward_A, forward_B=self._forward_B)
        bw.speed = speed
        bw.forward()
        time.sleep(.1)
        self._direction = 1

    def drive_backward(self, speed = 0):
        bw = bk.Back_Wheels(forward_A=self._forward_A, forward_B=self._forward_B)
        bw.speed = speed
        bw.backward()
        time.sleep(.1)
        self._direction = -1

    def drive_stop(self):
        bw = bk.Back_Wheels(forward_A=self._forward_A, forward_B=self._forward_B)
        bw.stop()
        time.sleep(.1)
        self._direction = 0

    def get_speed(self):
        bw = bk.Back_Wheels(forward_A=self._forward_A, forward_B=self._forward_B)
        self._speed = bw.speed
        return self._speed

    def get_direction(self):
        return self._direction

### Unterklasse
class SensorCar(BaseCar):
    """
    Diese Klasse ist eine Unterklasse der Klasse BaseCar und erbt alle Methoden der Klasse BaseCar.
    Zusätzlich hat die Klasse die Methoden:
    - check_Obstacle: Mittels Ultraschallsensor Hindernisse erkennen und anzuhalten.
    - write_logfile: Zeitstempel, Geschwindigkeit, Fahrtrichtung, Lenkwinkel und Abstand Hindernis in CSV-Datei speichern
    - write_logfile_new_run:
    """
    def __init__(self, turning_offset, forward_A, forward_B):
        super().__init__(turning_offset, forward_A, forward_B)
        self._distance = 0
        
        if os.path.isfile("Log_SensorCar_USS.csv"):
            print("Das Log-File für den Ultraschallsensor existiert bereits!")
        else:
            writer = csv.writer(open("Log_SensorCar_USS.csv", "w", newline=''))
            writer.writerow(["Zeit", "Geschwindigkeit", "Fahrtrichtung", "Lenkwinkel", "Abstand Hindernis"])

    def set_steering_angle_sensor(self, turn_angle):
        super().set_steering_angle(turn_angle)
        self.write_logfile()

    def drive_forward_sensor(self, speed):
        super().drive_forward(speed)
        self.write_logfile()

    def drive_backward_sensor(self, speed):
        super().drive_backward(speed)
        self.write_logfile()

    def drive_stop_sensor(self):
        super().drive_stop()
        self.write_logfile()

    def check_obstacle(self, distance_limit = 0):

        while True:

            self.write_logfile()

            self.uss = bk.Ultrasonic(preparation_time=0.01, impuls_length=0.00001, timeout=0.05)
            self._distance = self.uss.distance()

            if self._distance < 0:
                print("Keine plausiblen Ultraschallwerte. Messung wird wiederholt.")
                continue
            elif self._distance >= 0 and self._distance <= distance_limit:
                print("Der Abstand zum Hindernis ist kleiner als " + str(distance_limit) + " cm. Das Auto wird angehalten.")
                super().drive_stop()
                self.write_logfile()
                self.uss.stop()
                break
            elif self._distance > distance_limit:
                continue

            time.sleep(.1)

    def get_distance_uss(self):
        return self._distance

    def write_logfile(self):

        timestamp = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]
        speed = self.get_speed()
        direction = self. get_direction()
        steering_angle = self.get_steering_angle()
        distance = self.get_distance_uss()

        writer = csv.writer(open("Log_SensorCar_USS.csv", "a", newline=''))
        writer.writerow([timestamp, speed, direction, steering_angle, distance])

    def write_logfile_new_run(self):
        timestamp = datetime.datetime.now().strftime("%d.%m.%Y")
        writer = csv.writer(open("Log_SensorCar_USS.csv", "a", newline=''))
        writer.writerow([timestamp, "###", "###", "###", "###"])  


def func_fahrparcour1():
    car = BaseCar()
    print("Das Auto fährt Fahrparcours 1.")

    print("Das Auto fährt 3 Sekunden vorwärts.")
    car.set_steering_angle(90)
    car.drive_forward(50)
    time.sleep(3)

    print("Das Auto wartet 1 Sekunde.")
    car.drive_stop()
    time.sleep(1)

    print("Das Auto fährt 3 Sekunden rückwärts.")
    car.set_steering_angle(90)
    car.drive_backward(50)
    time.sleep(3)

    print("Das Auto hat den Fahrparcours beendet.")
    car.drive_stop()

def func_fahrparcour2():
    car = BaseCar()
    print("Das Auto fährt Fahrparcours 2.")

    print("Das Auto fährt 1 Sekunden vorwärts.")
    car.set_steering_angle(90)
    car.drive_forward(50)
    time.sleep(1)

    print("Das Auto fährt 8 Sekunden mit vollem Lenkeinschlag im Uhrzeigersinn vorwärts.")
    car.set_steering_angle(135)
    car.drive_forward(50)
    time.sleep(8)

    print("Das Auto wartet 1 Sekunde.")
    car.drive_stop()
    car.set_steering_angle(90)
    time.sleep(1)

    print("Das Auto fährt 8 Sekunden mit vollem Lenkeinschlag im Uhrzeigersinn rückwärts.")
    car.set_steering_angle(135)
    car.drive_backward(50)
    time.sleep(8)

    print("Das Auto fährt 1 Sekunden rückwärts.")
    car.set_steering_angle(90)
    car.drive_backward(50)
    time.sleep(1)

    print("Das Auto hat den Fahrparcours beendet.")
    car.drive_stop()

def func_fahrparcour3():
    sensorCar = SensorCar() 
    sensorCar.write_logfile_new_run()
    print("Das Auto fährt Fahrparcours 3.")

    print("Das Auto fährt solange vorwärts bis es auf ein Hindernis trifft.")
    sensorCar.set_steering_angle_sensor(90)
    sensorCar.drive_forward_sensor(50)
    sensorCar.check_obstacle(10)

def func_fahrparcour4(anzahl_hindernisse :int):
    sensorCar = SensorCar()
    sensorCar.write_logfile_new_run()
    print("Das Auto fährt Fahrparcours 4.")

    for i in range(anzahl_hindernisse):

        print("Das Auto fährt solange vorwärts bis es auf ein Hindernis trifft.")
        sensorCar.set_steering_angle_sensor(90)
        sensorCar.drive_forward_sensor(50)
        sensorCar.check_obstacle(10)
    
        print("Hindernis ausweichen.")
        sensorCar.set_steering_angle_sensor(45)
        sensorCar.drive_backward_sensor(30)
        time.sleep(1.5)
        sensorCar.set_steering_angle_sensor(135)
        sensorCar.drive_forward_sensor(30)
        time.sleep(1.5)
        sensorCar.drive_stop_sensor()
        sensorCar.set_steering_angle_sensor(90)

def FormatChanger():
    """
        Diese Funktion liest die Config Datei aus dem Raspberry
        und legt mit dem angepassten Inhalt eine config.py an.
    """
    with open("/home/pi/SunFounder_PiCar/picar/config","r") as file:
        readline=file.read().splitlines()
        # Name der erstellt werden soll
        filename = "config.py"
        # Öfnnen des File mit Schreibrechten
        myfile = open(filename, 'w')
        # Schreibt die eingelesen Parameter
        myfile.write(readline[2])
        # Schreibt Leerzeile
        myfile.write('\n')
        myfile.write(readline[4])
        myfile.write('\n')
        myfile.write(readline[6])
        myfile.close()



"""import config as conf
CarSeting = conf.turning_offset
CarConfig ={ 
    "turning_offset" : conf.turning_offset,
    "forward_A"      : conf.forward_A,
    "forward_B"      : conf.forward_B
}
print(CarConfig)
""" 


doExit = False
while doExit==False:
    """Nutzerabfrage für den gewünschten Fahrparcour"""
    print("Übersicht der Funktionen: ")
    print("  10 Fahrprofil")
    print("  20 Settings")
    print("  90 Exit")
    TopMenu = int(input("Was wollen wir machen:"))
    if TopMenu == 10: #Fahrprofile
        while doExit==False:
            fahrparcour_num = int(input("Welcher Fahrparcour(1-4) soll gefahren werden. 90 = Exit: "))

            if fahrparcour_num == 1:
                func_fahrparcour1()
            elif fahrparcour_num == 2:
                func_fahrparcour2()
            elif fahrparcour_num == 3:
                func_fahrparcour3()
            elif fahrparcour_num == 4:
                Hindernisse = int(input("wieviele Hindernisse?: "))
                func_fahrparcour4(Hindernisse)
            elif fahrparcour_num == 90:
                doExit = True
            else:
                print("Ungueltiger Fahrparcour")
        doExit = False
    elif TopMenu == 20: #Settings
        FormatChanger()
    elif TopMenu == 90: #Exit
        doExit = True
    else:
        print("Ungueltige Eingabe")

