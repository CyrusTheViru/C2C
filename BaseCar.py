# coding=utf-8
""" Autonomens Fahren mit Sunfounder PiCar-S """


from os import abort
import basisklassen as bk
import time
import numpy as np
import csv
import os.path
import datetime
import webbrowser

### Hauptklasse
class BaseCar:
    """
     Diese Klasse ruft die Klassen und Methoden der Datei basisklassen.py auf. Zusätzlich wird im init der Antrieb abgeschaltet und die Lenkung auf die Nullposition gefahren.

    :param turning_offset: setzt den Lenkwinkeloffset in der _INIT_
    :type turning_offset: Integer
    :param forward_A: setzt die Drehrichtung Fahrzeugspezifisch für das erste Rad. Die Umschaltung laeuft mit dem Wechsel 0 zu 1.
    :type forward_A: Integer
    :param forward_B: setzt die Drehrichtung Fahrzeugspezifisch für das erste Rad. Die Umschaltung laeuft mit dem Wechsel 0 zu 1.
    :type forward_B: Integer

    """
    
    def __init__(self, turning_offset, forward_A, forward_B):
        import config as conf
        self._turning_offset = turning_offset
        self._forward_A = forward_A
        self._forward_B = forward_B
        self._direction = 0
        self._speed = 0
        self._steering_angle = 0
        self._fw = bk.Front_Wheels(turning_offset=self._turning_offset)
        self._bw = bk.Back_Wheels(forward_A=self._forward_A, forward_B=self._forward_B)
        self.drive_stop()
        self.set_steering_angle(90)
   
    def set_steering_angle(self, turn_angle = 0):
        """Setzt den Lenkwinkel

        :param turn_angle: setzen von dem Ziellenkwinkel defaults to 0
        :type turn_angle: int, optional
        """
        self._steering_angle = self._fw.turn(turn_angle)
        time.sleep(.1)

    def get_steering_angle(self):
        """Rückgabe des aktuellen Lenkwinkels

        :return: Lenkwinkel in 0.5 Grad
        :rtype: int
        """
        return self._steering_angle
        
    def drive_forward(self, speed = 0):
        """Vorwärtsfahren mit übergebener Geschwindigkeit

        :param speed: Zielgeschwindigkeit, defaults to 0
        :type speed: int, optional
        """
        self._bw.speed = speed
        self._bw.forward()
        time.sleep(.1)
        self._speed = self._bw.speed
        if self._speed == 0:
            self._direction = 0
        else:
            self._direction = 1

    def drive_backward(self, speed = 0):
        """Rückwärtsfahren mit übergebener Geschwindigkeit

        :param speed: [Zielgeschwindigkeit], defaults to 0
        :type speed: int, optional
        """
        self._bw.speed = speed
        self._bw.backward()
        time.sleep(.1)
        self._speed = self._bw.speed
        if self._speed == 0:
            self._direction = 0
        else:
            self._direction = -1

    def drive_stop(self):
        """Stoppt die Fahrt
        """
        self._bw.stop()
        time.sleep(.1)
        self._speed = 0
        self._direction = 0

    def get_speed(self):
        """Rückgabe der aktuellen Geschwindigkeit

        :return: aktuelle Geschwindikeit
        :rtype: int
        """
        return self._speed

    def get_direction(self):
        """Rückgabe der aktuellen Fahrtrichtung (1: vorwärts, 0: Stillstand, -1 Rückwärts)

        :return: Fahrtrichtung  
        :rtype: int
        """
        return self._direction

