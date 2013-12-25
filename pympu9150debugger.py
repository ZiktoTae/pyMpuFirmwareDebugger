#!/usr/bin/python

import serial
import sys

class Mpu9150:
    def __init__(self):
        print "initializing 9150 class"

    def command(self, line):
        if line == "help":

            print "accel - print accel data"

        elif line == "accel":
            self.ToggleAccel()
        elif line =="":
            print "say something"
        else:
            print line+" : unkonwn command. type help"

    def ToggleAccel(self):
        print "toggle"
                
            

if __name__ == "__main__":
    command = ""
    mpu9150 = Mpu9150()
    while(command != "quit"):
        command = raw_input("mpu9150> ")
        mpu9150.command(command)
        
    
