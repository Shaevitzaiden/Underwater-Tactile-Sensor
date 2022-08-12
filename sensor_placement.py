#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


class Circle():
    def __init__(self, radius, center=(0,0)):
        self.radius = radius
        self.center = np.array(center)

    def move_circle(self, new_center):
        self.center = np.array[new_center]

    def copy(self):
        return Circle(self.radius, self.center)

    def permutate(self,):
        self.move_circle(np.random.randint(-1, 2), np.random.randint(-1, 2))


class SensorGrid():
    def __init__(self, dims, delta):
        self.delta = delta
        self.cols = int(dims[0] / delta)
        self.rows = int(dims[1] / delta)
        self.grid_vals = np.zeros((self.rows,self.cols))
        
        # Make mask of coordinates in their corresponding location
        grid_mask = []
        for r in range(self.rows):
            grid_mask_row = []
            for c in range(self.cols):
                grid_mask_row.append([r,c])
            grid_mask.append(grid_mask_row.copy())
        self.grid_mask = np.array(grid_mask)
        
    def get_coverage(self):
        # get NC, SA, and CC areas for use as heuristics
        nc = (self.grid_vals <=1).sum()
        sa = (self.grid_vals == 2).sum()
        cc = (self.grid_vals > 2).sum()
        return nc, sa, cc

    def update_grid_vals(self, circles):
        for circle in circles:
            circle_center = (int(circle.center[0]/self.delta), int(circle.center[1]/self.delta))
            circle_radius = int(circle.radius/self.delta)
            dist_sqrd = np.sum((self.grid_mask-circle_center)**2,axis=2)
            inside = dist_sqrd < circle_radius**2
            self.grid_vals[inside] += 1

    def convert_grid_to_physical(self):
        return self.grid_mask*self.delta
    
    def plot_circles_grid(self, circles):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.imshow(self.grid_vals,cmap="gnuplot2_r")
        for circle in circles:
            x, y = self.generate_circle_array(circle.radius, circle.center)
            ax.plot(x,y,'black')
        plt.show()

    def generate_circle_array(self, radius, center):
        angles = np.linspace(0, 2*np.pi, 200)
        x = radius/self.delta * np.cos(angles) + center[1]/self.delta
        y = radius/self.delta * np.sin(angles) + center[0]/self.delta
        return x, y


class TabuList():
    def __init__(self):
        self.tabulist = set()
    
    def push(self, centers):
        self.tabulist.add(centers)
    
    def is_in(self, centers):
        return centers in self.tabulist
    
class TabuOptimize():
    def __init__(self) -> None:
        self.best_sol = None
    
    def tabu(self, grid, circles, tabulist, iterations=100):
        current_sol = [c.copy() for c in circles]
        best_sol = [c.copy() for c in circles]
        tabulist.push(current_sol)

    def get_neighbors(current_sol):
        neighbors = []
        for i in range(len(current_sol)):
            neighbor = [c.copy() for c in current_sol]
            neighbor[i].permutate()
            neighbors.append(neighbor)

class SimulatedAnnealing:
    def __init__(self, TSP_instance, start_temp, min_temp, temp_step):
        self.tsp = TSP_instance
        self.start_cost = TSP_instance.total_distance(TSP_instance.current_path)
        self.best_path = None
        self.best_distances = []
        self.unique_solutions = np.array([self.tsp.current_path.copy()])
        self.optimize(start_temp, min_temp, temp_step)
    
    def optimize(self, start_temp, min_temp, temp_step):
        current_temp = start_temp
        while current_temp > min_temp:
            # generate new candidate
            candidate, rows = self.tsp.random_swap()
            self.unique_solutions = np.concatenate([self.unique_solutions, np.array([candidate])],
            axis=0)
            # update current solution (may just stay the same)
            self.update_solutions(candidate, rows, current_temp)
            # lower temperature
            current_temp -= temp_step
            self.best_distances.append(self.tsp.total_distance(self.tsp.closed_path(self.tsp.curre
            nt_path)))
    
    def update_solutions(self, candidate, rows, current_temp):
        a = self.tsp.total_distance(candidate)
        b = self.tsp.total_distance(self.tsp.current_path)
        delta_cost = a - b
        if delta_cost < 0:
            self.tsp.current_path = candidate
            self.tsp.path_order[rows] = self.tsp.path_order[[rows[1], rows[0]]]
            self.best_path = candidate
        elif np.random.uniform() < np.exp(-delta_cost/current_temp):
            self.tsp.current_path = candidate
            self.tsp.path_order[rows] = self.tsp.path_order[[rows[1], rows[0]]]
        else:
            pass
    
    def solution(self):
        print("Old cost = {0}, New cost = {1}".format(self.start_cost,
        self.tsp.total_distance(self.best_path)))
 

if __name__ == "__main__":
    grid_size = (20,50)
    grid = SensorGrid(grid_size, 0.1)
    circles = [Circle(9.5, (0,0)) for i in range(8)]
    grid.update_grid_vals(circles)
    # grid.plot_circles_grid(circles)
    t = TabuList()
    centers_tuple = tuple(np.array([c.center for c in circles]).reshape((len(circles)*2,)))