### Unterklasse
class SensorCar(BaseCar):
    """
     Diese Klasse ist eine Unterklasse der Klasse BaseCar und erbt alle Methoden der Klasse BaseCar.
    :param turning_offset: setzt den Linkwinkeloffset in der _INIT_
    :type turning_offset: Integer
    :param forward_A: setzt die Drehrichtung Fahrzeigspezifisch für das erste Rad. Die umschaltung laeuft mit dem wechsel 0 zu 1.
    :type forward_A: Integer
    :param forward_B: setzt die Drehrichtung Fahrzeigspezifisch für das erste Rad. Die umschaltung laeuft mit dem wechsel 0 zu 1.
    :type forward_B: Integer
    """
    def __init__(self, turning_offset, forward_A, forward_B):
        super().__init__(turning_offset, forward_A, forward_B)
        self._distance = 0
        import config as conf
        self._ir = bk.Infrared(references = conf.ir_references)
        
        if os.path.isfile("Log_SensorCar_USS_IR.csv") == True:
            print("Das Log-File für den Ultraschallsensor existiert bereits!")
        else:
            writer = csv.writer(open("Log_SensorCar_USS_IR.csv", "w", newline=''))
            writer.writerow(["Zeit", "Geschwindigkeit", "Fahrtrichtung", "Lenkwinkel", "Abstand_Hindernis", "Infrarot_Analogdaten", "Infrarot_Digitalwerte"])

    def set_steering_angle_sensor(self, turn_angle):
        """Funktion von der Class BaseCar, Setzt den Lenkwinkel und logt den zusätzlich

        :param turn_angle: setzen von dem Ziellenkwinkel defaults to 0
        :type turn_angle: int, optional
        """
        super().set_steering_angle(turn_angle)
        self.write_logfile()

    def drive_forward_sensor(self, speed):
        """Funktion von der Class BaseCar, Vorwärtsfahren mit übergebener Geschwindigkeit und logt dies

        :param speed: Zielgeschwindigkeit, defaults to 0
        :type speed: int, optional
        """
        super().drive_forward(speed)
        self.write_logfile()

    def drive_backward_sensor(self, speed):
        """Funktion von der Class BaseCar, Rückwärtsfahren mit übergebener Geschwindigkeit und logt dies

        :param speed: [Zielgeschwindigkeit], defaults to 0
        :type speed: int, optional
        """
        super().drive_backward(speed)
        self.write_logfile()

    def drive_stop_sensor(self):
        """Funktion von der Class BaseCar, Stoppt die Fahrt und logt dies
        """
        super().drive_stop()
        self.write_logfile()

    def check_obstacle(self, distance_limit = 0):
        """Mittels Ultraschallsensor Hindernisse erkennen und anzuhalten.

        :param distance_limit: setzt die Distance zum anhalten, defaults to 0
        :type distance_limit: int, optional
        """

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
        """Liest den aktuellen Abstand zum Hinderniss aus und liefert diesen zurück.

        :return: Distance zum Hinderniss
        :rtype: int
        """
        self.uss = bk.Ultrasonic(preparation_time=0.01, impuls_length=0.00001, timeout=0.05)
        self._distance = self.uss.distance()
        return self._distance

    def get_ir_analog(self):
        """Erfassung analoger Daten vom Infrarotsensor

        :return: Analoge Werte von dem Infrarotsensoren
        :rtype: Liste von 5 int
        """
        self._irAnalog = self._ir.read_analog()
        return self._irAnalog

    def get_ir_digital(self):
        """Erfassung digitaler Daten vom Infrarotsensor

        :return: Digitale Werte von dem Infrarotsensoren
        :rtype: Liste von 5 int
        """
        self._irDigital = self._ir.read_digital()
        return self._irDigital

    def write_logfile(self):
        """
        Speichert die Werte für Zeitstempel, Geschwindigkeit, Fahrtrichtung, Lenkwinkel, Abstand Hindernis, 
        Analoge und Digitale Werte von den Intrarotsensoren in eine CSV-Datei
        """
        timestamp = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]
        speed = self.get_speed()
        direction = self. get_direction()
        steering_angle = self.get_steering_angle()
        distance = self.get_distance_uss()
        #ir_data = self.get_ir_analog()
        ir_data = np.array(self.get_ir_analog())
        ir_digital = self.get_ir_digital()

        writer = csv.writer(open("Log_SensorCar_USS_IR.csv", "a", newline=''))
        writer.writerow([timestamp, speed, direction, steering_angle, distance, ir_data, ir_digital])

    def write_logfile_new_run(self):
        """ Schreibt das aktuelle Datum in die Logdatei.
        """
        timestamp = datetime.datetime.now().strftime("%d.%m.%Y")
        writer = csv.writer(open("Log_SensorCar_USS_IR.csv", "a", newline=''))
        writer.writerow([timestamp, "###", "###", "###", "###", "###"]) 

""" Fahrtrecken 1 - 6 """

