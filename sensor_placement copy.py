#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


class Circle():
    def __init__(self, radius, center=(0,0)):
        self.radius = radius
        self.center = np.array(center)

    def move_circle(self, new_center):
        self.center = np.array(new_center)

    def copy(self):
        return Circle(self.radius, self.center)

    def permutate(self, grid_shape):
        old_center = self.center.copy()
        if (old_center[0] > 0) and (old_center[0] < (grid_shape[0]-1)):
            r_options = [-1, 0, 1]
        elif (old_center[0] > 0) and (old_center[0] == (grid_shape[0]-1)):
            r_options = [-1, 0]
        elif (old_center[0] == 0) and (old_center[0] < (grid_shape[0]-1)):
            r_options = [1, 0]
        
        if (old_center[1] > 0) and (old_center[1] < (grid_shape[1]-1)):
            c_options = [-1, 0, 1]
        elif (old_center[1] > 0) and (old_center[1] == (grid_shape[1]-1)):
            c_options = [-1, 0]
        elif (old_center[1] == 0) and (old_center[1] < (grid_shape[1]-1)):
            c_options = [1, 0]
        
        self.move_circle((self.center[0] + np.random.choice(r_options), self.center[1] + np.random.choice(c_options)))


class GridSpace():
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
        
    def get_coverage(self, sol):
        self.update_grid_vals(sol)
        # get NC, SA, and CC areas for use as heuristics
        nc = (self.grid_vals == 0).sum()
        sa = (self.grid_vals == 1).sum()
        pc = (self.grid_vals == 2).sum()
        fc = (self.grid_vals >= 3).sum()
        return nc, sa, pc, fc

    def update_grid_vals(self, circles):
        self.grid_vals *= 0
        for circle in circles:
            circle_center = (int(circle.center[0]/self.delta), int(circle.center[1]/self.delta))
            circle_radius = int(circle.radius/self.delta)
            dist_sqrd = np.sum((self.grid_mask-circle_center)**2,axis=2)
            inside = dist_sqrd < circle_radius**2
            self.grid_vals[inside] += 1

    def convert_grid_to_physical(self):
        return self.grid_mask*self.delta
    
    def plot_circles_grid(self, circles):
        self.update_grid_vals(circles)
        fig = plt.figure()
        ax = fig.add_subplot(111)
        cm = ax.imshow(self.grid_vals)#,cmap="gnuplot2_r")
        fig.colorbar(cm, ax=ax)
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
    def __init__(self, grid, circles):
        self.grid = grid
        self.circles = circles
        self.grid_area = grid.grid_vals.shape[0] * grid.grid_vals.shape[1]
        self.start_cost = self.cost(circles)
        self.best_sol = circles
        self.best_distances = []
        
    def cost(self, sol):
        c = self.grid.get_coverage(sol)
        return self.grid.grid_vals.size*(50*c[0] + 0.5*c[1]) - 3*c[3] - 2*c[2]

    def optimize(self, start_temp, min_temp, temp_step):
        num_circles = len(self.best_sol)
        current_temp = start_temp
        current_sol = [c.copy() for c in self.best_sol]
        while current_temp > min_temp:
            candidate = [c.copy() for c in current_sol]
            for i in range(num_circles):
                # generate new candidate
                candidate[i].permutate(self.grid.grid_vals.shape)
                # update current solution (may just stay the same)
                current_sol = self.update_solutions(candidate, current_sol, current_temp)
                # lower temperature
            current_temp -= temp_step
                # self.best_distances.append(self.tsp.total_distance(self.tsp.closed_path(self.tsp.curre
                # nt_path)))
        self.solution()
        return self.best_sol
    
    def update_solutions(self, candidate, current_sol, current_temp):
        a = self.cost(candidate)
        b = self.cost(current_sol)
        delta_cost = a - b
        if delta_cost < 0:
            current_sol = candidate
            self.best_sol = candidate
        elif np.random.uniform() < np.exp(-delta_cost/current_temp):
            current_sol = candidate
        else:
            pass
        return current_sol
    
    def solution(self):
        print("Old cost = {0}, New cost = {1}".format(self.start_cost,
        self.cost(self.best_sol)))
 

if __name__ == "__main__":
    sensor_size = (25,50) # 25 wide X 75 tall ......... results in 75 rows and 25 columns
    grid = GridSpace(sensor_size, 1)
    centers = [(np.random.randint(0,sensor_size[1]), np.random.randint(0,sensor_size[0])) for i in range(8)]
    print(centers)
    circles = [Circle(9.5, centers[i]) for i in range(8)]
    # grid.update_grid_vals(circles)
    # grid.plot_circles_grid(circles)
    # t = TabuList()
    # centers_tuple = tuple(np.array([c.center for c in circles]).reshape((len(circles)*2,)))
    
    sa = SimulatedAnnealing(grid, circles)
    sol = sa.optimize(50, 0.01, 0.001)
    for i in range(8):
        print(sol[i].center)
    grid.plot_circles_grid(sol)

    # for i in range(100):
    #     circles[0].permutate(grid.grid_vals.shape)