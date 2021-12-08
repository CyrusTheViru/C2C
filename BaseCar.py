import basisklassen as bk
import time
import numpy as np

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
    
    def __init__(self, turning_offset, forward_A, forward_B):
        self.TURNING_OFFSET = turning_offset
        self.FORWARD_A = forward_A
        self.FORWARD_B = forward_B
        self.fw = bk.Front_Wheels(turning_offset=self.TURNING_OFFSET)
        self.bw = bk.Back_Wheels(forward_A=self.FORWARD_A, forward_B=self.FORWARD_B)
        self.DIRECTION = 0
        self.drive_stop()
        self.set_steering_angle(90)
   
    def set_steering_angle(self, turn_angle = 0):
        self.fw.turn(turn_angle)

    def get_steering_angle(self):
        self.fw.get_angles()

    def drive_forward(self, speed = 0):
        self.bw.speed = speed
        self.bw.forward()
        self.DIRECTION = 1

    def drive_backward(self, speed = 0):
        self.bw.speed = speed
        self.bw.backward()
        self.DIRECTION = -1

    def drive_stop(self):
        self.bw.stop()
        self.DIRECTION = 0

    def get_speed(self):
        speed = self.bw.speed
        return speed

    def get_direction(self):
        return self.DIRECTION

### Unterklasse
class SensorCar(BaseCar):
    """
    Diese Klasse ist eine Unterklasse der Klasse BaseCar und erbt alle Methoden der Klasse BaseCar.
    Zusätzlich hat die Klasse die Methode:
    - check_Obstacle um mittels Ultraschallsensor Hindernisse zu erkennen und anzuhalten.
    """
    def __init__(self, turning_offset, forward_A, forward_B):
        super().__init__(turning_offset, forward_A, forward_B)
        self.uss = bk.Ultrasonic(preparation_time=0.01, impuls_length=0.00001, timeout=0.05)
        self.uss.stop()

    def check_obstacle(self):
        while True:
            
            distance = self.uss.distance()

            if distance < 0:
                print("Keine plausiblen Ultraschallwerte. Messung wird wiederholt.")
                continue
            elif distance >= 0 and distance <= 5:
                print("Der Abstand zum Hindernis ist kleiner als 5 cm. Das Auto wird angehalten.")
                super().drive_stop()
                break
            elif distance > 5:
                continue

            time.sleep(.1)
                 

car = BaseCar(30,1,1)
sensorCar = SensorCar(30,1,1)    

fahrparcours = 3

if fahrparcours == 1:

    print("Das Auto fährt Fahrparcours 1.")

    print("Das Auto fährt 3 Sekunden vorwärts.")
    car.set_steering_angle(90)
    time.sleep(.1)
    car.drive_forward(50)
    time.sleep(3)

    print("Das Auto wartet 1 Sekunde.")
    car.drive_stop()
    time.sleep(1)

    print("Das Auto fährt 3 Sekunden rückwärts.")
    car.set_steering_angle(90)
    time.sleep(.1)
    car.drive_backward(50)
    time.sleep(3)

    print("Das Auto hat den Fahrparcours beendet.")
    car.drive_stop()

elif fahrparcours == 2:

    print("Das Auto fährt Fahrparcours 2.")

    print("Das Auto fährt 1 Sekunden vorwärts.")
    car.set_steering_angle(90)
    time.sleep(.1)
    car.drive_forward(50)
    time.sleep(1)

    print("Das Auto fährt 8 Sekunden mit vollem Lenkeinschlag im Uhrzeigersinn vorwärts.")
    car.set_steering_angle(135)
    time.sleep(8)

    print("Das Auto wartet 1 Sekunde.")
    car.drive_stop()
    time.sleep(.1)
    car.set_steering_angle(90)
    time.sleep(1)

    print("Das Auto fährt 8 Sekunden mit vollem Lenkeinschlag im Uhrzeigersinn rückwärts.")
    car.set_steering_angle(135)
    time.sleep(.1)
    car.drive_backward(50)
    time.sleep(8)

    print("Das Auto fährt 1 Sekunden rückwärts.")
    car.set_steering_angle(90)
    time.sleep(.1)
    car.drive_backward(50)
    time.sleep(1)

    print("Das Auto hat den Fahrparcours beendet.")
    car.drive_stop()

elif fahrparcours == 3:
    print("Das Auto fährt Fahrparcours 3.")

    print("Das Auto fährt solange vorwärts bis es auf ein Hindernis trifft.")
    sensorCar.set_steering_angle(90)
    time.sleep(.1)
    sensorCar.drive_forward(50)
    sensorCar.check_obstacle()

else:
    print("Kein gültiger Fahrparcours ausgewählt!")