def func_fahrparcour1():
    """ 1. Das Auto fährt 3 Sekunden vorwärts 2. Das Auto wartet 1 Sekunde 3. Das Auto fährt 3 Sekunden rückwärts """
    import config as conf
    car = BaseCar(conf.turning_offset, conf.forward_A, conf.forward_B)
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
    """ 1. Das Auto fährt 1 Sekunden vorwärts 2. Das Auto fährt 8 Sekunden mit vollem Lenkeinschlag im Uhrzeigersinn vorwärts 3. Das Auto wartet 1 Sekunde
    4. Das Auto fährt 8 Sekunden mit vollem Lenkeinschlag im Uhrzeigersinn rückwärts 5. Das Auto fährt 1 Sekunden rückwärts """
    import config as conf
    car = BaseCar(conf.turning_offset, conf.forward_A, conf.forward_B)
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
    """ 1. Das Auto fährt solange vorwärts bis es auf ein Hindernis trifft """
    import config as conf
    sensorCar = SensorCar(conf.turning_offset, conf.forward_A, conf.forward_B)
    
    #sensorCar.write_logfile_new_run()
    print("Das Auto fährt Fahrparcours 3.")

    print("Das Auto fährt solange vorwärts bis es auf ein Hindernis trifft.")
    sensorCar.set_steering_angle_sensor(90)
    sensorCar.drive_forward_sensor(30)
    sensorCar.check_obstacle(10)

def func_fahrparcour4(anzahl_hindernisse = 3):
    """  
     1. Das Auto fährt solange vorwärts bis es auf ein Hindernis trifft 2. Das Auto weicht ingesammt 3 x einem Hindernis aus 
    :param anzahl_hindernisse: Anzahl der zu erkennenden Hindernisse im Parcour. Nach dieser Anzahl wird die Fahrt gestoppt.
    :type anzahl_hindernisse: int
    """
    import config as conf
    sensorCar = SensorCar(conf.turning_offset, conf.forward_A, conf.forward_B)

    #sensorCar.write_logfile_new_run()
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


def func_fahrparcour5():
    """ 1. Das Auto fährt der markierten Linie entlang 2. Das Auto stoppt wenn die markierte Linie endet """
    import config as conf
    sensorCar = SensorCar(conf.turning_offset, conf.forward_A, conf.forward_B)
    print("Das Auto fährt Fahrparcours 5.")
    print("Das Auto fährt an der Linie entlang")
    sensorCar.set_steering_angle_sensor(90)
    sensorCar.drive_forward_sensor(30)
    #sensorCar.check_obstacle(10)
    #sensorCar.write_logfile_new_run()
    
    while(sum(sensorCar.get_ir_digital())!=0):
        if sensorCar.get_ir_digital() == ([0, 0, 1, 0, 0]):
            sensorCar.set_steering_angle_sensor(90)
        elif sensorCar.get_ir_digital() == ([0, 0, 1, 1, 0]):
            sensorCar.set_steering_angle_sensor(100)
        elif sensorCar.get_ir_digital() == ([0, 0, 0, 1, 0]):
            sensorCar.set_steering_angle_sensor(110)
        elif sensorCar.get_ir_digital() == ([0, 0, 0, 1, 1]):
            sensorCar.set_steering_angle_sensor(120)
        elif sensorCar.get_ir_digital() == ([0, 0, 0, 0, 1]):
            sensorCar.set_steering_angle_sensor(130)
        elif sensorCar.get_ir_digital() == ([0, 1, 1, 0, 0]):
            sensorCar.set_steering_angle_sensor(80)
        elif sensorCar.get_ir_digital() == ([0, 1, 0, 0, 0]):
            sensorCar.set_steering_angle_sensor(70)
        elif sensorCar.get_ir_digital() == ([1, 1, 0, 0, 0]):
            sensorCar.set_steering_angle_sensor(60)
        elif sensorCar.get_ir_digital() == ([1, 0, 0, 0, 0]):
            sensorCar.set_steering_angle_sensor(50)
        else: break
        time.sleep(0.1)
    sensorCar.drive_stop_sensor()


