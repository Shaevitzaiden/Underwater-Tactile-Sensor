#!/usr/bin/env python3

import time
import serial
import matplotlib.pyplot as plt
import numpy as np

from myVizTools import LiveHeatmap
from sensor import msgConfirmation


class SensorTestBench():
    def __init__(self):
        self.arduino = serial.Serial(port="COM3", baudrate=115200, timeout=0.1)
        ready = self.startup()
        if ready:
            print("Coms initiated successfully")
        else:    
            print("Failed to initiate coms, terminate and retry")
            while True:
                time.sleep(0.5)

        self.in_motion = False
        self.sensor_calibration = None

    def startup(self, delay=100, timeout=3):
        t1 = time.time()
        while True:
            if self.arduino.in_waiting > 0:
                inByte = int(self.arduino.read_until().decode())
                if inByte == 1:
                    print("startup successful")
                    return True
            elif (time.time()-t1) > timeout:
                return False
    
    def sendSerialMSG(self, msg, begin_delimiter="<", end_delimiter=">", timeout=100):
        """ Send msg by serial line, expects to recieve the same message back as confirmation"""
        t1 = time.time()
        msg_str = "{0}{1},{2},{3}{4}".format(begin_delimiter, msg[0], msg[1], msg[2], end_delimiter)
        msg_bytes = bytes(msg_str, 'utf-8')
        self.arduino.write(msg_bytes)
        
        # Wait for confirmation and try to resend message if not received
        confirmation = self.msgConfirmation(msg[0])
        while not confirmation and (time.time() - t1) < timeout:
            self.arduino.write(msg)
            confirmation = self.msgConfirmation(msg[0])
        return confirmation

    def msgConfirmation(self, msgToBeReceived, timeout=100):
        t1 = time.time()
        while (time.time() - t1) < timeout:
            if self.arduino.in_waiting > 0:
                msg = int(self.arduino.read_until().decode()[:-2])
                if msg == msgToBeReceived:
                    return True
        return False
    
    def movetoPos(self, pos):
        # Conversion factor using lead screw and number of steps
        # call moveToSteps
        pass

    def moveToStep(self, steps):
        # Send and confirm that command initiated
        start_motion = self.sendSerialMSG([2,steps[0],steps[1]])
        is_finished = False
        if start_motion:
            print("motion started")
            finished_motion = msgConfirmation(2)
            if finished_motion:
                print("motion finished")
                is_finished = True
            else:
                print("motion failed to finish")
        else:
            print("motion failed to start")
        return is_finished

    def getSensorData(self, timeout=1):
        ready = self.sendSerialMSG([1,0,0])
        if ready:
            reshapedData = np.zeros((4,2))
            t1 = time.time()
            while (time.time()-t1) < timeout:
                if self.arduino.in_waiting > 0:
                    inData = self.arduino.read_until().decode().split(",") 
                    if inData[0] == '':
                        return False, None
                    rawData = np.array([int(i) for i in inData], dtype=np.float64)
                    reshapedData[:,1] = rawData[0:4]
                    reshapedData[:,0] = np.flip(rawData[4:])
                    processedData = reshapedData/10*0.0145
                    if self.sensor_calibration is not None:
                        processedData -= self.sensor_calibration
                    return True, processedData
        return False, None 

    def getSensorCalibration(self):
        """ Get 1-point calibration """
        for i in range(10):
            msg_status, sens_data = self.getSensorData()
            if i == 0:
                calibration = sens_data
            else:
                calibration = (calibration + sens_data) / 2   
        self.sensor_calibration = calibration
        return calibration


if __name__ == "__main__":
    test_bench = SensorTestBench()
