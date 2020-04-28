import serial
import time
import argparse
import sys



def openSerialPort(port, baud):
        #open the serial port
        print('Opening Serial Port...')
        try:
                s = serial.Serial(port, baud)
                if (s.isOpen() == True):
                        print(port + " has opened successfully.")
                        return s
                else:
                        print(port + " has failed to open.")
                        exit()
        except:
                print("An error occurred while opening " + port)
                exit()

def openFile(file):
        #open the gcode file
        print('Opening Gcode file...')
        try:
                f = open(file, 'r')
                print(file + " has opened successfully.")
                return f
        except IOError:
                print("Could not open " + file)
                exit()
        except:
                print("An error occurred while trying to open " + file)
                exit()

#remove comments present in a gcode line
def removeComment(string):
        if (string.find(';') == -1):
                return string
        else:
                return string[:string.index(';')]

def sendGcode(serial, sequence):

        #wake up printer and initialize
        serial.write("\n\n".encode('utf-8'))
        time.sleep(2)

        serial.flushInput()
        for line in sequence:
                l = removeComment(line)
                l = l.strip()
                if (l.isspace() == False and len(l) > 0):
                        print("Sending: " + l)
                        serial.write((l + "\n").encode('utf-8'))
                        grbl_out = serial.readline() #wait for response from printer
                        print(" > " + grbl_out.strip().decode('utf-8'))



SHUTDOWN = [
        'M104 S0 ;extruder heater off',
        'G91 ;relative positioning',
        'G1 E-1 F300  ;retract the filament a bit before lifting the nozzle, to release some of the pressure',
        'G1 Z+0.5 E-5 X-20 Y-20 F9000 ;move Z up a bit and retract filament even more',
        'G28 X0 Y0 ;move X/Y to min endstops, so the head is out of the way',
        'G1 Y150 F5000 ;move completed part out',
        'M84 ;steppers off',
        'G90 ;absolute positioning',
]

if __name__ == '__main__':        

        parser = argparse.ArgumentParser(description='CHESAPEAKE v1.0 - Send gcode file to arduino over serial')
        parser.add_argument('-p', '--port', help='Arduino serial port')
        parser.add_argument('-f', '--file', help='Gcode file path')
        if len(sys.argv) == 1:
                parser.print_help()
                sys.exit(1)


        args = parser.parse_args()
        logo = open('chesapeake_logo.txt', 'r')
        for line in logo:
                print(line, end='')

        print('')
        print('USB Port: ' + args.port)
        print('Gcode File: ' + args.file)
        print('')

        ser = openSerialPort(args.port, 115200)
        gcode = openFile(args.file)
        

        print('')
        sendGcode(ser, gcode)
        sendGcode(ser, SHUTDOWN)

        #close the file and the serial port
        gcode.close()
        ser.close()

        print('\n The GCode has finished sending.')
