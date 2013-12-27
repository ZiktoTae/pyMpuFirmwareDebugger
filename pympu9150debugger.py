#!/usr/bin/python

import serial
from serial.tools import list_ports
import sys
import os


class Mpu9150:
    def __init__(self):
        print "initializing 9150 class"

    def command(self, line):
        if line == "help":
            print "accel - print accel data"
            print "connect - connect to module"
            print "sample - change thie sampling rate"
        elif line == "connect":
            self.connect()
        elif line == "sample":
            self.change_sampling_rate()
        elif line =="":
            print "say something"     
        elif line == "quit":
            print "quitting"
                
        else:
            print line+" : unkonwn command. type help"

    def ToggleAccel(self):
        print "toggle"

    def connect(self):
        ports = list(self.serial_ports())
        for idx,val in enumerate(ports):
            print str(idx) + ". "+val

        num = raw_input("Select the port for the MPU-9150 : ")

        self.port = ports[int(num)]

        self.ser = serial.Serial(self.port , 115200 , timeout=1)
        #self.ser.open()

        if self.ser.isOpen():
            print "Connected..."
        else:
            print "Port busy"

    def change_sampling_rate(self):
        print "changing sampling rates to : "
        print "1. 100,000"
        print "2. 50,000"
        print "3. 25,000"
        print "4. 20,000"
        print "5. 10,000"
        command = raw_input("Choose sampling rate(1-5) : ")

        self.ser.write("inv"+command)
        

    def serial_ports(self):
        """
        Returns a generator for all available serial ports
        """
        if os.name == 'nt':
            # windows
            for i in range(256):
                try:
                    s = serial.Serial(i)
                    s.close()
                    yield 'COM' + str(i + 1)
                except serial.SerialException:
                    pass
        else:
            # unix
            for port in list_ports.comports():
                yield port[0]

if __name__ == "__main__":
    command = ""
    mpu9150 = Mpu9150()
    while(command != "quit"):
        command = raw_input("mpu9150> ")
        mpu9150.command(command)
        
    
