import serial
import time
import argparse

parser = argparse.ArgumentParser(description='CHESAPEAKE v1.0 - Send gcode file to arduino over serial')
parser.add_argument('-p', '--port', help='USB port of the Arduino')
parser.add_argument('-f', '--file', help='Gcode file path')
args = parser.parse_args()

#ascii word art font: slant
delay = 0.1
print("    __4___       ________  _____________ ___    ____  _________    __ __ ______     __4___")
time.sleep(delay)
print(" _  \ \ \ \     / ____/ / / / ____/ ___//   |  / __ \/ ____/   |  / //_// ____/  _  \ \ \ \\")
time.sleep(delay)
print("<'\ /_/_/_/    / /   / /_/ / __/  \__ \/ /| | / /_/ / __/ / /| | / ,<  / __/    <'\ /_/_/_/")
time.sleep(delay)
print(" ((____!___/) / /___/ __  / /___ ___/ / ___ |/ ____/ /___/ ___ |/ /| |/ /___     ((____!___/)")
time.sleep(delay)
print("  \\0\\0\\0\\0\/  \____/_/ /_/_____//____/_/  |_/_/   /_____/_/  |_/_/ |_/_____/      \\0\\0\\0\\0\/")
time.sleep(delay)
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
time.sleep(delay)
print("                CHESAPEAKE v1.0: A REPRAP 3D printer made from DVD drives")
time.sleep(delay)
print("                                Created by Hersh Vakharia\n")

print('USB Port: ' + args.port)
print('Gcode File: ' + args.file)
print('')

#remove comments present in a gcode line
def removeComment(string):
        if (string.find(';') == -1):
                return string
        else:
                return string[:string.index(';')]

def openSerialPort():
        #open the serial port
        print('Opening Serial Port...')
        try:
                s = serial.Serial(args.port, 115200)
                if (s.isOpen() == True):
                        print(args.port + " has opened successfully.")
                        return s
                else:
                        print(args.port + " has failed to open.")
                        exit()
        except:
                print("An error occurred while opening " + args.port)
                exit()

def openFile():
        #open the gcode file
        print('Opening Gcode file...')
        try:
                f = open(args.file, 'r')
                if (f.isOpen() == True):
                        print(args.file + " has opened successfully.")
                        return f
                else:
                        print(args.file + " has failed to open.")
                        exit()
        except:
                print("An error occurred while opening " + args.file)
                exit()

def sendGcode(serial, file):

        #wake up printer and initialize
        serial.write("\n\n")
        time.sleep(2)

        serial.flushInput()
        print("Sending Gcode...")

        for line in file:
                l = removeComment(line)
                l = l.strip()
                if (l.isspace() == False and len(l) > 0):
                        print("Sending: " + l)
                        serial.write(l + "\n")
                        grbl_out = serial.readline() #wait for response from printer
                        print(" : " + grbl_out.strip())

def sendShutdownSequence(serial, sequence):
        for line in sequence:
                l = removeComment(line)
                l = l.strip()
                if (l.isspace() == False and len(l) > 0):
                        print("Sending: " + l)
                        serial.write(l + "\n")
                        grbl_out = serial.readline() #wait for response from printer
                        print(" : " + grbl_out.strip())

shutdown = [
        'M104 S0 ;extruder heater off',
        'G91 ;relative positioning',
        'G1 E-1 F300  ;retract the filament a bit before lifting the nozzle, to release some of the pressure',
        'G1 Z+0.5 E-5 X-20 Y-20 F9000 ;move Z up a bit and retract filament even more',
        'G28 X0 Y0 ;move X/Y to min endstops, so the head is out of the way',
        'G1 Y150 F5000 ;move completed part out',
        'M84 ;steppers off',
        'G90 ;absolute positioning',
]


#----------------------------------------------------------------------

s = openSerialPort()
f = openFile()

print('')

sendGcode(s, f)
sendShutdownSequence(s, shutdown)

#close the file and the serial port
f.close()
s.close()

raw_input("Press any key to exit after printing has ended...")

