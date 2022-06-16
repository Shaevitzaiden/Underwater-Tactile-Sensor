#!/usr/bin/env python3

import time
import numpy as np
from myVizTools import LiveHeatmap


def separate_data(data):
    sensor_data = []
    for i in range(data.shape[0]):
        sensor_data.append(data[i,2:10].reshape((4,2)))
    return sensor_data



if __name__ == "__main__":
    data = np.load("test_data\\test_9_19.5_0.5_0.5.npy")
    sd = separate_data(data)

    heatmap = LiveHeatmap()
    heatmap.create_heat_map()
    heatmap.add_title("Tactile Sensor Visualization")

    for sample in sd:
        time.sleep(0.0005)
        heatmap.update_map(sample, scale=2)


