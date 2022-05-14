#!/usr/bin/env python3

import time

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import serial

arduino = serial.Serial(port="COM3", baudrate=115200, timeout=0.1)

""" I need to consider creating starting and ending packet information for sending to the arduino so that it can tell what kind
of stuff I am sending to it. For instance, if I send it a packet wrapped like: '<>' and I am expecting a packet like '{}' I know
that one is for commands and the other is for the number of steps from home to move to reach the edge of the sensor. This could
be important if I end up having issues where the buffer has stuff missordered. Can maybe get around this by using sleep/delay commands.
"""

def writeCommand(command):
    """ Writes command to arduino to initiate different functionalities
    :params string command: "run" or "manual" to start a test cycle or manually control via a gui
    """
    # if arduino.in_waiting > 0:
    #     print("reset buffer, {} bytes in buffer".format(arduino.in_waiting))
    #     arduino.reset_input_buffer()
    
    # print("sending command")
    if command.lower() == "run":
        msg = 0
        # print("----------------------")
    elif command.lower() == "manual":
        msg = 1
    # print(msg)
    received = False
    arduino.write(bytes(str(msg).encode("utf-8")))
    while not received:
        # print(arduino.out_waiting)
        # print(arduino.write(bytes(str(msg).encode("utf-8"))))
        time.sleep(0.1)
        if arduino.in_waiting > 0:
            # print("attempting to read, {} bytes in buffer".format(arduino.in_waiting))
            inByte=arduino.read_until()
            # print(int(inByte.decode()))
            received = True
        time.sleep(1)
    return inByte

def getCalibration():
    """ Get 1-point calibration 
    """
    for i in range(10):
        while True:
            if arduino.in_waiting > 0:
                inData = arduino.read_until().decode().split(",") 
                if inData[0] == '':
                    continue
                processedData = np.array([int(i) for i in inData], dtype=np.int64)
                if i == 0:
                    calibration = processedData 
                else:
                    calibration = (calibration + processedData) / 2   
                break         
    return calibration

def readSensorData(calibration=None, timeout=5):
    reshapedData = np.zeros((4,2))
    t1 = time.time()
    while (time.time()-t1) < timeout:
        if arduino.in_waiting > 0:
            inData = arduino.read_until().decode().split(",") 
            if inData[0] == '':
                return False, None
            rawData = np.array([int(i) for i in inData], dtype=np.float64)
            if calibration is not None:
                rawData -= calibration
            reshapedData[:,1] = rawData[0:4]
            reshapedData[:,0] = np.flip(rawData[4:])
            processedData = reshapedData/10*0.0145
            return True, processedData
        return False, None 

def vizSensorData(fig, ax, im, data, scale=1) -> None:
    time.sleep(0.1)
    im.set_array(data*scale)
    row, col = data.shape
    for i in range(row):
        for j in range(col):
            ax.texts[(j*col)+i].set_text(round(data[i, j], 3))
    fig.canvas.draw()
    fig.canvas.flush_events()


def sendSerialMSG(msg, delimiter="\n"):
    msg_str = "{0}{1}".format(msg, delimiter)
    # msg_str = "{0} {1}".format(msg,delimiter)
    msg = bytes(msg_str, 'utf-8')
    print(msg)
    # arduino.write(bytes("\n"))
    # time.sleep(0.1)
    # confirmation = False
    # while not confirmation:
    #     if arduino.in_waiting > 0:
    #         confirmation = True
    #         print(arduino.readline().decode())



def startup(delay=100, timeout=5):
    start_time = time.time()
    while True:
        if arduino.in_waiting > 0:
            inByte = int(arduino.read_until().decode())
            print("received serial startup byte")
            # arduino.write(bytes(str(delay).encode("utf-8")))
            # received = False
            # while not received or (time.time()-start_time) > timeout:
            #     if arduino.in_waiting > 0:
            #         received = True
            #         returnMsg=arduino.read_until().decode()
            #         print("startup successful, {}".format(returnMsg))
            return True
        if (time.time()-start_time) > timeout:
            return False

if __name__ == "__main__":
    ready = startup()
    if ready:
        sendSerialMSG(5)

    if ready:
        print("starting program")
        cal = getCalibration()
        rand_startup_data = np.random.random((4,2))
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.set_xticks([0, 1])
        ax.set_yticks([3, 2, 1, 0])
        im = ax.imshow(rand_startup_data, cmap='Reds')
        plt.show(block=False)
        for i in range(4):
            for j in range(2):
                text = ax.text(j, i, round(rand_startup_data[i, j],3),
                            ha="center", va="center", color="w")
        
        while True:
            # writeCommand("run")
            msg_status, sens_data = readSensorData(calibration=cal)
            # time.sleep(0.005)
            if msg_status != False:
                vizSensorData(fig, ax, im, sens_data, scale=5)
                print(sens_data)
            # time.sleep(1)
    else:
        print("failed to startup")


