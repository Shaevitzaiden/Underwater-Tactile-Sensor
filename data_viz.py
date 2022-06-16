#!/usr/bin/env python3

import time
import numpy as np
from myVizTools import LiveHeatmap


def separate_data(data):
    sensor_data = []
    temp_data = np.zeros((4,2))
    for i in range(data.shape[0]):
        temp_data[:,1] = data[i,2:6]
        temp_data[:,0] = np.flip(data[i,6:10])
        sensor_data.append(temp_data.copy())
    return sensor_data



if __name__ == "__main__":
    data = np.load("test_data\\test_0.5mm.npy")
    sd = separate_data(data)

    heatmap = LiveHeatmap()
    heatmap.create_heat_map()
    heatmap.add_title("Tactile Sensor Visualization")

    for sample in sd:
        time.sleep(0.0005)
        heatmap.update_map(sample, scale=2)


