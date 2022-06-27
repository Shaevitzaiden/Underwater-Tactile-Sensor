import matplotlib.pyplot as plt
import numpy as np
import atexit
import time
import sys

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
        self.im = self.ax.imshow(data, cmap='Reds', vmin=0, vmax=10)
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
    
