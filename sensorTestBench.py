#!/usr/bin/env python3

import time
from tracemalloc import start
import serial
import matplotlib.pyplot as plt
import numpy as np
import sys

from myVizTools import LiveHeatmap


class SensorTestBench():
    def __init__(self):
        self.arduino = serial.Serial(port="COM4", baudrate=115200, timeout=0.5) # Don't forget to check port, can maybe automate finding the port
        ready = self.startup()
        if not ready:    
            print("Failed to initiate coms, retry")
            sys.exit()

        self.in_motion = False
        self.sensor_calibration = None
        self.stored_data = None
        self.sensor_zero_offset = [3, 3] # mm in x and y

    def run_test_sequence(sample_locs, points_per_loc, write_to_csv=False):
        


    def startup(self, delay=100, timeout=3):
        t1 = time.time()
        startup = self.msgConfirmation(10)
        print("Coms up")
        if startup:
            ready = self.msgConfirmation(11, timeout=10)
            print("Motors ready")
            if ready:
                return True
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
                print(msg)
                if msg == msgToBeReceived:
                    return True
        return False
    
    def runDemo(self):
        started = self.sendSerialMSG([4,0,0])
        if started:
            print("Successfully started")
            finished = self.msgConfirmation(2, timeout=30)
            if finished:
                print("Successfully finished")
                return True
        print("Failed to complete")
        return False

    def moveToPos(self, pos):
        # Send and confirm that command initiated
        start_motion = self.sendSerialMSG([2,pos[0],pos[1]*-1])
        is_finished = False
        if start_motion:
            print("motion started")
            finished_motion = self.msgConfirmation(2)
            if finished_motion:
                print("motion finished")
                is_finished = True
            else:
                print("motion failed to finish")
        else:
            print("motion failed to start")
        return is_finished

    def moveToSteps(self, steps):
        # Send and confirm that command initiated
        start_motion = self.sendSerialMSG([3,steps[0],steps[1]*-1])
        is_finished = False
        if start_motion:
            print("motion started")
            finished_motion = self.msgConfirmation(2)
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

    def writeToCSV(self, title="test_data\\test1.csv"):
        with open (title, 'w') as file:
            for i in range(self.stored_data.shape[0]):
                file.write("{0}\n".format(",".join([str(val) for val in self.stored_data[i].tolist()])))

    def get_grid_points(self, dims, deltas):
        # Be careful with the x_dim+dx and y_dim+dy for any non perfectly divisible dimensions by the deltas
        dx, dy = deltas
        x_dim, y_dim = dims
        x_offset, y_offset = self.sensor_zero_offset
        x_range = np.arange(start=0, stop=x_dim+dx, step=dx)
        y_range = np.arange(start=0, stop=y_dim+dy, step=dy)
    
        target_points = []
        for i in range(y_range.shape[0]):
            for j in range(x_range.shape[0]):
                target_points.append((x_range[j]+x_offset, y_range[i]+y_offset))
            print(target_points)
        return target_points

    def get_grid_points(self, dims, deltas):
        dx, dy = deltas
        x_dim, y_dim = dims
        x_range = np.arange(start=0, stop=x_dim, step=dx)
        y_range = np.arange(start=0, stop=y_dim, step=dy)




if __name__ == "__main__":
    test_bench = SensorTestBench()
    test_bench.sendSerialMSG([6,9,9])
