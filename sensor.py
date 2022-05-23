#!/usr/bin/env python3

import time

import matplotlib.pyplot as plt
import numpy as np
import serial
import sys

arduino = serial.Serial(port="COM3", baudrate=115200, timeout=0.1)


class LiveHeatmap:
    def __init__(self):
        self.map_size = None
        self.fig = None
        self.ax = None
        self.im = None
    
    def create_heat_map(self, data=None, text=True):
        if data is None:
            data = np.random.random((4,2))
        self.fig = plt.figure()
        self.fig.canvas.mpl_connect('close_event', self.save_fig)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        if text:
            self.create_text(data)
        self.im = self.ax.imshow(data, cmap='Reds', vmin=0, vmax=0.25)
        plt.show(block=False)

    def update_map(self, data, scale=1, text=True):
        if self.fig is None:
            self.create_heat_map(data)

        time.sleep(0.1)
        self.im.set_array(data*scale)
        if text:
            self.update_text(data)
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    def create_text(self, data):
        row, col = data.shape
        for i in range(row):
            for j in range(col):
                self.ax.text(j, i, round(data[i, j], 3),
                       ha="center", va="center", color="w")

    def update_text(self, data):
        row, col = data.shape
        idx = 0
        for i in range(row):
            for j in range(col):
                self.ax.texts[idx].set_text(round(data[i, j], 3))
                idx += 1

    def set_axes_ticks(self, xticks, yticks):
        self.ax.set_xticks(xticks)
        self.ax.set_yticks(yticks)
    
    def add_title(self, title):
        self.ax.set_title(title)

    def save_fig(self, needs_to_be_here_for_some_reason):
        plt.savefig("C:\\Users\\Aiden\\Documents\\Research\\UnderwaterTactileSensor\\Underwater-Tactile-Sensor\\Figures\\heatmap.png")
        sys.exit()
    

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
    pass

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
        heatmap = LiveHeatmap()
        heatmap.create_heat_map()
        heatmap.add_title("Tactile Sensor Visualization")
        saved = False
        i = 0
        while True:
            i += 1
            # writeCommand("run")
            msg_status, sens_data = readSensorData(calibration=cal)
            # time.sleep(0.005)
            if msg_status != False:
                heatmap.update_map(sens_data, scale=3)

    else:
        print("failed to startup")


