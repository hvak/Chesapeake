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

#open the serial port
print('Opening Serial Port...')
try:
        s = serial.Serial(args.port, 115200)
        if (s.isOpen() == True):
                print(args.port + " has opened successfully.")
        else:
                print(args.port + " has failed to open.")
                exit()
except:
        print("An error has occurred opening " + args.port)
        exit()

#open the gcode file
print('Opening Gcode file...')
try:
        f = open(args.file, 'r')
        if (f.isOpen() == True):
                print(args.file + " has opened successfully.")
        else:
                print(args.file + " has failed to open.")
                exit()
except:
        print("An error has occurred opening " + args.file)
        exit()


print('')

#wake up printer and initialize
s.write("\n\n")
time.sleep(2)

s.flushInput()
print("Sending Gcode...")

for line in f:
        l = removeComment(line)
        l = l.strip()
        if (l.isspace() == False and len(l) > 0):
                print("Sending: " + l)
                s.write(l + "\n")
                grbl_out = s.readline() #wait for response from printer
                print(" : " + grbl_out.strip())

raw_input("Press any key to exit after printing has ended...")

#close the file and the serial port
f.close()
s.close()