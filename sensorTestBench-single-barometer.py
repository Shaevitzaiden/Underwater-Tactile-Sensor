#!/usr/bin/env python3

import time
from tracemalloc import start
import serial
import matplotlib.pyplot as plt
import numpy as np
import atexit
import sys

from myVizTools import LiveHeatmap


class SensorTestBench():
    def __init__(self):
        self.arduino = serial.Serial(port="COM5", baudrate=230400, timeout=0.5) # Don't forget to check port, can maybe automate finding the port
        ready = self.startup()
        if not ready:    
            print("Failed to initiate coms, retry")
            sys.exit()

        self.in_motion = False
        self.position = np.array([0,0])
        self.home_offsets = (0, 0)
        self.z = "lowered"
        self.sensor_calibration = np.zeros((1,))
        self.stored_data = None
        self.ambient = None
        # self.sensor_zero_offset = np.array([25, 3+4]) # mm in x and y
        # self.sensor_zero_offset = np.array([9.42, 3]) # mm in x and y
        self.pcb_from_reference = np.array((3, 3))
        self.sensor_center_from_pcb = np.array((12.56+3.3/2, 12.55+3.3/2))
        self.sensor_size = np.array((20,20))
        self.sensor_zero_offset = self.pcb_from_reference + self.sensor_center_from_pcb


        self.reset_offset = np.array([0,0])
        print("pre register")
        atexit.register(self.cleanup)
        print("post register")

    def run_test_sequence(self, sample_locs, restart_loc=None, samples=1, delay=1.5):
        if restart_loc != None:
            print("adjusting start location to", restart_loc)
            print(self.setStepperLocation(restart_loc))
            sample_locs_copy = sample_locs.copy()
            for loc in sample_locs:
                dist = np.sqrt((loc[0]-restart_loc[0])**2 + (loc[1]-restart_loc[1])**2)
                if dist < 0.01:
                    break
                else:
                    sample_locs_copy.remove(loc)
            sample_locs = sample_locs_copy
        
        # x, y, p_sens, p_amb, temp 
        self.stored_data = np.zeros((len(sample_locs), samples, 2+1+1+1))
        
        # Raise carriage at start
        self.moveZ("raise")

        # Move axes away from limit switches if applicable
        self.moveOffLimitSwitches()

        # Get a sensor calibration
        print("Getting sensor calibration")
        time.sleep(0.25)
        # if self.sensor_calibration[0] == 0: ---------------------- switching to calibration off of current atmospheric pressure
        #     self.getSensorCalibration()
        
        # Loop through a series of locations and take samples
        for i, loc in enumerate(sample_locs):
            # Move sensor into position (x,y)
            self.moveToPos(loc)
            self.stored_data[i,:,0:2] = [round(loc[0]-self.sensor_zero_offset[0],2), round(loc[1]-self.sensor_zero_offset[1],2)]

            # Get ambient pressure of silicone by averaging all 8 sensors
            # time.sleep(0.1)
            for j in range(samples):
                received, sens_data_amb = self.getSensorData()
                self.stored_data[i,j,3] = sens_data_amb[0]
            print("AMBIENT PRESSURE ~=", sens_data_amb[0])
            
            # Lower carriage for measurement
            self.moveZ("lower")
            time.sleep(delay)
            
            for k in range(samples):
                received, sens_data_p = self.getSensorData()
                received, sens_data_t = self.getSensorData(get_temp=True)
                self.stored_data[i,k,2] = sens_data_p[0]
                self.stored_data[i,k,4] = sens_data_t[0]
            print(sens_data_p)
            print("TEMPERATURE ~=", sens_data_t[0])
                # print(self.stored_data[i])
        
                # self.appendToCSV(self.stored_data[i])
            # for p in range(points_per_loc):
            #     _, sens_data = self.getSensorData()
            #     print(sens_data)
            #     self.stored_data[i,2:10] = sens_data
            #     print(self.stored_data[i])
            # self.moveZ("raise")
        
        # Move back to home position and lower
        self.moveToPos((0,0))
        self.moveZ("lower")
        self.saveArray()
        return self.stored_data
            
    def startup(self, delay=10, timeout=3):
        t1 = time.time()
        startup = self.msgConfirmation(10)
        print("Coms up")
        if startup:
            sensor_ready = self.msgConfirmation(12, timeout=3)
            if sensor_ready:
                return True
        return False
    
    def clean_inbox(self):
        print("--------------- emptying input buffer -------------------")
        while self.arduino.in_waiting > 0:
            msg = self.arduino.read_all()
        print("--------------- Finished Emptying --------------")

    def moveOffLimitSwitches(self):
        if self.z != "raised":
            self.moveZ("raise")
        received = self.sendSerialMSG([5,0,0])
        if received:
            print("moving off limit switches (if applicable)")
            if self.msgConfirmation(5):
                return True
            return False

    def sendSerialMSG(self, msg, begin_delimiter="<", end_delimiter=">", timeout=1):
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

    def setStepperLocation(self, loc):
        return self.sendSerialMSG([8,10*loc[0],10*loc[1]])

    def moveZ(self, action):
        if (action == "raise") and (self.z != "raised"):
            print("raising")
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
        start_motion = self.sendSerialMSG([2,100*pos[0],100*pos[1]]) # Multiplied by 10 as decimal would be lost in transfer, divided on arduino side to retain precision
        is_finished = False
        if start_motion:
            print("motion started to", pos)
            finished_motion = self.msgConfirmation(2)
            # loc_reached = self.receiveVectorData()
            if finished_motion:
                print("motion finished")
                self.position = pos
                print(pos)
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
        msg = []
        num_str = []
        while (time.time()-t1) < timeout:
            if self.arduino.in_waiting > 0:
                inData = self.arduino.read().decode()
                if (inData == ","):
                    msg.append(int("".join(num_str)))
                    num_str = []
                elif (inData == ">"):
                    rawData = np.array(msg, dtype=np.float64)
                    # print(rawData)
                    return True, rawData
                else:
                    num_str.append(inData)
        return False, None

    def getSensorData(self, get_temp=False, timeout=2):
        # print("Sending sensor data request")
        t0 = time.time()
        if get_temp:
            ready = self.sendSerialMSG([1,1,0])
        else:
            ready = self.sendSerialMSG([1,0,0]) 
        
        if ready:
            received, rawData = self.receiveVectorData()
            # print(received, rawData)
            if received is False:
                print("No data received")
                return False, None
            processedData = np.zeros(rawData.shape)
            if get_temp:
                processedData[0:1] = rawData[0:1]/100 # Degrees Celsius
            else:
                # Conversion from mbar to psi and apply calibration
                processedData[0:1] = rawData[0:1]/10*0.0145    # PSI
            return True, processedData
        print("Sensor did not receive request for data")
        return False, None 

    def getSensorCalibration(self):
        """ Get 1-point calibration """
        for i in range(10):
            msg_status, sens_data = self.getSensorData()
            time.sleep(0.1)
            if i == 0:
                calibration = sens_data
            else:
                calibration = (calibration + sens_data) / 2   
        self.sensor_calibration = calibration
        return calibration

    def appendToCSV(self, data, title="test_data\\DS20_100g_atm_delta-0.5mm_thick-8mm-single.csv"):
        with open (title, 'a') as file:
            file.write("{0}\n".format(",".join([str(val) for val in data.tolist()])))
        print("Finished appending to CSV")

    def writeToCSV(self, title="test_data\\DS10_100g_atm_0.5mm.csv"):
        with open (title, 'w') as file:
            for i in range(self.stored_data.shape[0]):
                file.write("{0}\n".format(",".join([str(val) for val in self.stored_data[i].tolist()])))

    def saveArray(self, title="test_data_multi-sample\\DS10_100g_50-PSI_delta-0.5mm_thick-8mm_single-barometer-16_multi-sample-10.npy"):
        np.save(title, self.stored_data)

    def get_grid_points(self, dims, deltas, border_offsets):
        # Be careful with the x_dim+dx and y_dim+dy for any non perfectly divisible dimensions by the deltas
        dx, dy = deltas
        x_dim, y_dim = dims
        x_offset, y_offset = self.sensor_zero_offset
        x_range = np.arange(start=border_offsets[0], stop=x_dim+dx-border_offsets[1], step=dx)
        y_range = np.arange(start=border_offsets[0], stop=y_dim+dy-border_offsets[1], step=dy)
        target_points = []
        for i in range(y_range.shape[0]):
            for j in range(x_range.shape[0]):
                target_points.append((round(x_range[j]+x_offset-(x_dim/2),1), round(y_range[i]+y_offset-(y_dim/2),1)))
        return target_points

    def get_line_points(self, length, delta):
        x_range = np.arange(start=self.sensor_zero_offset[0], stop=self.sensor_zero_offset[0]+length+delta, step=delta)
        y = self.sensor_zero_offset[1]
        target_points = []
        for i in range(x_range.shape[0]):
            target_points.append((round(x_range[i],1), round(y,1)))
        return target_points

    def cleanup(self):
        self.moveZ("lower")



