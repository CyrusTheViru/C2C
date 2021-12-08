
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
