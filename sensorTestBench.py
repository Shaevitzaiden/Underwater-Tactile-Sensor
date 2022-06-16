#!/usr/bin/env python3

import time
import serial
import matplotlib.pyplot as plt
import numpy as np
import atexit
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
        self.position = (0, 0)
        self.home_offsets = (0, 0)
        self.z = "lowered"
        self.sensor_calibration = np.zeros((8,))
        self.stored_data = None
        self.sensor_zero_offset = np.array([3+10.5, 3+4]) # mm in x and y
        print("pre register")
        atexit.register(self.cleanup)
        print("post register")

    def run_test_sequence(self, sample_locs, points_per_loc=1, delay=1):
        self.stored_data = np.zeros((len(sample_locs), 8+1+1+1+2))
        self.moveZ("raise")
        self.moveOffLimitSwitches()
        if self.sensor_calibration[0] == 0:
            self.getSensorCalibration()
        for i, loc in enumerate(sample_locs):
            self.moveToPos(loc)
            print("lowering")
            self.moveZ("lower")
            self.stored_data[i,0:2] = [loc[0]-self.sensor_zero_offset[0], loc[1]-self.sensor_zero_offset[1]]
            time.sleep(delay)
            
            _, sens_data = self.getSensorData()
            print(sens_data)
            self.stored_data[i,2:10] = sens_data
            print(self.stored_data[i])
            time.sleep(0.1)
            # for p in range(points_per_loc):
            #     _, sens_data = self.getSensorData()
            #     print(sens_data)
            #     self.stored_data[i,2:10] = sens_data
            #     print(self.stored_data[i])
            # self.moveZ("raise")
        self.moveToPos((0,0))
        self.moveZ("lower")
        return self.stored_data

    def startup(self, delay=100, timeout=3):
        t1 = time.time()
        startup = self.msgConfirmation(10)
        print("Coms up")
        if startup:
            sensor_ready = self.msgConfirmation(12, timeout=3)
            if sensor_ready:
                return True
        return False
    
    def moveOffLimitSwitches(self):
        if self.z != "raised":
            self.moveZ("raise")
        received = self.sendSerialMSG([5,0,0])
        if received:
            print("moving off limit switches (if applicable)")
            if self.msgConfirmation(5):
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

    def msgConfirmation(self, msgToBeReceived, timeout=8):
        t1 = time.time()
        while (time.time() - t1) < timeout:
            if self.arduino.in_waiting > 0:
                msg = int(self.arduino.read_until().decode()[:-2])
                # print(msg)
                if msg == msgToBeReceived:
                    return True
        return False
    
    def getHomeOffset(self):
        ready = self.sendSerialMSG([7,0,0])
        if ready:
            _, offsets = self.receiveVectorData()
            self.home_offsets = (offsets[0], offsets[1])
            return offsets
        return None

    def moveZ(self, action):
        if (action == "raise") and (self.z != "raised"):
            self.sendSerialMSG([4,0,0])
            self.z = "raised"
        if (action == "lower") and (self.z != "lowered"):
            self.sendSerialMSG([4,1,0])
            self.z = "lowered"
        if isinstance(action, (int,float)):
            self.sendSerialMSG([4,2,int(action)]) # Sends degrees to move (may change to steps for my own laziness) 
        if self.msgConfirmation(4):
            return True
        return False

    def moveToPos(self, pos):
        if self.z != "raised":
            self.moveZ("raise")
        # Send and confirm that command initiated
        start_motion = self.sendSerialMSG([2,10*pos[0],10*pos[1]]) # Multiplied by 10 as decimal would be lost in transfer, divided on arduino side to retain precision
        is_finished = False
        if start_motion:
            print("motion started to", pos)
            finished_motion = self.msgConfirmation(2)
            loc_reached = self.receiveVectorData()
            if finished_motion:
                print("motion reached ", loc_reached)
                is_finished = True
            else:
                print("motion failed to finish")
        else:
            print("motion failed to start")
        return is_finished

    def moveToSteps(self, steps):
        if self.z != "raised":
            self.moveZ("raise")
        # Send and confirm that command initiated
        start_motion = self.sendSerialMSG([3,steps[0],steps[1]])
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

    def receiveVectorData(self, timeout=1):
        t1 = time.time()
        while (time.time()-t1) < timeout:
            if self.arduino.in_waiting > 0:
                inData = self.arduino.read_until().decode().split(",") 
                if inData[0] == '':
                    return False, None
                rawData = np.array([int(i) for i in inData], dtype=np.float64)
                return True, rawData
        return False, None

    def getSensorData(self, timeout=1):
        ready = self.sendSerialMSG([1,0,0])
        if ready:
            _, rawData = self.receiveVectorData()
            # reshapedData = np.zeros((4,2))
            # reshapedData[:,1] = rawData[0:4]
            # reshapedData[:,0] = np.flip(rawData[4:])
            reshapedData = rawData
            processedData = reshapedData/10*0.0145
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

    def writeToCSV(self, title="test_data\\test_0.5mm.csv"):
        with open (title, 'w') as file:
            for i in range(self.stored_data.shape[0]):
                file.write("{0}\n".format(",".join([str(val) for val in self.stored_data[i].tolist()])))

    def saveArray(self, title="test_data\\test_0.5mm.npy"):
        np.save(title, self.stored_data)

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
        return target_points

    def cleanup(self):
        self.moveZ("lower")



if __name__ == "__main__":
    test_bench = SensorTestBench()
    # test_bench.sendSerialMSG([6,9,9])
    # test_bench.moveToPos(test_bench.sensor_zero_offset)
    # time.sleep(10)
    
    # test_bench.moveToPos(-test_bench.sensor_zero_offset)
    # test_bench.moveZ("lower")
    # time.sleep(4)
    # test_bench.moveToPos((0,0))
    # test_bench.moveZ("lower")


    # test_bench.moveToPos(test_bench.sensor_zero_offset)
    locs = test_bench.get_grid_points((9,19.5), (0.5,0.5))
    test_bench.run_test_sequence(locs)
    test_bench.saveArray()
    test_bench.writeToCSV()
    
    
    # test_bench.moveToPos(test_bench.sensor_zero_offset)
    # test_bench.moveZ("lower")
    # time.sleep(5)
    # test_bench.moveToPos((0,0))
    # # test_bench.getSensorCalibration()
    # # test_bench.moveZ("raise")
    # # test_bench.moveOffLimitSwitches()
    # test_bench.moveZ("lower")
    
#------------------------------------------------------
#     cal = test_bench.getSensorCalibration()
#     heatmap = LiveHeatmap()
#     heatmap.create_heat_map()
#     heatmap.add_title("Tactile Sensor Visualization")
# #     saved = False
#     i = 0
#     iterations = 1000
# #     store_data = np.zeros((iterations,8))
#     while i<iterations:
#         msg_status, sens_data = test_bench.getSensorData()
#         time.sleep(0.005)
#         if msg_status != False:
#             print(sens_data)
#             heatmap.update_map(sens_data, scale=2)

#         i += 1  