if __name__ == "__main__":
    test_bench = SensorTestBench()
    # print(test_bench.getSensorData())
    
    # test_bench.moveZ("lower")

    # test_bench.sendSerialMSG([6,9,9])
    # test_bench.moveToPos(test_bench.sensor_zero_offset)
    # time.sleep(10)
    
    # test_bench.moveToPos(-test_bench.sensor_zero_offset)
    # test_bench.moveZ("lower")
    # time.sleep(4)
    # test_bench.moveToPos((0,0))
    # test_bench.moveZ("lower")


    # test_bench.moveToPos(test_bench.sensor_zero_offset)
    
    # --------------------------------------------------------
    locs = test_bench.get_grid_points((16,16), (0.5,0.5), (0.5,0.5))
    # locs = test_bench.get_line_points(8,0.5)
    # print(locs)
    # locs = test_bench.get_grid_points((2,2), (0.5,0.5), (0.5,0.5))

    # print(locs)
    # locs = test_bench.get_grid_points((3,3), (0.5,0.5))
    # test_bench.run_test_sequence(locs) 
    # x_off, y_off = test_bench.sensor_zero_offset
   # test_bench.run_test_sequence(locs, samples=10)
    for i in range(1000):
        print(i)
        a, b = test_bench.getSensorData()
        print(b)
        if (np.abs(b) > 20000).any():
            print("error")
            break
    # test_bench.run_test_sequence(locs, restart_loc=(4.0+x_off,0+y_off))
    # --------------------------------------------------------
    
    
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
