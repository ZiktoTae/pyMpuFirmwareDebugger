
#!/usr/bin/python
import sys
import serial
from serial.tools import list_ports
from mpudata import quat_packet, debug_packet, data_packet
import os
import time
import numpy as np
import matplotlib.pyplot as plt

class mpu9150interface(object):
    def __init__(self):
        #self.connect()
        #self.read()
        print "init"
        self.SIZE = 500
        self.x_list = [None]*self.SIZE
        self.y_list = [None]*self.SIZE
        self.z_list = [None]*self.SIZE
        self.mag_list = [None]*self.SIZE
        
        self.port="null"
        self.gravity = np.array([0,0,0])

    def connect(self):
        ports = list(self.serial_ports())
        for idx,val in enumerate(ports):
            print str(idx) + ". "+val

        num = raw_input("Select the port for the MPU-9150 : ")

        self.port = ports[int(num)]

        self.s = serial.Serial(self.port , 115200 , timeout=1)
        #self.ser.open()

        if self.s.isOpen():
            print "Connected..."
        else:
            self.s.open()
    
    def send(self, str):
        for i in range(0,len(str)):
            self.s.write(str[i])
            time.sleep(0.1)
                
    def write(self):
        command = ""
        while command != "q":
            command = raw_input("To Mpu>")
            self.send(command)

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

    def zeroing(self):
        self.index=0
        while (self.index <2 ):
            self.read_debug()
            #print self.index,
        self.gravity = np.array([ self.data[0],self.data[1] ,self.data[2] ])
        print self.gravity
                
    def read_debug(self):
        NUM_BYTES = 23
        p = None

        time.sleep(0.01)
        while self.s.inWaiting() >= NUM_BYTES:
            rs = self.s.read(NUM_BYTES)
            if ord(rs[0]) == ord('$'):
                pkt_code = ord(rs[1])
                #print "."
                print "\r"+str(pkt_code),
                if pkt_code == 1:
                    d = debug_packet(rs)
                    d.display()                
                elif pkt_code == 3:
                    d = data_packet(rs)
                    #d.display()
                    self.data = d.data
                    datatype = d.type

                    if datatype ==0:
                        self.index = self.index+1
                        #print self.index
                        self.x_list[self.index] = d.data[0]
                        self.y_list[self.index] = d.data[1]
                        self.z_list[self.index] = d.data[2]

                        vec = [d.data[0] , d.data[1], d.data[2]]
                        vec = vec - self.gravity
                        norm = np.linalg.norm(vec)
                        norm = norm-1
                        self.mag_list[self.index] = norm
                                                                    
                        if (self.index %2 == 1):
                            print "+",
                        else:
                            print "-",
                        
                    
                sys.stdout.flush()

    def read(self):
        self.index = 0
        print "logging..."
        n=0
        while( self.index < (self.SIZE-1)):
            self.read_debug()
            print self.index,
            sys.stdout.flush()

        self.s.close()
        print "plotting..."
        plt.plot(self.mag_list)
        plt.show()
        

if __name__ =="__main__":
    mpu =mpu9150interface()
    if (len(sys.argv) == 2):
        if sys.argv[1] == "setup":
            mpu.connect()
            mpu.write()
            mpu.s.close()
        else:
            mpu.s = serial.Serial(sys.argv[1],115200, timeout =1)
            print mpu.s
            if(mpu.s.isOpen()):
                print "connected..."
            #mpu.s = serial.Serial("/dev/cu.usbmodemfa141",115200, timeout =1)        
            #mpu.read()
            #raw_input("press enter to zeroing...")
            #mpu.zeroing()
            raw_input("press enter to start...")
            mpu.read()