def func_fahrparcour6():
    """ 1. Das Auto fährt einer markierten Linie entlang 2. Das Auto stoppt wenn die markierte Linie endet oder auf ein Hindernis trifft """
    import config as conf
    sensorCar = SensorCar(conf.turning_offset, conf.forward_A, conf.forward_B)
    print("Das Auto fährt Fahrparcours 6.")
    print("Das Auto fährt an der Linie entlang")
    sensorCar.set_steering_angle_sensor(90)
    sensorCar.drive_forward_sensor(30)
    #sensorCar.check_obstacle(10)
    #sensorCar.write_logfile_new_run()
    
    while(sum(sensorCar.get_ir_digital())!=0):
        print(sensorCar.get_distance_uss())
        if sensorCar.get_distance_uss() <= 0:
            print("Keine plausiblen Ultraschallwerte. Messung wird wiederholt.")
            continue
        elif sensorCar.get_distance_uss() >= 20:
            if sensorCar.get_ir_digital() == ([0, 0, 1, 0, 0]):
                sensorCar.set_steering_angle_sensor(90)
            elif sensorCar.get_ir_digital() == ([0, 0, 1, 1, 0]):
                sensorCar.set_steering_angle_sensor(100)
            elif sensorCar.get_ir_digital() == ([0, 0, 0, 1, 0]):
                sensorCar.set_steering_angle_sensor(110)
            elif sensorCar.get_ir_digital() == ([0, 0, 0, 1, 1]):
                sensorCar.set_steering_angle_sensor(120)
            elif sensorCar.get_ir_digital() == ([0, 0, 0, 0, 1]):
                sensorCar.set_steering_angle_sensor(130)
            elif sensorCar.get_ir_digital() == ([0, 1, 1, 0, 0]):
                sensorCar.set_steering_angle_sensor(80)
            elif sensorCar.get_ir_digital() == ([0, 1, 0, 0, 0]):
                sensorCar.set_steering_angle_sensor(70)
            elif sensorCar.get_ir_digital() == ([1, 1, 0, 0, 0]):
                sensorCar.set_steering_angle_sensor(60)
            elif sensorCar.get_ir_digital() == ([1, 0, 0, 0, 0]):
                sensorCar.set_steering_angle_sensor(50)
            else: break
            time.sleep(0.1)
        else: break
    sensorCar.drive_stop_sensor()

def setIRCalibration():
    """ Initialle Kalibrierung der Infrarot Sensoren """
    #Initialle Kalibrierung der Infrarot Sensoren
    ir = bk.Infrared()
    ir.cali_references()
    filename = "config.py"
    # Öfnnen des File mit Schreibrechten
    myfile = open(filename, 'a')
    # Schreibt Leerzeile
    myfile.write('\n')
    # Schreibt die eingelesen Parameter
    myfile.write("ir_references = " + str(list(ir._references)))
    print(" Die Referenzwerte für den IR-Sensor wurden erfolgreich in die Config geschrieben.")
    
def setIRCalibrationNew():
    """ Neue Kalibrierung der Infrarot Sensoren zur Laufzeit """
    #Neue Kalibrierung der Infrarot Sensoren zur Laufzeit
    ir = bk.Infrared()
    ir.cali_references()
    import config as conf
    conf.ir_references = list(ir._references)


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
    print("/home/pi/SunFounder_PiCar/picar/config wurde erfolgreich eingelesen.")

if os.path.isfile("config.py") == True:
    print("Das Config-File wurde bereits importiert.")
else:
    FormatChanger()
    setIRCalibration()

doExit = False
while doExit==False:
    """Nutzerabfrage für den gewünschten Fahrparcour"""
    print("Übersicht der Funktionen: ")
    print("   10 Fahrprofil")
    print("   20 Settings")
    print("   90 Exit")
    print("  100 Hilfe")
    TopMenu = int(input("Was wollen wir machen:"))
    if TopMenu == 10: #Fahrprofile
        while doExit==False:
            fahrparcour_num = int(input("Welcher Fahrparcour(1-6) soll gefahren werden. 90 = Exit: "))

            if fahrparcour_num == 1:
                func_fahrparcour1()
            elif fahrparcour_num == 2:
                func_fahrparcour2()
            elif fahrparcour_num == 3:
                func_fahrparcour3()
            elif fahrparcour_num == 4:
                Hindernisse = int(input("wieviele Hindernisse?: "))
                func_fahrparcour4(Hindernisse)
            elif fahrparcour_num == 5:
                func_fahrparcour5()
            elif fahrparcour_num == 6:
                func_fahrparcour6()
            elif fahrparcour_num == 90:
                doExit = True
            else:
                print("Ungueltiger Fahrparcour")
        doExit = False
    elif TopMenu == 20: #Settings
        while doExit==False:
            SetID = int(input("Welche einstellungen sollen durchgeführt werden: 10 = formatchanger; 20 = Kalibrierung IR; 90 = Exit"))
            if SetID == 10: 
                FormatChanger()
            elif SetID == 20:
                setIRCalibrationNew()
            elif SetID == 90:
                doExit = True
            else:
                print("keine Einstellung verfügbar")
        doExit = False
    elif TopMenu == 90: #Exit
        doExit = True
    elif TopMenu == 100: #Hilfe
        localDir = os.path.dirname(os.path.realpath(__file__))
        webbrowser.open(localDir + "/html/BaseCar.py.html")
    else:
        print("Ungueltige Eingabe")