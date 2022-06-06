#!/usr/bin/env python3

import time
import serial
import matplotlib.pyplot as plt
import numpy as np

from myVizTools import LiveHeatmap

arduino = serial.Serial(port="COM3", baudrate=115200, timeout=0.1)


    

def getCalibration():
    """ Get 1-point calibration """
    for i in range(10):
        msg_status, sens_data = getSensorData()
        if i == 0:
            calibration = sens_data
        else:
            calibration = (calibration + sens_data) / 2   
    return calibration


def getSensorData(calibration=None, timeout=1):
    ready = sendSerialMSG([1,0,0])
    if ready:
        reshapedData = np.zeros((4,2))
        t1 = time.time()
        while (time.time()-t1) < timeout:
            if arduino.in_waiting > 0:
                inData = arduino.read_until().decode().split(",") 
                if inData[0] == '':
                    return False, None
                rawData = np.array([int(i) for i in inData], dtype=np.float64)
                reshapedData[:,1] = rawData[0:4]
                reshapedData[:,0] = np.flip(rawData[4:])
                processedData = reshapedData/10*0.0145
                if calibration is not None:
                    processedData -= calibration
                return True, processedData
    return False, None 

def sendSerialMSG(msg, begin_delimiter="<", end_delimiter=">", timeout=100):
    """ Send msg by serial line, expects to recieve the same message back as confirmation"""
    t1 = time.time()
    msg_str = "{0}{1},{2},{3}{4}".format(begin_delimiter, msg[0], msg[1], msg[2], end_delimiter)
    msg_bytes = bytes(msg_str, 'utf-8')
    arduino.write(msg_bytes)
    
    # Wait for confirmation and try to resend message if not received
    confirmation = msgConfirmation(msg[0])
    while not confirmation and (time.time() - t1) < timeout:
        arduino.write(msg)
        confirmation = msgConfirmation(msg[0])
    return confirmation

def msgConfirmation(msgToBeReceived, timeout=100):
    t1 = time.time()
    while (time.time() - t1) < timeout:
        if arduino.in_waiting > 0:
            msg = int(arduino.read_until().decode()[:-2])
            if msg == msgToBeReceived:
                return True
    return False

def startup(delay=100, timeout=3):
    start_time = time.time()
    while True:
        if arduino.in_waiting > 0:
            inByte = int(arduino.read_until().decode())
            if inByte == 1:
                print("startup successful")
                return True
        elif (time.time()-start_time) > timeout:
            return False

def writeToCSV(data, title="test_data\\test1.csv"):
    with open (title, 'w') as file:
        for i in range(data.shape[0]):
            file.write("{0}\n".format(",".join([str(val) for val in data[i].tolist()])))


if __name__ == "__main__":
    ready = startup()
    if ready:
        cal = getCalibration()
        # print(cal)
        # t1 = time.time()
        # for i in range(10):
        #     msg_status, sens_data = getSensorData()
        # print("Hz = {0}".format(10/(time.time()-t1)))


    # if ready:
    #     print("starting program")
    #     cal = getCalibration()
        # heatmap = LiveHeatmap()
        # heatmap.create_heat_map()
        # heatmap.add_title("Tactile Sensor Visualization")
        saved = False
        i = 0
        iterations = 10
        store_data = np.zeros((iterations,8))
        while i<iterations:
            
    #         # writeCommand("run")
            msg_status, sens_data = getSensorData(calibration=cal)
            time.sleep(0.005)
            if msg_status != False:
                store_data[i] = sens_data.flatten()
                # heatmap.update_map(sens_data, scale=2)
                # write to csv file      
            i += 1  
        writeToCSV(store_data)

    else:
        print("failed to startup")


